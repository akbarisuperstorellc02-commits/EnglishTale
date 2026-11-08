#!/usr/bin/env python3
"""Deterministic frame renderer for the EnglishTale airport motion study."""
from pathlib import Path
import asyncio
import subprocess
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "experiments/svg-motion/airport-arrival-study.html"
OUT = ROOT / "dist/airport-arrival-sample.mp4"
FRAMES = ROOT / "dist/frames"
FPS = 30
DURATION = 6

async def main():
    if not SOURCE.exists():
        raise SystemExit(f"Missing source scene: {SOURCE}")
    FRAMES.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": 1330, "height": 770},
            device_scale_factor=1,
            reduced_motion="no-preference",
        )
        await page.goto(SOURCE.as_uri(), wait_until="networkidle")
        stage = page.locator(".stage")
        await stage.wait_for()
        await page.evaluate("document.fonts.ready")
        for frame in range(FPS * DURATION):
            milliseconds = frame * 1000 / FPS
            await page.evaluate(
                """(t) => {
                    for (const animation of document.getAnimations()) {
                        animation.currentTime = t;
                    }
                }""",
                milliseconds,
            )
            await stage.screenshot(
                path=str(FRAMES / f"frame-{frame:05d}.jpg"),
                type="jpeg",
                quality=92,
                animations="allow",
            )
        await browser.close()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-framerate", str(FPS), "-i", str(FRAMES / "frame-%05d.jpg"),
        "-frames:v", str(FPS * DURATION),
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        str(OUT),
    ], check=True)
    probe = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration,size", "-of", "default=noprint_wrappers=1",
        str(OUT),
    ], check=True, capture_output=True, text=True)
    print(f"Created: {OUT}")
    print(probe.stdout.strip())

if __name__ == "__main__":
    asyncio.run(main())
