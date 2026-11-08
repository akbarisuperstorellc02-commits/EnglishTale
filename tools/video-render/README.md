# Render the airport motion sample

This renderer converts the self-contained HTML/SVG airport study into a real
H.264 MP4 using Chromium screenshots and FFmpeg. It uses no paid API and no
image-generation quota.

## Run on GitHub

Open **Actions → Render airport sample video → Run workflow**. When it finishes,
download the artifact named `EnglishTale-airport-sample-mp4` from that run.
The output is a 6-second, 1280×720, 30 fps MP4.

## Run locally

Requirements: Python 3.11+, FFmpeg, and Playwright Chromium.

```bash
python -m pip install playwright
python -m playwright install chromium
python tools/video-render/render_airport_sample.py
```

The MP4 is written to `dist/airport-arrival-sample.mp4`. The renderer fixes the
animation clock for every frame to avoid depending on machine speed.

## Scope

This is a technical MP4 render of the existing 2D vector motion study. It is
not yet the final 3D cinematic art direction, final episode, or a voiced video.
