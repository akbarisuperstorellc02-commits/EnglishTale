#!/usr/bin/env python3
"""Download the pinned British English VCTK Piper voice and verify its files.

The VCTK model contains 109 British English speakers. Its model card lists
the VCTK dataset under CC BY 4.0; attribution is required for commercial use.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "models/piper/en_GB-vctk-medium"
BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/vctk/medium/"
FILES = {
    "en_GB-vctk-medium.onnx": {
        "md5": "573025290fdc68812543b7438ace0c29",
        "size": 76952753,
    },
    "en_GB-vctk-medium.onnx.json": {
        "md5": "68e82dee4c9a723e804f9fc0b14f1802",
        "size": 6637,
    },
    "MODEL_CARD": {
        "md5": "b88a963e3bee27bc4fff84563f1be388",
        "size": 326,
    },
}


def digest(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download(name: str, spec: dict, folder: Path) -> Path:
    destination = folder / name
    if destination.is_file() and destination.stat().st_size == spec["size"] and digest(destination) == spec["md5"]:
        print(f"VERIFIED existing {name}")
        return destination
    temporary = destination.with_suffix(destination.suffix + ".download")
    url = BASE + name
    request = urllib.request.Request(url, headers={"User-Agent": "EnglishTale-local-voice-setup/1.0"})
    print(f"Downloading {name} ...")
    with urllib.request.urlopen(request, timeout=90) as response, temporary.open("wb") as out:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)
    actual_size = temporary.stat().st_size
    actual_md5 = digest(temporary)
    if actual_size != spec["size"] or actual_md5 != spec["md5"]:
        temporary.unlink(missing_ok=True)
        raise ValueError(f"Integrity check failed for {name}: size={actual_size}, md5={actual_md5}")
    temporary.replace(destination)
    print(f"VERIFIED {name} ({actual_size:,} bytes)")
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    try:
        for name, spec in FILES.items():
            download(name, spec, args.output_dir)
        card = (args.output_dir / "MODEL_CARD").read_text(encoding="utf-8")
        if "creativecommons.org/licenses/by/4.0/" not in card:
            raise ValueError("Pinned model card does not declare the expected CC BY 4.0 dataset license.")
        (args.output_dir / "ATTRIBUTION.txt").write_text(
            "Voice model: en_GB-vctk-medium (Piper Voices, v1.0.0)\n"
            "Dataset: CSTR VCTK Corpus, University of Edinburgh\n"
            "Dataset license: Creative Commons Attribution 4.0 International (CC BY 4.0)\n"
            "Source/model card: https://huggingface.co/rhasspy/piper-voices/tree/v1.0.0/en/en_GB/vctk/medium\n"
            "Attribution: VCTK Corpus by CSTR, University of Edinburgh. See the model card and dataset terms.\n",
            encoding="utf-8",
        )
    except (OSError, ValueError, urllib.error.URLError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print(f"READY: {args.output_dir / 'en_GB-vctk-medium.onnx'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
