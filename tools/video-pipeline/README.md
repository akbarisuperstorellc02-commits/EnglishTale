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
python tools/video-pipeline/render_episode.py --english-audio build/audio/episode-001-en.wav --dari-audio build/audio/episode-001-fa.wav
```

Before assembling language tracks, `build_audio_tracks.py` automatically runs `tools/tts/validate_voice_assets.py --strict`; all 96 clips must pass technical validation. The optional audio file(s) must be at least 419 seconds long. The tool refuses to mux short files and silently truncate the episode. Use `--english-audio` and `--dari-audio` together to place both languages in one MP4 as selectable audio tracks; the English track is the default. `--audio` remains available for a single pre-mixed track.

## Current limitations
- The renderer uses scene plates with gentle camera movement; it does not composite the animated character rigs.
- It does not generate voices, music, or sound effects.
- It does not synthesize or mix the English and Dari recordings together. The dual-track export keeps them selectable so learners do not hear two languages speaking over one another.
- It does not burn captions into the picture. Keep the English and Dari SRT files as separate subtitle tracks until their timings are checked against real audio.
- It is a review assembly, not a final broadcast-quality animation. A human review is required before publication.

## Timeline integrity
The shot list is stored in `episodes/001-english-at-the-airport/render-shotlist.json`. The script checks that all shot durations total exactly 420 seconds (07:00). The still-image zoom effect emits one output frame per input frame to avoid accidental frame multiplication.
