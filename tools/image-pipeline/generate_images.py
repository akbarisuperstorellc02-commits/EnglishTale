#!/usr/bin/env python3
"""Generate cinematic 3D Episode 001 scene artwork with the Gemini Developer API."""
from __future__ import annotations

import argparse
import base64
import json
import os
import random
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "episodes/001-english-at-the-airport/image-manifest.json"

CHARACTER_DESCRIPTIONS = {
    "leo": "Leo: fictional 19-year-old young man, tousled medium-brown hair, expressive brown eyes, vivid blue hoodie, dark blue jeans, white sneakers. Keep this exact face, hairstyle, age, outfit and proportions.",
    "emma": "Emma: fictional 19-year-old young woman, shoulder-length brown hair, expressive brown eyes, warm pink sweater, dark jeans, white sneakers. Keep this exact face, hairstyle, age, outfit and proportions.",
    "ollie": "Ollie: same small cute brown owl mascot, cream face and chest, large expressive eyes, round glasses, navy scarf with a tiny gold accent. Clearly an owl, never a dog or another animal.",
}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene", action="append", help="Scene ID; repeat to select multiple. Default: all.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--delay", type=float, default=2.0)
    parser.add_argument("--retries", type=int, default=4)
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    scenes = manifest["scenes"]
    if args.scene:
        wanted = set(args.scene)
        scenes = [s for s in scenes if s["id"] in wanted]
        missing = wanted - {s["id"] for s in scenes}
        if missing:
            print("Unknown scene ID(s): " + ", ".join(sorted(missing)), file=sys.stderr)
            return 2

    out_dir = ROOT / manifest["output_dir"]
    if args.dry_run:
        print(f"DRY RUN: {len(scenes)} scene(s), model={manifest['model']}, ratio={manifest['aspect_ratio']}")
        for scene in scenes:
            print(f"  {scene['id']} -> {scene['file']} (3D character descriptions: {', '.join(scene['refs']) or 'environment'})")
        return 0

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        print("GEMINI_API_KEY is missing. Add it as a GitHub Actions secret.", file=sys.stderr)
        return 2

    out_dir.mkdir(parents=True, exist_ok=True)
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{manifest['model']}:generateContent"
    session = requests.Session()
    session.headers.update({"x-goog-api-key": api_key, "Content-Type": "application/json"})

    for index, scene in enumerate(scenes):
        target = out_dir / scene["file"]
        if target.exists() and target.stat().st_size > 0:
            print(f"SKIP existing: {scene['id']}")
            continue

        character_notes = [CHARACTER_DESCRIPTIONS[name] for name in scene["refs"]]
        prompt = manifest["style"] + "\n\nCharacter continuity notes:\n" + "\n".join(character_notes)
        prompt += "\n\nScene direction: " + scene["prompt"]
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseModalities": ["IMAGE"],
                "imageConfig": {
                    "aspectRatio": manifest["aspect_ratio"],
                    "imageSize": manifest["image_size"]
                }
            }
        }

        for attempt in range(args.retries + 1):
            try:
                response = session.post(endpoint, json=payload, timeout=240)
                if response.status_code in (429, 500, 502, 503, 504) and attempt < args.retries:
                    wait = min(60, (2 ** attempt) + random.random() * 2)
                    print(f"Temporary API response {response.status_code}; retrying in {wait:.1f}s")
                    time.sleep(wait)
                    continue
                if not response.ok:
                    try:
                        err = response.json().get("error", {})
                        message = err.get("message", "API request failed")
                    except Exception:
                        message = "API request failed"
                    print(f"API error for {scene['id']}: HTTP {response.status_code}: {message}", file=sys.stderr)
                    return 1

                data = response.json()
                candidates = data.get("candidates", [])
                image_part = None
                for candidate in candidates:
                    for part in candidate.get("content", {}).get("parts", []):
                        inline = part.get("inlineData") or part.get("inline_data")
                        if inline and inline.get("data"):
                            image_part = inline
                            break
                    if image_part:
                        break
                if not image_part:
                    print(f"No image returned for {scene['id']}; finish reason: " +
                          str(candidates[0].get("finishReason") if candidates else "no candidates"), file=sys.stderr)
                    return 1

                image_bytes = base64.b64decode(image_part["data"])
                if len(image_bytes) < 10_000:
                    print(f"Image response unexpectedly small for {scene['id']}", file=sys.stderr)
                    return 1
                target.write_bytes(image_bytes)
                print(f"GENERATED: {scene['id']} ({len(image_bytes):,} bytes)")
                break
            except requests.RequestException as exc:
                if attempt >= args.retries:
                    print(f"Network failure for {scene['id']}: {exc}", file=sys.stderr)
                    return 1
                wait = min(60, 2 ** attempt)
                print(f"Network error; retrying in {wait}s")
                time.sleep(wait)

        if index < len(scenes) - 1:
            time.sleep(max(0, args.delay))

    print(f"Completed {len(scenes)} selected scene(s). Output: {out_dir.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
