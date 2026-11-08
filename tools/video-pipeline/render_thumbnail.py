#!/usr/bin/env python3
"""Export the Episode 001 SVG thumbnail at YouTube's recommended 4K 16:9 size."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "assets" / "thumbnails" / "episode-001-thumbnail.svg"
OUTPUT = ROOT / "build" / "episode-001-thumbnail.png"
WIDTH, HEIGHT = 3840, 2160

def main() -> int:
    try:
        import cairosvg
    except ImportError:
        print("CairoSVG is required: python -m pip install -r tools/video-pipeline/requirements.txt")
        return 2
    if not SOURCE.is_file():
        print(f"Thumbnail SVG missing: {SOURCE}")
        return 1
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    cairosvg.svg2png(url=str(SOURCE), write_to=str(OUTPUT), output_width=WIDTH, output_height=HEIGHT)
    size = OUTPUT.stat().st_size
    print(f"Thumbnail exported: {OUTPUT} ({WIDTH}x{HEIGHT}, {size:,} bytes)")
    print("Review at phone size; confirm all text remains readable before upload.")
    if size > 50 * 1024 * 1024:
        print("Warning: file exceeds YouTube's 50 MB desktop upload limit.")
        return 1
    if size > 2 * 1024 * 1024:
        print("Note: file exceeds the 2 MB mobile upload limit; upload from YouTube Studio on desktop.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
