#!/usr/bin/env python3
"""Generate reviewed per-cue English and Afghan Dari WAV clips with Gemini TTS.

Set GEMINI_API_KEY in the environment. The script never stores or prints the key.
Generated clips are provisional until listened to and checked by a Dari speaker.
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import os
import sys
import time
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "episodes" / "001-english-at-the-airport" / "voice-manifest.json"
VOICE_CONFIG = ROOT / "tools" / "tts" / "voices.json"

ENGLISH_STYLES = {
    "Narrator": "Warm, clear educational storyteller. Natural pacing and crisp pronunciation.",
    "Leo": "Young adult male voice. Curious and slightly nervous at first, then confident. Natural conversational English.",
    "Emma": "Young adult female voice. Friendly, reassuring, upbeat, and clear.",
    "Airport Agent": "Professional airport employee. Polite, calm, and concise.",
    "Security Officer": "Professional security officer. Neutral, clear, and concise.",
    "Ollie": "Cheerful, playful guide character. Bright energy, clear diction, never shrill.",
}
DARI_STYLE = (
    "Speak naturally in Afghan Dari as used in Kabul, Afghanistan, not Iranian Persian. "
    "Use a warm, clear educational narration style, measured pace, and natural Dari pronunciation."
)

def load_audio(response) -> bytes:
    audio = getattr(response, "output_audio", None)
    encoded = getattr(audio, "data", None) if audio is not None else None
    if not encoded:
        raise RuntimeError("Gemini response did not contain output_audio.data.")
    return base64.b64decode(encoded)

def validate_wav(data: bytes) -> None:
    with wave.open(io.BytesIO(data), "rb") as wf:
        if wf.getnchannels() < 1 or wf.getframerate() < 8000 or wf.getnframes() == 0:
            raise ValueError("Generated WAV is empty or has invalid audio parameters.")

def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Episode 001 voice clips with Gemini TTS.")
    parser.add_argument("--language", choices=("en", "fa", "both"), default="both")
    parser.add_argument("--limit", type=int, default=0, help="Generate only the first N cues per language (useful for auditioning).")
    parser.add_argument("--start-id", type=int, default=1, help="First cue ID to process.")
    parser.add_argument("--delay", type=float, default=1.0, help="Seconds to wait between API calls.")
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--model", default=None, help="Override the model in tools/tts/voices.json.")
    args = parser.parse_args()

    if args.delay < 0 or args.retries < 1:
        raise SystemExit("--delay must be >= 0 and --retries must be >= 1.")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    settings = json.loads(VOICE_CONFIG.read_text(encoding="utf-8"))
    model = args.model or settings["model"]
    selected = [c for c in manifest["cues"] if int(c["id"]) >= args.start_id]
    if args.limit:
        selected = selected[:args.limit]
    languages = ("en", "fa") if args.language == "both" else (args.language,)
    if args.dry_run:
        for lang in languages:
            key = "english_file" if lang == "en" else "dari_file"
            for cue in selected:
                print(f"{lang} | cue {cue['id']:03d} | {cue[key]}")
        print(f"Dry run only. {len(selected) * len(languages)} clip(s) selected; no API request sent.")
        return 0

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("GEMINI_API_KEY is not set. Add it to your local environment; never commit it to GitHub.")

    try:
        from google import genai
    except ImportError:
        raise SystemExit("Missing dependency. Install with: python -m pip install -r tools/tts/requirements.txt")

    client = genai.Client(api_key=api_key)
    completed = skipped = 0
    for lang in languages:
        for cue in selected:
            file_key = "english_file" if lang == "en" else "dari_file"
            output = ROOT / cue[file_key]
            if output.exists() and not args.overwrite:
                print(f"SKIP existing: {output.relative_to(ROOT)}")
                skipped += 1
                continue
            output.parent.mkdir(parents=True, exist_ok=True)
            if lang == "en":
                role = cue["role"]
                voice = settings["english_voices"].get(role, settings["english_voices"]["Narrator"])
                style = ENGLISH_STYLES.get(role, ENGLISH_STYLES["Narrator"])
                text = cue["english_text"]
            else:
                voice = settings["dari_voice"]
                style = DARI_STYLE
                text = cue["dari_text"]

            request_input = [{
                "type": "user_input",
                "content": [{
                    "type": "text",
                    "text": text,
                    "annotations": [{"type": "speech_metadata", "style": style}],
                }],
            }]
            last_error = None
            for attempt in range(1, args.retries + 1):
                try:
                    response = client.interactions.create(
                        model=model,
                        input=request_input,
                        response_format={"type": "audio", "mime_type": "audio/wav"},
                        generation_config={"speech_config": [{"voice": voice}]},
                    )
                    audio = load_audio(response)
                    validate_wav(audio)
                    temp = output.with_suffix(output.suffix + ".part")
                    temp.write_bytes(audio)
                    temp.replace(output)
                    completed += 1
                    print(f"OK {lang} cue {int(cue['id']):03d}: {output.relative_to(ROOT)}")
                    last_error = None
                    break
                except Exception as exc:
                    last_error = exc
                    if attempt < args.retries:
                        wait = min(2 ** (attempt - 1) * 2, 20)
                        print(f"Retry {attempt}/{args.retries} for cue {cue['id']} ({lang}) after error: {exc}", file=sys.stderr)
                        time.sleep(wait)
            if last_error is not None:
                print(f"FAILED {lang} cue {cue['id']}: {last_error}", file=sys.stderr)
                print("Completed clips are kept. Re-run the same command to resume; existing clips are skipped.", file=sys.stderr)
                return 2
            if args.delay:
                time.sleep(args.delay)

    print(f"\nFinished. Generated: {completed}; skipped existing: {skipped}.")
    print("Listen to every clip and confirm pronunciation, voice consistency, and timing before assembly.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
