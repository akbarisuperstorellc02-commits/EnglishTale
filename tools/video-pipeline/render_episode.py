#!/usr/bin/env python3
"""Render Episode 001 scene plates into a 7-minute MP4 review/master candidate.

Requires FFmpeg/ffprobe on PATH and CairoSVG. This renderer applies gentle
camera motion to the approved scene plates. It can mux one English audio track
and separate selectable English/Afghan Dari subtitle tracks. It does not claim
to create full 3D character animation or phoneme-accurate lip sync.
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
SCENES = ROOT / "assets" / "scenes"
SHOT_FILE = ROOT / "episodes" / "001-english-at-the-airport" / "render-shotlist.json"
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--shot-list", type=Path, default=SHOT_FILE,
                        help="JSON shot list; supports SVG/PNG plates and rendered MP4 animation clips")
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--fps", type=int, default=30)
    audio_group = parser.add_mutually_exclusive_group()
    audio_group.add_argument("--english-audio", "--audio", dest="english_audio", type=Path,
                             help="Optional reviewed British English WAV track")
    parser.add_argument("--subtitles-en", type=Path, help="Optional English SRT subtitle track")
    parser.add_argument("--subtitles-fa", type=Path, help="Optional Afghan Dari SRT subtitle track")
    parser.add_argument("--no-motion", action="store_true", help="Use static scene plates")
    args = parser.parse_args()

    ffmpeg = require_tool("ffmpeg")
    require_tool("ffprobe")
    try:
        import cairosvg
    except ImportError:
        cairosvg = None

    for label, path in (("English audio", args.english_audio),
                        ("English subtitles", args.subtitles_en),
                        ("Afghan Dari subtitles", args.subtitles_fa)):
        if path is not None and not path.is_file():
            raise SystemExit(f"{label} file not found: {path}")

    shots = json.loads(args.shot_list.read_text(encoding="utf-8"))
    if not shots:
        raise SystemExit("Shot list is empty.")
    total = sum(int(shot["duration"]) for shot in shots)
    if total != 420:
        raise SystemExit(f"Expected a 420-second (07:00) timeline; shot list totals {total} seconds.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="englishtale-") as temp:
        tempdir = Path(temp)
        rendered: list[Path] = []
        for index, shot in enumerate(shots, start=1):
            scene_ref = Path(shot["scene"])
            if scene_ref.is_absolute():
                scene = scene_ref
            elif scene_ref.parts and scene_ref.parts[0] == "build":
                scene = ROOT / scene_ref
            else:
                scene = SCENES / scene_ref
            if not scene.is_file():
                raise SystemExit(f"Missing scene asset: {scene}")
            clip = tempdir / f"shot-{index:02d}.mp4"
            shot_seconds = int(shot["duration"])
            if scene.suffix.lower() == ".mp4":
                # Actual rendered animation: no artificial zoom is applied.
                vf = (f"scale={args.width}:{args.height}:force_original_aspect_ratio=decrease,"
                      f"pad={args.width}:{args.height}:(ow-iw)/2:(oh-ih)/2,"
                      f"fps={args.fps},format=yuv420p")
                run([ffmpeg, "-y", "-stream_loop", "-1", "-i", str(scene),
                     "-t", str(shot_seconds), "-vf", vf, "-an",
                     "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                     "-pix_fmt", "yuv420p", str(clip)])
            else:
                png = tempdir / f"scene-{index:02d}.png"
                if scene.suffix.lower() == ".svg":
                    if cairosvg is None:
                        raise SystemExit("CairoSVG is required for SVG plates.")
                    cairosvg.svg2png(url=str(scene), write_to=str(png),
                                     output_width=args.width, output_height=args.height)
                elif scene.suffix.lower() == ".png":
                    shutil.copy2(scene, png)
                else:
                    raise SystemExit(f"Unsupported scene asset type: {scene.suffix}")
                frames = shot_seconds * args.fps
                vf = f"scale={args.width}:{args.height},format=yuv420p"
                if not args.no_motion:
                    vf = (f"zoompan=z='min(zoom+0.00035,1.045)':d=1:"
                          f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                          f"s={args.width}x{args.height}:fps={args.fps},format=yuv420p")
                run([ffmpeg, "-y", "-loop", "1", "-framerate", str(args.fps),
                     "-i", str(png), "-vf", vf, "-frames:v", str(frames),
                     "-an", "-c:v", "libx264", "-preset", "veryfast",
                     "-crf", "22", "-pix_fmt", "yuv420p", str(clip)])
            rendered.append(clip)
            print(f"Rendered shot {index}/{len(shots)}: {shot['label']}")

        concat = tempdir / "concat.txt"
        concat.write_text("".join(f"file '{clip.as_posix()}'\n" for clip in rendered), encoding="utf-8")
        silent = tempdir / "silent.mp4"
        run([ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
             "-c", "copy", "-movflags", "+faststart", str(silent)])

        has_tracks = any((args.english_audio, args.subtitles_en, args.subtitles_fa))
        if has_tracks:
            cmd = [ffmpeg, "-y", "-i", str(silent)]
            input_index = 1
            if args.english_audio:
                duration = probe_duration(args.english_audio)
                if duration < total - 1.0:
                    raise SystemExit(f"English audio is only {duration:.1f}s; expected about {total}s. Refusing to truncate the video.")
                cmd += ["-i", str(args.english_audio)]
                input_index += 1
            subtitle_inputs = []
            for subtitle in (args.subtitles_en, args.subtitles_fa):
                if subtitle:
                    cmd += ["-sub_charenc", "UTF-8", "-i", str(subtitle)]
                    subtitle_inputs.append((input_index, subtitle))
                    input_index += 1
            cmd += ["-map", "0:v:0", "-c:v", "copy"]
            if args.english_audio:
                cmd += ["-map", "1:a:0", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                        "-c:a", "aac", "-b:a", "192k",
                        "-metadata:s:a:0", "language=eng", "-metadata:s:a:0", "title=British English (normalized)"]
            if subtitle_inputs:
                for stream_index, (_, subtitle) in enumerate(subtitle_inputs):
                    cmd += ["-map", f"{subtitle_inputs[stream_index][0]}:s:0"]
                cmd += ["-c:s", "mov_text"]
                if args.subtitles_en:
                    cmd += ["-metadata:s:s:0", "language=eng", "-metadata:s:s:0", "title=English"]
                if args.subtitles_fa:
                    fa_stream = 1 if args.subtitles_en else 0
                    cmd += [f"-metadata:s:s:{fa_stream}", "language=fas",
                            f"-metadata:s:s:{fa_stream}", "title=Afghan Dari"]
            cmd += ["-t", str(total), "-movflags", "+faststart", str(args.output)]
            run(cmd)
        else:
            shutil.copy2(silent, args.output)

    if not args.output.is_file() or args.output.stat().st_size < 50000:
        raise SystemExit(f"Render output missing or unexpectedly small: {args.output}")
    print(f"\nReview render created: {args.output}")
    print("MP4 shot assets are rendered motion clips; SVG/PNG assets remain scene plates (PNG may use camera motion only).")
    print("Afghan Dari is subtitle-only. Subtitle timestamps remain provisional until final English audio is approved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
