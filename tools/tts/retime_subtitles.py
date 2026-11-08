#!/usr/bin/env python3
"""Retiming helper: derive provisional subtitle cue ends from approved WAV durations.

This uses per-cue WAV file duration, not speech recognition or phoneme alignment.
It improves cue boundaries but still requires human listening and final review.
"""
from __future__ import annotations

import argparse
import json
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "episodes/001-english-at-the-airport/voice-manifest.json"
DEFAULT_INPUT = ROOT / "build/audio/episode-001/en"
DEFAULT_EN = ROOT / "build/subtitles/episode-001-en-retimed.srt"
DEFAULT_FA = ROOT / "build/subtitles/episode-001-fa-retimed.srt"


def to_ms(value: str) -> int:
    hours, minutes, tail = value.split(":")
    seconds, millis = tail.split(",")
    return (((int(hours) * 60 + int(minutes)) * 60) + int(seconds)) * 1000 + int(millis)


def stamp(value: int) -> str:
    hours, rem = divmod(value, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    seconds, millis = divmod(rem, 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as wav:
        if wav.getnframes() <= 0 or wav.getframerate() <= 0:
            raise ValueError("empty WAV")
        if wav.getsampwidth() != 2 or wav.getcomptype() != "NONE":
            raise ValueError("expected uncompressed 16-bit PCM WAV")
        return wav.getnframes() / wav.getframerate()


def write_srt(path: Path, cues: list[dict], language: str) -> None:
    text_key = "english_text" if language == "en" else "dari_text"
    blocks = []
    for index, cue in enumerate(cues, start=1):
        blocks.append(
            f"{index}\n{stamp(cue['start_ms'])} --> {stamp(cue['end_ms'])}\n{cue[text_key].strip()}"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--english-output", type=Path, default=DEFAULT_EN)
    parser.add_argument("--dari-output", type=Path, default=DEFAULT_FA)
    parser.add_argument("--padding-ms", type=int, default=250,
                        help="small reading tail after each WAV cue")
    args = parser.parse_args()
    if args.padding_ms < 0 or args.padding_ms > 1000:
        parser.error("--padding-ms must be between 0 and 1000")

    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        source_cues = manifest["cues"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"ERROR: cannot load voice manifest: {exc}")
        return 2
    if len(source_cues) != 48:
        print(f"ERROR: expected 48 cues, found {len(source_cues)}")
        return 2

    cues = []
    for index, source in enumerate(source_cues):
        cue_id = int(source["id"])
        start = to_ms(source["start"])
        path = args.input / f"{cue_id:03d}.wav"
        if not path.is_file():
            print(f"MISSING: {path}")
            return 1
        try:
            duration_ms = round(wav_duration(path) * 1000)
        except (OSError, wave.Error, ValueError) as exc:
            print(f"INVALID cue {cue_id}: {exc}")
            return 1
        end = start + duration_ms + args.padding_ms
        next_start = to_ms(source_cues[index + 1]["start"]) if index + 1 < len(source_cues) else int(manifest.get("target_duration_seconds", 420)) * 1000
        if end > next_start:
            print(f"OVERLAP cue {cue_id}: WAV duration plus reading tail reaches {end} ms; next cue starts at {next_start} ms")
            return 1
        if not source.get("english_text", "").strip() or not source.get("dari_text", "").strip():
            print(f"INVALID cue {cue_id}: missing English or Dari subtitle text")
            return 1
        cues.append({"start_ms": start, "end_ms": end,
                     "english_text": source["english_text"], "dari_text": source["dari_text"]})

    write_srt(args.english_output, cues, "en")
    write_srt(args.dari_output, cues, "fa")
    print("SUBTITLE RETIMING COMPLETE")
    print(f"Retimed cue boundaries: {len(cues)}/48")
    print(f"English SRT: {args.english_output}")
    print(f"Afghan Dari SRT: {args.dari_output}")
    print("Method: measured WAV file duration plus reading tail; human listening and final caption review remain mandatory.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
