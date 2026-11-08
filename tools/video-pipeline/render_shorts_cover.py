#!/usr/bin/env python3
"""Export the Episode 001 Shorts cover at YouTube's recommended 2160x3840."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "assets" / "thumbnails" / "episode-001-shorts-cover.svg"
OUTPUT = ROOT / "build" / "episode-001-shorts-cover.png"
WIDTH, HEIGHT = 2160, 3840

def main() -> int:
    try:
        import cairosvg
    except ImportError:
        print("CairoSVG is required: python -m pip install -r tools/video-pipeline/requirements.txt")
        return 2
    if not SOURCE.is_file():
        print(f"Shorts cover SVG missing: {SOURCE}")
        return 1
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    cairosvg.svg2png(url=str(SOURCE), write_to=str(OUTPUT), output_width=WIDTH, output_height=HEIGHT)
    size = OUTPUT.stat().st_size
    print(f"Shorts cover exported: {OUTPUT} ({WIDTH}x{HEIGHT}, {size:,} bytes)")
    if size > 50 * 1024 * 1024:
        print("File exceeds YouTube's 50 MB desktop upload limit.")
        return 1
    if size > 10 * 1024 * 1024:
        print("Note: file exceeds the 10 MB mobile podcast limit; upload from desktop.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
