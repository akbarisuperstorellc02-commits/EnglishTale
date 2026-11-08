#!/usr/bin/env python3
"""Deprecated compatibility entry point for the former bilingual audio workflow.

Current approved delivery is British English audio plus Afghan Dari subtitles.
Use tools/tts/build_english_track.py instead. No Dari WAV track is produced.
"""
import sys


def main() -> int:
    print("DEPRECATED: the bilingual audio assembler is no longer part of EnglishTale.")
    print("Current policy: British English WAV audio + Afghan Dari SRT subtitles only.")
    print("Run: python tools/tts/build_english_track.py")
    return 2


if __name__ == "__main__":
    sys.exit(main())
