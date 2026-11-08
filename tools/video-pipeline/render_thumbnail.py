#!/usr/bin/env python3
"""Export the Episode 001 SVG thumbnail to a YouTube-ready 1280x720 PNG."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "assets" / "thumbnails" / "episode-001-thumbnail.svg"
OUTPUT = ROOT / "build" / "episode-001-thumbnail.png"

def main() -> int:
    try:
        import cairosvg
    except ImportError:
        print("CairoSVG is required: python -m pip install -r tools/video-pipeline/requirements.txt")
        return 2
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    cairosvg.svg2png(url=str(SOURCE), write_to=str(OUTPUT), output_width=1280, output_height=720)
    print(f"Thumbnail exported: {OUTPUT}")
    print("Review at phone size and confirm all text remains readable before upload.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
