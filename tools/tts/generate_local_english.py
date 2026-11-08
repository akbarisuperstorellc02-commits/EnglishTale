#!/usr/bin/env python3
"""Generate English-only episode dialogue locally with Piper TTS (no cloud API).

Install Piper TTS locally, obtain a British English Piper voice model, and
review that model's own license before commercial publication. Voice model
weights are intentionally not bundled in this repository.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "episodes/001-english-at-the-airport/voice-manifest.json"
DEFAULT_OUT = ROOT / "build/audio/episode-001/en"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True,
                        help="Path to a licensed British English Piper .onnx voice model")
    parser.add_argument("--config", type=Path,
                        help="Optional matching Piper .onnx.json config file")
    parser.add_argument("--voices-json", type=Path,
                        help="Optional JSON mapping role names to model paths; unmapped roles use --model")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--piper", default="piper", help="Piper CLI executable")
    parser.add_argument("--start-id", type=int, default=1)
    parser.add_argument("--limit", type=int, default=0, help="0 means all cues")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    executable = shutil.which(args.piper)
    if not executable and not args.dry_run:
        print("ERROR: Piper CLI not found. Install piper-tts in the local Python environment.")
        return 2
    if not args.model.is_file():
        print(f"ERROR: voice model does not exist: {args.model}")
        return 2

    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cues = manifest["cues"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"ERROR: cannot read voice manifest: {exc}")
        return 2

    role_models: dict[str, Path] = {}
    if args.voices_json:
        try:
            raw = json.loads(args.voices_json.read_text(encoding="utf-8"))
            role_models = {role: Path(path) for role, path in raw.items()}
        except (OSError, json.JSONDecodeError, AttributeError) as exc:
            print(f"ERROR: invalid role-to-model JSON: {exc}")
            return 2

    selected = [c for c in cues if int(c.get("id", 0)) >= args.start_id]
    if args.limit > 0:
        selected = selected[:args.limit]
    if not selected:
        print("No cues selected.")
        return 0

    args.output.mkdir(parents=True, exist_ok=True)
    generated = skipped = failed = 0
    for cue in selected:
        cue_id = int(cue["id"])
        role = str(cue.get("role", "Narrator"))
        text = str(cue.get("english_text", "")).replace("\n", " ").strip()
        destination = args.output / f"{cue_id:03d}.wav"
        model = role_models.get(role, args.model)
        if not model.is_file():
            print(f"FAIL cue {cue_id}: model missing for role {role}: {model}")
            failed += 1
            continue
        if destination.exists() and not args.overwrite:
            skipped += 1
            continue
        command = [executable or args.piper, "--model", str(model), "--output_file", str(destination)]
        config = args.config if model == args.model else Path(str(model) + ".json")
        if config and config.is_file():
            command.extend(["--config", str(config)])
        if args.dry_run:
            print(f"DRY RUN cue {cue_id:02d} [{role}] -> {destination.name} | model={model.name}")
            continue
        try:
            subprocess.run(command, input=text + "\n", text=True, check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            with wave.open(str(destination), "rb") as wav:
                if wav.getnframes() <= 0 or wav.getnchannels() not in (1, 2):
                    raise ValueError("empty or unsupported WAV output")
            generated += 1
            print(f"OK cue {cue_id:02d} [{role}] -> {destination.name}")
        except (subprocess.CalledProcessError, OSError, wave.Error, ValueError) as exc:
            destination.unlink(missing_ok=True)
            detail = getattr(exc, "stderr", "") or str(exc)
            print(f"FAIL cue {cue_id:02d}: {detail}")
            failed += 1

    print("\nLOCAL ENGLISH TTS SUMMARY")
    print(f"Selected: {len(selected)} | generated: {generated} | skipped: {skipped} | failed: {failed}")
    print("Dari narration is intentionally disabled; use the Afghan Dari SRT subtitle track.")
    print("Retiming subtitles against the final WAV durations remains mandatory.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
