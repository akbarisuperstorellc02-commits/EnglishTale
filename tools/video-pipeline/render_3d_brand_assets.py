#!/usr/bin/env python3
"""Create 3D-consistent YouTube thumbnail and Shorts cover from Blender stills."""
from __future__ import annotations

import argparse
import base64
from pathlib import Path
import cairosvg
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]


def image_data(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f"Required 3D still not found: {path}")
    return base64.b64encode(path.read_bytes()).decode("ascii")


def svg_image(data: str, x: int, y: int, width: int, height: int,
              clip: str | None = None, preserve: str = "xMidYMid slice") -> str:
    clip_attr = f' clip-path="url(#{clip})"' if clip else ""
    return (
        f'<image x="{x}" y="{y}" width="{width}" height="{height}" '
        f'preserveAspectRatio="{preserve}" href="data:image/png;base64,{data}"{clip_attr}/>'
    )


def render_jpeg(svg: str, output: Path, width: int, height: int) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    png = output.with_suffix(".render.png")
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(png),
                     output_width=width, output_height=height)
    with Image.open(png) as image:
        image.convert("RGB").save(output, "JPEG", quality=89, optimize=True, progressive=True, subsampling=0)
    png.unlink(missing_ok=True)
    if not output.is_file() or output.stat().st_size < 100_000 or output.stat().st_size > 50 * 1024 * 1024:
        raise SystemExit(f"Thumbnail output missing or invalid: {output}")
    print(f"3D brand asset: {output} ({width}x{height}, {output.stat().st_size:,} bytes)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shots-dir", type=Path, default=ROOT / "build/3d-shots")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "build/brand-assets")
    args = parser.parse_args()
    shots = args.shots_dir
    bg = image_data(shots / "shot-01.png")
    leo = image_data(shots / "shot-02.png")
    emma = image_data(shots / "shot-03.png")
    ollie = image_data(shots / "shot-14.png")
    ending = image_data(shots / "shot-18.png")

    thumb = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="3840" height="2160" viewBox="0 0 3840 2160">
      <defs>
        <linearGradient id="shade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#07182e" stop-opacity=".98"/><stop offset=".48" stop-color="#07182e" stop-opacity=".84"/><stop offset="1" stop-color="#07182e" stop-opacity=".08"/></linearGradient>
        <linearGradient id="bottom" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#06172b" stop-opacity="0"/><stop offset="1" stop-color="#06172b" stop-opacity=".85"/></linearGradient>
        <clipPath id="leoClip"><rect x="1950" y="390" width="780" height="1390" rx="70"/></clipPath>
        <clipPath id="emmaClip"><rect x="2800" y="390" width="780" height="1390" rx="70"/></clipPath>
        <clipPath id="owlClip"><circle cx="2780" cy="1640" r="340"/></clipPath>
      </defs>
      {svg_image(bg,0,0,3840,2160)}
      <rect width="3840" height="2160" fill="#06172b" opacity=".30"/>
      <rect width="2150" height="2160" fill="url(#shade)"/>
      <rect y="1750" width="3840" height="410" fill="url(#bottom)"/>
      <rect x="130" y="135" width="620" height="180" rx="90" fill="#ffc653"/>
      <text x="440" y="255" text-anchor="middle" font-family="DejaVu Sans, sans-serif" font-size="108" font-weight="800" fill="#08203a">ENGLISH A1</text>
      <text x="180" y="690" font-family="DejaVu Sans, sans-serif" font-size="260" font-weight="900" fill="#ffffff">ENGLISH</text>
      <text x="180" y="1000" font-family="DejaVu Sans, sans-serif" font-size="260" font-weight="900" fill="#ffffff">AT THE</text>
      <text x="180" y="1310" font-family="DejaVu Sans, sans-serif" font-size="300" font-weight="900" fill="#63d8f2">AIRPORT</text>
      <rect x="180" y="1390" width="1510" height="20" rx="10" fill="#ffc653"/>
      <text x="185" y="1565" font-family="DejaVu Sans, sans-serif" font-size="86" font-weight="700" fill="#ffffff">LEARN ENGLISH THROUGH STORY</text>
      <text x="185" y="1695" font-family="DejaVu Sans, sans-serif" font-size="66" fill="#c8e2f2">LISTEN  •  LEARN  •  SPEAK</text>
      <rect x="1930" y="370" width="820" height="1430" rx="82" fill="#ffc653"/>
      {svg_image(leo,1950,390,780,1390,"leoClip")}
      <rect x="2780" y="370" width="820" height="1430" rx="82" fill="#ffc653"/>
      {svg_image(emma,2800,390,780,1390,"emmaClip")}
      <circle cx="2780" cy="1640" r="365" fill="#ffc653"/>
      {svg_image(ollie,2440,1300,680,680,"owlClip")}
      <text x="3650" y="2050" text-anchor="end" font-family="DejaVu Sans, sans-serif" font-size="52" font-weight="700" fill="#ffffff">ENGLISHTALE  •  EPISODE 001</text>
    </svg>'''
    shorts = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="2160" height="3840" viewBox="0 0 2160 3840">
      <defs>
        <linearGradient id="top" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#06172b" stop-opacity=".98"/><stop offset="1" stop-color="#06172b" stop-opacity="0"/></linearGradient>
        <linearGradient id="bottom" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#06172b" stop-opacity="0"/><stop offset="1" stop-color="#06172b" stop-opacity=".98"/></linearGradient>
        <clipPath id="shortLeoClip"><rect x="120" y="1450" width="900" height="1680" rx="80"/></clipPath>
        <clipPath id="shortEmmaClip"><rect x="1140" y="1450" width="900" height="1680" rx="80"/></clipPath>
        <clipPath id="shortOwlClip"><circle cx="1080" cy="3060" r="300"/></clipPath>
      </defs>
      {svg_image(bg,0,0,2160,3840)}
      <rect width="2160" height="3840" fill="#06172b" opacity=".40"/>
      <rect width="2160" height="1350" fill="url(#top)"/>
      <rect y="2780" width="2160" height="1060" fill="url(#bottom)"/>
      <rect x="180" y="190" width="600" height="170" rx="85" fill="#ffc653"/>
      <text x="480" y="305" text-anchor="middle" font-family="DejaVu Sans, sans-serif" font-size="98" font-weight="900" fill="#08203a">A1 ENGLISH</text>
      <text x="1080" y="820" text-anchor="middle" font-family="DejaVu Sans, sans-serif" font-size="180" font-weight="900" fill="#ffffff">ENGLISH AT</text>
      <text x="1080" y="1050" text-anchor="middle" font-family="DejaVu Sans, sans-serif" font-size="220" font-weight="900" fill="#63d8f2">THE AIRPORT</text>
      <rect x="280" y="1140" width="1600" height="18" rx="9" fill="#ffc653"/>
      <rect x="100" y="1430" width="940" height="1720" rx="95" fill="#ffc653"/>
      {svg_image(leo,120,1450,900,1680,"shortLeoClip")}
      <rect x="1120" y="1430" width="940" height="1720" rx="95" fill="#ffc653"/>
      {svg_image(emma,1140,1450,900,1680,"shortEmmaClip")}
      <circle cx="1080" cy="3060" r="320" fill="#ffc653"/>
      {svg_image(ollie,780,2760,600,600,"shortOwlClip")}
      <text x="1080" y="3470" text-anchor="middle" font-family="DejaVu Sans, sans-serif" font-size="100" font-weight="800" fill="#ffffff">LEARN ENGLISH THROUGH STORY</text>
      <text x="1080" y="3620" text-anchor="middle" font-family="DejaVu Sans, sans-serif" font-size="72" fill="#c8e2f2">LISTEN  •  LEARN  •  SPEAK</text>
      <text x="1080" y="3770" text-anchor="middle" font-family="DejaVu Sans, sans-serif" font-size="64" font-weight="700" fill="#ffc653">ENGLISHTALE  •  EPISODE 001</text>
    </svg>'''
    render_jpeg(thumb, args.output_dir / "episode-001-thumbnail-3d.jpg", 3840, 2160)
    render_jpeg(shorts, args.output_dir / "episode-001-shorts-cover-3d.jpg", 2160, 3840)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
