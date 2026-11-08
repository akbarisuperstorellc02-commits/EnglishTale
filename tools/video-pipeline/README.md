# EnglishTale Episode Renderer

This local tool builds a **silent visual review cut** from the five original SVG scene plates. It is intended to validate the timeline, scene order, and export settings while the voice recordings are being produced.

## Requirements
- Python 3.10+
- FFmpeg and FFprobe installed and available on PATH
- CairoSVG: `python -m pip install -r tools/video-pipeline/requirements.txt`

## Run from the repository root
```bash
python tools/video-pipeline/render_episode.py
```

Default output:
`build/episode-001-review.mp4`

Optional settings:
```bash
python tools/video-pipeline/render_episode.py --output build/review.mp4 --width 960 --height 540 --fps 24
python tools/video-pipeline/render_episode.py --no-motion
python tools/video-pipeline/render_episode.py --audio path/to/reviewed-full-mix.wav
```

The optional audio file must be at least 419 seconds long. The tool refuses to mux a short file and silently truncate the episode.

## Current limitations
- The renderer uses scene plates with gentle camera movement; it does not composite the animated character rigs.
- It does not generate voices, music, or sound effects.
- It does not burn captions into the picture. Keep the English and Dari SRT files as separate subtitle tracks until their timings are checked against real audio.
- It is a review assembly, not a final broadcast-quality animation. A human review is required before publication.

## Timeline integrity
The shot list is stored in `episodes/001-english-at-the-airport/render-shotlist.json`. The script checks that all shot durations total exactly 420 seconds (07:00).
