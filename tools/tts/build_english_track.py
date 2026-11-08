#!/usr/bin/env python3
"""Validate and assemble the 48 English-only local TTS clips into a 7-minute WAV."""
from __future__ import annotations

import argparse
import json
import struct
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "episodes/001-english-at-the-airport/voice-manifest.json"
DEFAULT_INPUT = ROOT / "build/audio/episode-001/en"
DEFAULT_OUTPUT = ROOT / "build/audio/episode-001-en.wav"


def ms(value: str) -> int:
    hh, mm, tail = value.split(":")
    ss, millis = tail.split(",")
    return (((int(hh) * 60 + int(mm)) * 60) + int(ss)) * 1000 + int(millis)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--duration", type=int, default=420)
    args = parser.parse_args()

    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cues = manifest["cues"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"ERROR: cannot load voice manifest: {exc}")
        return 2
    if len(cues) != 48:
        print(f"ERROR: expected 48 English cues, found {len(cues)}")
        return 2

    clips = []
    fmt = None
    for cue in cues:
        cue_id = int(cue["id"])
        path = args.input / f"{cue_id:03d}.wav"
        if not path.is_file():
            print(f"MISSING: {path}")
            return 1
        try:
            with wave.open(str(path), "rb") as wav:
                current = (wav.getnchannels(), wav.getsampwidth(), wav.getframerate(), wav.getcomptype())
                if current[0] != 1 or current[1] != 2 or current[3] != "NONE":
                    raise ValueError(f"expected mono 16-bit PCM WAV, got {current}")
                if fmt is None:
                    fmt = current
                elif current != fmt:
                    raise ValueError(f"inconsistent WAV format: {path} has {current}, expected {fmt}")
                frames = wav.getnframes()
                audio = wav.readframes(frames)
                if frames <= 0 or max((abs(v) for (v,) in struct.iter_unpack("<h", audio)), default=0) < 32:
                    raise ValueError(f"empty or silent WAV: {path}")
        except (OSError, wave.Error, ValueError, struct.error) as exc:
            print(f"INVALID cue {cue_id}: {exc}")
            return 1
        start = ms(cue["start"])
        end = ms(cue["end"])
        if end <= start:
            print(f"INVALID cue {cue_id}: non-positive timing slot")
            return 1
        clips.append((cue_id, start, end, frames, audio))

    sample_rate = fmt[2]
    total_frames = args.duration * sample_rate
    output = bytearray(total_frames * 2)
    for cue_id, start_ms, end_ms, frames, audio in clips:
        start_frame = round(start_ms * sample_rate / 1000)
        slot_frames = round((end_ms - start_ms) * sample_rate / 1000)
        if frames > slot_frames:
            print(f"OVERFLOW cue {cue_id}: {frames/sample_rate:.2f}s exceeds {slot_frames/sample_rate:.2f}s slot")
            return 1
        stop = start_frame + frames
        if stop > total_frames:
            print(f"OVERFLOW cue {cue_id}: clip extends beyond episode duration")
            return 1
        byte_start = start_frame * 2
        output[byte_start:byte_start + len(audio)] = audio

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(args.output), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(output)
    print("ENGLISHTALE ENGLISH TRACK")
    print(f"PASS: {len(clips)}/48 cues | {sample_rate} Hz mono PCM | {args.duration}s")
    print(f"Output: {args.output}")
    print("Afghan Dari remains subtitles only; no Dari narration track was created.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
