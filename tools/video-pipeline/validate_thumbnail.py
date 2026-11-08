#!/usr/bin/env python3
"""Validate the exported YouTube 4K thumbnail PNG."""
from __future__ import annotations
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PNG = ROOT / "build" / "episode-001-thumbnail.png"
EXPECTED = (3840, 2160)
DESKTOP_LIMIT = 50 * 1024 * 1024

def main() -> int:
    if not PNG.is_file():
        print(f"Thumbnail file missing: {PNG}")
        return 1
    data = PNG.read_bytes()
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        print("Thumbnail is not a valid PNG file.")
        return 1
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != EXPECTED:
        print(f"Wrong thumbnail dimensions: {width}x{height}; expected {EXPECTED[0]}x{EXPECTED[1]}.")
        return 1
    if len(data) > DESKTOP_LIMIT:
        print(f"Thumbnail is too large for YouTube desktop upload: {len(data)} bytes.")
        return 1
    mobile_note = "within 2 MB mobile limit" if len(data) <= 2 * 1024 * 1024 else "desktop upload required (over 2 MB mobile limit)"
    print(f"THUMBNAIL VALID: {width}x{height}, {len(data):,} bytes; {mobile_note}.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
