#!/usr/bin/env python3
"""Validate Episode 001's production inputs without external dependencies."""
from __future__ import annotations
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EP = ROOT / "episodes" / "001-english-at-the-airport"
SCENES = ROOT / "assets" / "scenes"

def parse_srt(path: Path):
    raw = path.read_text(encoding="utf-8-sig").strip()
    blocks = re.split(r"\n\s*\n", raw)
    cues = []
    for block in blocks:
        lines = block.splitlines()
        if len(lines) < 3 or not lines[0].strip().isdigit():
            raise ValueError(f"Malformed SRT block in {path.name}: {block[:80]!r}")
        match = re.fullmatch(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})", lines[1].strip())
        if not match:
            raise ValueError(f"Invalid timestamp in {path.name}: {lines[1]}")
        cue_text = "\n".join(lines[2:]).strip()
        cues.append((int(lines[0]), match.group(1), match.group(2), cue_text))
    return cues

def to_ms(value: str) -> int:
    h, m, rest = value.split(":")
    s, ms = rest.split(",")
    return ((int(h) * 60 + int(m)) * 60 + int(s)) * 1000 + int(ms)

def main() -> int:
    errors = []
    shot_path = EP / "render-shotlist.json"
    shots = json.loads(shot_path.read_text(encoding="utf-8"))
    if sum(int(s["duration"]) for s in shots) != 420:
        errors.append("Shot durations do not total 420 seconds.")
    if any(int(s.get("duration", 0)) <= 0 for s in shots):
        errors.append("Every shot must have a positive duration.")
    shot_ids = [str(s.get("id", "")) for s in shots]
    if len(shot_ids) != len(set(shot_ids)):
        errors.append("Shot IDs are not unique.")
    for shot in shots:
        if not (SCENES / shot["scene"]).is_file():
            errors.append(f"Missing scene file: {shot['scene']}")
    en = parse_srt(EP / "subtitles-en.srt")
    fa = parse_srt(EP / "subtitles-fa.srt")
    manifest = json.loads((EP / "voice-manifest.json").read_text(encoding="utf-8"))
    manifest_cues = manifest.get("cues", [])
    if int(manifest.get("target_duration_seconds", 0)) != 420:
        errors.append("Voice manifest target duration must be 420 seconds.")
    valid_roles = {"Narrator", "Leo", "Emma", "Airport Agent", "Security Officer", "Ollie"}
    voice_paths = []
    if len(manifest_cues) != len(en):
        errors.append(f"Voice manifest cue count differs from English SRT: {len(manifest_cues)} vs {len(en)}.")
    else:
        for index, cue in enumerate(manifest_cues):
            if cue.get("id") != en[index][0] or cue.get("start") != en[index][1] or cue.get("end") != en[index][2]:
                errors.append(f"Voice manifest timing/ID differs at cue {index + 1}.")
            if cue.get("english_text", "").strip() == "" or cue.get("dari_text", "").strip() == "":
                errors.append(f"Voice manifest cue {index + 1} has an empty language text.")
            if cue.get("role") not in valid_roles:
                errors.append(f"Voice manifest cue {index + 1} has an unknown role: {cue.get('role')}.")
            voice_paths.extend([cue.get("english_file", ""), cue.get("dari_file", "")])
            if cue.get("english_text", "").strip() != en[index][3].strip():
                errors.append(f"Voice manifest English text differs from SRT at cue {index + 1}.")
            if index < len(fa) and cue.get("dari_text", "").strip() != fa[index][3].strip():
                errors.append(f"Voice manifest Dari text differs from SRT at cue {index + 1}.")
    if len(voice_paths) != len(set(voice_paths)):
        errors.append("Voice manifest contains duplicate or empty output paths.")
    if len(en) != len(fa):
        errors.append(f"Subtitle cue count differs: EN={len(en)}, FA={len(fa)}.")
    if [x[1:3] for x in en] != [x[1:3] for x in fa]:
        errors.append("English and Dari subtitle time boundaries do not match.")
    for lang, cues in (("EN", en), ("FA", fa)):
        if [x[0] for x in cues] != list(range(1, len(cues) + 1)):
            errors.append(f"{lang} subtitle cue numbering is not sequential.")
        for i, cue in enumerate(cues):
            if to_ms(cue[1]) >= to_ms(cue[2]):
                errors.append(f"{lang} cue {cue[0]} has zero/negative duration.")
            if i and to_ms(cues[i-1][2]) > to_ms(cue[1]):
                errors.append(f"{lang} cues {cues[i-1][0]} and {cue[0]} overlap.")
    if en and en[-1][2] != "00:07:00,000":
        errors.append("English subtitle track does not end at 07:00.")
    gate_scene = (SCENES / "04-departure-gate.svg").read_text(encoding="utf-8")
    if "GATE 12" not in gate_scene:
        errors.append("Departure gate artwork is missing Gate 12 signage.")
    svg_paths = list((ROOT / "assets").rglob("*.svg"))
    for svg_path in svg_paths:
        try:
            root = ET.parse(svg_path).getroot()
            if svg_path.parent == SCENES and (root.attrib.get("width") != "1280" or root.attrib.get("height") != "720"):
                errors.append(f"Scene plate must be 1280x720: {svg_path.relative_to(ROOT)}")
        except ET.ParseError as exc:
            errors.append(f"Invalid SVG/XML in {svg_path.relative_to(ROOT)}: {exc}")
    if not svg_paths:
        errors.append("No SVG assets were found.")
    if errors:
        print("VALIDATION FAILED")
        for item in errors:
            print(" -", item)
        return 1
    print("VALIDATION PASSED")
    print(f" - {len(shots)} shots / 420 seconds")
    print(f" - {len(en)} English cues and {len(fa)} Dari cues; voice manifest text/timing/roles aligned")
    print(" - English/Dari cue boundaries match")
    print(" - all scene plates exist; Gate 12 confirmed")
    print(f" - {len(svg_paths)} SVG files parse as valid XML")
    return 0

if __name__ == "__main__":
    sys.exit(main())
