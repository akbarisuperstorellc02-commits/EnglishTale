#!/usr/bin/env python3
"""Assemble reviewed per-cue WAV files into aligned English and Dari tracks."""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EP = ROOT / "episodes" / "001-english-at-the-airport"
MANIFEST = EP / "voice-manifest.json"
OUT = ROOT / "build" / "audio"

def tool(name: str) -> str:
    found = shutil.which(name)
    if not found:
        raise SystemExit(f"Missing required executable: {name}")
    return found

def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)

def duration(ffprobe: str, path: Path) -> float:
    p = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True
    )
    return float(p.stdout.strip())

def ms(value: str) -> int:
    h, m, tail = value.split(":")
    s, milli = tail.split(",")
    return ((int(h) * 60 + int(m)) * 60 + int(s)) * 1000 + int(milli)

def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble EnglishTale Episode 001 voice tracks.")
    parser.add_argument("--language", choices=("en", "fa", "both"), default="both")
    parser.add_argument("--output-dir", type=Path, default=OUT)
    args = parser.parse_args()

    ffmpeg, ffprobe = tool("ffmpeg"), tool("ffprobe")
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cues = data["cues"]
    languages = ("en", "fa") if args.language == "both" else (args.language,)

    # Validate the entire requested input set before writing any output.
    missing, too_long = [], []
    for lang in languages:
        key = "english_file" if lang == "en" else "dari_file"
        for cue in cues:
            clip = ROOT / cue[key]
            if not clip.is_file():
                missing.append(str(clip.relative_to(ROOT)))
                continue
            slot = (ms(cue["end"]) - ms(cue["start"])) / 1000.0
            actual = duration(ffprobe, clip)
            if actual > slot + 0.12:
                too_long.append(f"cue {cue['id']} ({lang}): {actual:.2f}s audio in {slot:.2f}s slot")

    if missing:
        print("Missing voice clips. Generate and review all requested clips first:")
        for item in missing:
            print(" -", item)
        return 2
    if too_long:
        print("Some voice clips exceed their provisional subtitle slots. Retiming is required:")
        for item in too_long:
            print(" -", item)
        return 3

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="englishtale-audio-") as temp:
        tempdir = Path(temp)
        for lang in languages:
            key = "english_file" if lang == "en" else "dari_file"
            parts = []
            for cue in cues:
                source = ROOT / cue[key]
                slot = (ms(cue["end"]) - ms(cue["start"])) / 1000.0
                part = tempdir / f"{lang}-{int(cue['id']):03d}.wav"
                filter_chain = f"apad=pad_dur={slot:.3f},atrim=duration={slot:.3f}"
                run([ffmpeg, "-y", "-i", str(source), "-vn", "-af", filter_chain,
                     "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(part)])
                parts.append(part)
            concat_file = tempdir / f"{lang}-concat.txt"
            concat_file.write_text(
                "".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8"
            )
            output = args.output_dir / ("episode-001-en.wav" if lang == "en" else "episode-001-fa.wav")
            run([ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file),
                 "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(output)])
            print(f"Created {output} ({duration(ffprobe, output):.2f}s)")

    print("Audio tracks assembled. Listen through and retime captions before final video export.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
