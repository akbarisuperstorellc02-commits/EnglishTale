#!/usr/bin/env python3
"""Check the generated YouTube thumbnail PNG signature and dimensions."""
from __future__ import annotations
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PNG = ROOT / "build" / "episode-001-thumbnail.png"

def main() -> int:
    if not PNG.is_file():
        print(f"Thumbnail file missing: {PNG}")
        return 1
    data = PNG.read_bytes()
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        print("Thumbnail is not a valid PNG file.")
        return 1
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1280, 720):
        print(f"Wrong thumbnail dimensions: {width}x{height}; expected 1280x720.")
        return 1
    print(f"THUMBNAIL VALID: {width}x{height}, {len(data)} bytes")
    return 0

if __name__ == "__main__":
    sys.exit(main())
