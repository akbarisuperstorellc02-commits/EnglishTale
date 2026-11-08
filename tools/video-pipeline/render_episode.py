#!/usr/bin/env python3
"""Build a silent visual review cut from EnglishTale's coded SVG scene plates.

Requires FFmpeg/ffprobe on PATH and CairoSVG:
    python -m pip install -r tools/video-pipeline/requirements.txt

This is a review renderer, not a finished animation system. It applies gentle
camera motion to scene plates. Final character animation, recorded voices,
waveform-accurate captions, sound design, and final QC remain separate steps.
"""
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
SCENES = ROOT / "assets" / "scenes"
SHOT_FILE = EP / "render-shotlist.json"
DEFAULT_OUT = ROOT / "build" / "episode-001-review.mp4"

def run(cmd: list[str]) -> None:
    print("+", subprocess.list2cmdline(cmd))
    subprocess.run(cmd, check=True)

def require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise SystemExit(f"Required executable not found on PATH: {name}")
    return path

def probe_duration(path: Path) -> float:
    result = subprocess.run(
        [require_tool("ffprobe"), "-v", "error", "-show_entries",
         "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, capture_output=True, text=True
    )
    return float(result.stdout.strip())

def main() -> int:
    parser = argparse.ArgumentParser(description="Render an EnglishTale Episode 001 review cut.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--audio", type=Path, help="Optional reviewed narration/dialogue mix.")
    parser.add_argument("--no-motion", action="store_true", help="Use static scene plates.")
    args = parser.parse_args()

    ffmpeg = require_tool("ffmpeg")
    require_tool("ffprobe")
    try:
        import cairosvg
    except ImportError:
        raise SystemExit("CairoSVG is missing. Run: python -m pip install -r tools/video-pipeline/requirements.txt")

    shots = json.loads(SHOT_FILE.read_text(encoding="utf-8"))
    if not shots:
        raise SystemExit("Shot list is empty.")
    total = sum(int(s["duration"]) for s in shots)
    if total != 420:
        raise SystemExit(f"Expected a 420-second (07:00) timeline; shot list totals {total} seconds.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="englishtale-") as temp:
        tempdir = Path(temp)
        rendered: list[Path] = []
        for index, shot in enumerate(shots, start=1):
            scene = SCENES / shot["scene"]
            if not scene.is_file():
                raise SystemExit(f"Missing scene asset: {scene}")
            png = tempdir / f"scene-{index:02d}.png"
            clip = tempdir / f"shot-{index:02d}.mp4"
            cairosvg.svg2png(url=str(scene), write_to=str(png),
                             output_width=args.width, output_height=args.height)
            frames = int(shot["duration"]) * args.fps
            vf = f"scale={args.width}:{args.height},format=yuv420p"
            if not args.no_motion:
                vf = (f"zoompan=z='min(zoom+0.00035,1.045)':d=1:"
                      f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                      f"s={args.width}x{args.height}:fps={args.fps},format=yuv420p")
            run([ffmpeg, "-y", "-loop", "1", "-framerate", str(args.fps),
                 "-i", str(png), "-vf", vf, "-frames:v", str(frames),
                 "-an", "-c:v", "libx264", "-preset", "veryfast",
                 "-crf", "24", "-pix_fmt", "yuv420p", str(clip)])
            rendered.append(clip)
            print(f"Rendered shot {index}/{len(shots)}: {shot['label']}")

        concat = tempdir / "concat.txt"
        concat.write_text("".join(f"file '{p.as_posix()}'\n" for p in rendered), encoding="utf-8")
        silent = tempdir / "silent.mp4"
        run([ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
             "-c", "copy", "-movflags", "+faststart", str(silent)])

        if args.audio:
            audio = args.audio.resolve()
            if not audio.is_file():
                raise SystemExit(f"Audio file not found: {audio}")
            duration = probe_duration(audio)
            if duration < total - 1.0:
                raise SystemExit(f"Audio is only {duration:.1f}s; expected about {total}s. Refusing to truncate the video.")
            run([ffmpeg, "-y", "-i", str(silent), "-i", str(audio),
                 "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
                 "-c:a", "aac", "-b:a", "192k", "-t", str(total),
                 "-movflags", "+faststart", str(args.output)])
        else:
            shutil.copy2(silent, args.output)

    print(f"\nReview render created: {args.output}")
    print("This file uses scene plates only. It is not the final animated episode.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
