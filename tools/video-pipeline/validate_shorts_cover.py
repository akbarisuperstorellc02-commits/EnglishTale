#!/usr/bin/env python3
"""Validate the generated vertical Shorts cover PNG."""
from __future__ import annotations
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PNG = ROOT / "build" / "episode-001-shorts-cover.png"
EXPECTED = (2160, 3840)
LIMIT = 50 * 1024 * 1024

def main() -> int:
    if not PNG.is_file():
        print(f"Shorts cover missing: {PNG}")
        return 1
    data = PNG.read_bytes()
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        print("Shorts cover is not a valid PNG.")
        return 1
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != EXPECTED:
        print(f"Wrong Shorts cover dimensions: {width}x{height}; expected {EXPECTED[0]}x{EXPECTED[1]}.")
        return 1
    if len(data) > LIMIT:
        print(f"Shorts cover exceeds desktop upload limit: {len(data)} bytes.")
        return 1
    print(f"SHORTS COVER VALID: {width}x{height}, {len(data):,} bytes.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
