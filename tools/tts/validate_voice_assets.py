#!/usr/bin/env python3
"""Validate Episode 001 voice WAV assets; missing recordings are pending by default."""
from __future__ import annotations

import argparse
import json
import math
import struct
import sys
import wave
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "episodes" / "001-english-at-the-airport" / "voice-manifest.json"
ALLOWED_RATES = {22050, 24000, 44100, 48000}
ALLOWED_CHANNELS = {1, 2}
VALID_ROLES = {"Narrator", "Leo", "Emma", "Airport Agent", "Security Officer", "Ollie"}


def timestamp_ms(value: str) -> int:
    hours, minutes, tail = value.split(":")
    seconds, millis = tail.split(",")
    return (((int(hours) * 60 + int(minutes)) * 60) + int(seconds)) * 1000 + int(millis)


def safe_asset_path(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
    base = root.resolve()
    if candidate != base and base not in candidate.parents:
        raise ValueError(f"path escapes repository root: {relative}")
    return candidate


def inspect_wav(path: Path, slot_seconds: float, tolerance: float) -> tuple[dict, list[str]]:
    problems: list[str] = []
    try:
        with wave.open(str(path), "rb") as wav:
            channels = wav.getnchannels()
            sample_width = wav.getsampwidth()
            sample_rate = wav.getframerate()
            frames = wav.getnframes()
            compression = wav.getcomptype()
            duration = frames / float(sample_rate) if sample_rate else 0.0
            if compression != "NONE":
                problems.append(f"unsupported WAV compression: {compression}")
            if sample_width != 2:
                problems.append(f"expected 16-bit PCM, found {sample_width * 8}-bit")
            if sample_rate not in ALLOWED_RATES:
                problems.append(f"unsupported sample rate: {sample_rate} Hz")
            if channels not in ALLOWED_CHANNELS:
                problems.append(f"expected mono/stereo, found {channels} channels")
            if frames <= 0 or duration <= 0:
                problems.append("empty audio")
            if duration > slot_seconds + tolerance:
                problems.append(f"clip {duration:.3f}s exceeds slot {slot_seconds:.3f}s (+{tolerance:.3f}s tolerance)")
            if duration < 0.10:
                problems.append(f"clip is implausibly short ({duration:.3f}s)")
            # Check the complete PCM payload for an all-zero/silent file.
            wav.rewind()
            peak = 0
            while True:
                chunk = wav.readframes(16384)
                if not chunk:
                    break
                usable = len(chunk) - (len(chunk) % 2)
                if usable:
                    count = usable // 2
                    samples = struct.unpack("<" + ("h" * count), chunk[:usable])
                    local_peak = max(abs(value) for value in samples) if samples else 0
                    if local_peak > peak:
                        peak = local_peak
                        if peak >= 32:
                            break
            if peak < 32:
                problems.append("audio is silent or near-silent (peak below 32/32767)")
            return {
                "duration": duration,
                "sample_rate": sample_rate,
                "channels": channels,
                "sample_width": sample_width,
                "peak": peak,
            }, problems
    except (wave.Error, EOFError, OSError, struct.error) as exc:
        return {}, [f"cannot read WAV: {exc}"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root used to resolve manifest paths")
    parser.add_argument("--strict", action="store_true", help="fail when any expected recording is missing")
    parser.add_argument("--tolerance", type=float, default=0.12, help="allowed overrun beyond each provisional cue slot, in seconds")
    args = parser.parse_args()

    if args.tolerance < 0:
        parser.error("--tolerance must be non-negative")
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot load voice manifest: {exc}")
        return 2

    cues = data.get("cues")
    if not isinstance(cues, list) or not cues:
        print("ERROR: voice manifest has no cues")
        return 2

    errors: list[str] = []
    missing: list[str] = []
    checked = defaultdict(int)
    formats: dict[str, set[tuple[int, int, int]]] = defaultdict(set)
    seen_paths: set[str] = set()
    seen_ids: set[int] = set()

    for index, cue in enumerate(cues, start=1):
        cue_id = cue.get("id")
        if not isinstance(cue_id, int) or cue_id in seen_ids:
            errors.append(f"cue {index}: invalid or duplicate cue ID {cue_id!r}")
            continue
        seen_ids.add(cue_id)
        if cue.get("role") not in VALID_ROLES:
            errors.append(f"cue {cue_id}: unknown role {cue.get('role')!r}")
        try:
            slot_ms = timestamp_ms(cue["end"]) - timestamp_ms(cue["start"])
            if slot_ms <= 0:
                raise ValueError("non-positive cue slot")
        except (KeyError, ValueError, TypeError) as exc:
            errors.append(f"cue {cue_id}: invalid start/end timing ({exc})")
            continue
        slot_seconds = slot_ms / 1000.0

        for lang, key in (("en", "english_file"),):
            relative = cue.get(key, "")
            if not isinstance(relative, str) or not relative:
                errors.append(f"cue {cue_id} ({lang}): missing {key} path")
                continue
            if relative in seen_paths:
                errors.append(f"cue {cue_id} ({lang}): duplicate asset path {relative}")
                continue
            seen_paths.add(relative)
            try:
                asset = safe_asset_path(args.root, relative)
            except ValueError as exc:
                errors.append(f"cue {cue_id} ({lang}): {exc}")
                continue
            if not asset.is_file():
                missing.append(relative)
                continue
            info, problems = inspect_wav(asset, slot_seconds, args.tolerance)
            if problems:
                for problem in problems:
                    errors.append(f"cue {cue_id} ({lang}) {relative}: {problem}")
                continue
            checked[lang] += 1
            formats[lang].add((info["sample_rate"], info["channels"], info["sample_width"]))

    expected_ids = set(range(1, len(cues) + 1))
    if seen_ids != expected_ids:
        errors.append("cue IDs must be sequential from 1 through the manifest cue count")
    if len(cues) != 48:
        errors.append(f"expected 48 cues for Episode 001, found {len(cues)}")
    for lang, found in formats.items():
        if len(found) > 1:
            errors.append(f"{lang}: audio format is inconsistent across clips: {sorted(found)}")

    expected = len(cues)
    completed = checked["en"]
    print("ENGLISHTALE VOICE ASSET VALIDATION")
    print(f"Manifest cues: {len(cues)} | expected English WAV files: {expected}")
    print(f"Valid English clips: {completed}/{len(cues)} | Afghan Dari voiceover: disabled (subtitles only)")
    print(f"Missing clips: {len(missing)} | Invalid clips/issues: {len(errors)}")
    if missing:
        print("\nPENDING — missing recordings:")
        for item in missing:
            print(f" - {item}")
    if errors:
        print("\nFAILED — fix these issues:")
        for item in errors:
            print(f" - {item}")
    if errors or (args.strict and missing):
        print("\nRESULT: FAILED")
        return 1
    if missing:
        print("\nRESULT: SOURCE PACKAGE VALID; AUDIO GENERATION IS STILL PENDING.")
        print("Use --strict for a release gate that requires all 96 WAV files.")
    else:
        print("\nRESULT: ALL VOICE WAV FILES PASSED TECHNICAL VALIDATION.")
        print("Human listening, pronunciation approval, and subtitle retiming are still required.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
