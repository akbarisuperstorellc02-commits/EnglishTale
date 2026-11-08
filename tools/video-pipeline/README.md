# EnglishTale Episode Renderer

This local tool assembles the 18-shot, 420-second Episode 001 timeline from either the original SVG scene plates or a procedural Blender PNG shot library. It applies gentle Ken Burns-style zoom to the stills; it does not add multi-layer parallax or continuous full-3D character animation.

## Requirements
- Python 3.10+
- FFmpeg and FFprobe on PATH
- CairoSVG: `python -m pip install -r tools/video-pipeline/requirements.txt`

## Silent review
```bash
python tools/video-pipeline/render_episode.py
```
Default output: `build/episode-001-review.mp4`.

## English audio and subtitle tracks

The active delivery has one British English audio track and two optional selectable subtitle tracks. Afghan Dari is never generated as voiceover. English dialogue is loudness-normalized to an approximately -16 LUFS target with a -1.5 dBTP true-peak ceiling during MP4 muxing.

```bash
python tools/video-pipeline/render_episode.py \
  --english-audio build/audio/episode-001-en.wav \
  --subtitles-en episodes/001-english-at-the-airport/subtitles-en.srt \
  --subtitles-fa episodes/001-english-at-the-airport/subtitles-fa.srt
```

Options:
- `--shot-list` — use an alternate JSON timeline, including `render-shotlist-3d.json` after the Blender stills are rendered.
- `--width`, `--height`, `--fps` — review export dimensions and frame rate.
- `--no-motion` — disable the gentle scene-plate zoom.
- `--audio` — compatibility alias for `--english-audio`.
- `--subtitles-en` and `--subtitles-fa` — mux selectable MP4 subtitle tracks (UTF-8).

The renderer checks that the English audio is approximately the full 420-second runtime and refuses to silently truncate the video. For the 3D-still workflow, first run `tools/blender/render_character_lookdev.py --shot-library` to create `build/3d-shots/shot-01.png` through `shot-18.png`, then pass `--shot-list episodes/001-english-at-the-airport/render-shotlist-3d.json`. CI produces a 720p24 review cut and a 1080p30 master candidate; both are technical outputs and still require human review. Subtitle timestamps are still provisional and must be retimed after the actual voice recordings are approved.

## 3D YouTube brand assets

After the 18 Blender stills are rendered, create a 4K 16:9 thumbnail and a vertical Shorts cover that reuse the episode's actual 3D characters:

```bash
python -m pip install cairosvg pillow
python tools/video-pipeline/render_3d_brand_assets.py --shots-dir build/3d-shots --output-dir build/brand-assets
```

Outputs:
- `build/brand-assets/episode-001-thumbnail-3d.jpg` — 3840×2160.
- `build/brand-assets/episode-001-shorts-cover-3d.jpg` — 2160×3840.

Both outputs are JPEG-optimized for YouTube upload and must be checked at phone size before publication.

## Current limitations
- Uses scene plates with gentle camera motion; it does not composite the animated character rigs.
- Does not create full 3D character animation, lip sync, voice, music, or sound effects.
- Soft subtitle tracks are optional; separate SRT files should also be retained for YouTube upload.
- A human review of the complete MP4 is mandatory before publication.

## Timeline integrity
The shot list is `episodes/001-english-at-the-airport/render-shotlist.json`. The renderer requires exactly 420 seconds (07:00) and verifies the output file exists and is not unexpectedly small.
