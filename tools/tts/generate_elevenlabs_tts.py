#!/usr/bin/env python3
"""Generate per-cue WAV files through the ElevenLabs TTS API.

Requires ELEVENLABS_API_KEY and FFmpeg. Voice IDs must be selected by the owner
from their own ElevenLabs account and saved in tools/tts/elevenlabs-voices.json.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "episodes" / "001-english-at-the-airport" / "voice-manifest.json"
CONFIG = ROOT / "tools" / "tts" / "elevenlabs-voices.json"
API = "https://api.elevenlabs.io"

def request(method: str, url: str, key: str, payload=None) -> bytes:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"xi-api-key": key, "Accept": "application/json" if method == "GET" else "audio/mpeg",
                 "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        return response.read()

def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Episode 001 voice clips with ElevenLabs.")
    parser.add_argument("--language", choices=("en", "fa", "both"), default="both")
    parser.add_argument("--cue-ids", type=str, default="", help="Comma-separated cue IDs for a representative audition set.")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--start-id", type=int, default=1)
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--list-voices", action="store_true", help="List voices available to this API key.")
    args = parser.parse_args()

    key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not args.dry_run and not key:
        raise SystemExit("ELEVENLABS_API_KEY is not set. Never save the key in this repository.")

    if args.list_voices:
        raw = request("GET", API + "/v2/voices?page_size=100", key)
        data = json.loads(raw.decode("utf-8"))
        for voice in data.get("voices", []):
            labels = voice.get("labels") or {}
            print(f"{voice.get('name','(unnamed)')} | {voice.get('voice_id','')} | "
                  f"language={labels.get('language','?')} | accent={labels.get('accent','?')} | "
                  f"gender={labels.get('gender','?')} | category={voice.get('category','?')}")
        if data.get("has_more"):
            print("More voices are available; use the ElevenLabs Voice Library to inspect the complete list.")
        return 0

    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    model = config.get("model_id", "eleven_multilingual_v2")
    output_format = config.get("output_format", "mp3_44100_128")
    languages = ("en", "fa") if args.language == "both" else (args.language,)
    if args.cue_ids and args.limit:
        raise SystemExit("Use either --cue-ids or --limit, not both.")
    if args.cue_ids:
        requested_ids = {int(value.strip()) for value in args.cue_ids.split(",") if value.strip()}
        selected = [cue for cue in manifest["cues"] if int(cue["id"]) in requested_ids]
        found_ids = {int(cue["id"]) for cue in selected}
        missing_ids = sorted(requested_ids - found_ids)
        if missing_ids:
            raise SystemExit("Unknown cue IDs: " + ", ".join(map(str, missing_ids)))
    else:
        selected = [cue for cue in manifest["cues"] if int(cue["id"]) >= args.start_id]
        if args.limit:
            selected = selected[:args.limit]

    if args.dry_run:
        count = 0
        for lang in languages:
            key_name = "english_file" if lang == "en" else "dari_file"
            for cue in selected:
                print(f"{lang} | cue {cue['id']:03d} | {cue[key_name]}")
                count += 1
        print(f"Dry run only: {count} clip(s); no API requests sent.")
        return 0

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("FFmpeg is required to convert API MP3 output into the WAV files used by this pipeline.")

    voice_map = config.get("english_voices", {})
    dari_voice = config.get("dari_voice", "")
    missing_roles = [role for role in sorted({c["role"] for c in selected})
                     if not voice_map.get(role)]
    if "en" in languages and missing_roles:
        raise SystemExit("Add ElevenLabs voice IDs for these English roles in tools/tts/elevenlabs-voices.json: " + ", ".join(missing_roles))
    if "fa" in languages and not dari_voice:
        raise SystemExit("Add a Persian/Afghan Dari voice ID to dari_voice in tools/tts/elevenlabs-voices.json.")

    completed = skipped = 0
    for lang in languages:
        for cue in selected:
            file_key = "english_file" if lang == "en" else "dari_file"
            output = ROOT / cue[file_key]
            if output.exists() and not args.overwrite:
                print(f"SKIP existing: {output.relative_to(ROOT)}")
                skipped += 1
                continue
            voice_id = voice_map[cue["role"]] if lang == "en" else dari_voice
            text = cue["english_text"] if lang == "en" else cue["dari_text"]
            url = f"{API}/v1/text-to-speech/{urllib.parse.quote(voice_id, safe='')}?output_format={urllib.parse.quote(output_format)}"
            payload = {
                "text": text,
                "model_id": model,
                "voice_settings": {
                    "stability": 0.45,
                    "similarity_boost": 0.8,
                    "style": 0.25,
                    "use_speaker_boost": True
                }
            }
            output.parent.mkdir(parents=True, exist_ok=True)
            mp3 = output.with_suffix(".elevenlabs.tmp.mp3")
            wav_tmp = output.with_suffix(output.suffix + ".part")
            last_error = None
            for attempt in range(1, args.retries + 1):
                try:
                    audio = request("POST", url, key, payload)
                    if len(audio) < 1000:
                        raise RuntimeError("API returned an unexpectedly small audio response.")
                    mp3.write_bytes(audio)
                    subprocess.run(
                        [ffmpeg, "-y", "-i", str(mp3), "-ar", "24000", "-ac", "1",
                         "-c:a", "pcm_s16le", str(wav_tmp)],
                        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE
                    )
                    if not wav_tmp.is_file() or wav_tmp.stat().st_size < 1000:
                        raise RuntimeError("FFmpeg did not create a valid WAV file.")
                    wav_tmp.replace(output)
                    mp3.unlink(missing_ok=True)
                    completed += 1
                    print(f"OK {lang} cue {int(cue['id']):03d}: {output.relative_to(ROOT)}")
                    last_error = None
                    break
                except Exception as exc:
                    last_error = exc
                    mp3.unlink(missing_ok=True)
                    wav_tmp.unlink(missing_ok=True)
                    if attempt < args.retries:
                        wait = min(2 ** attempt, 20)
                        print(f"Retry {attempt}/{args.retries} for cue {cue['id']} ({lang}): {exc}", file=sys.stderr)
                        time.sleep(wait)
            if last_error is not None:
                print(f"FAILED {lang} cue {cue['id']}: {last_error}", file=sys.stderr)
                print("Completed clips are retained. Re-run to resume; existing clips are skipped.", file=sys.stderr)
                return 2
            if args.delay:
                time.sleep(args.delay)

    print(f"\nFinished. Generated: {completed}; skipped existing: {skipped}.")
    print("Listen to every line and have a native Afghan Dari speaker review the Dari track.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
