# SVG motion study — Airport Arrival

This is a browser-playable proof of concept for Episode 001. Open
`airport-arrival-study.html` directly in a modern desktop browser. It is a
self-contained 16:9 HTML/SVG scene; no API key, image-generation service,
GPU, npm install, or external asset is required.

## What this prototype demonstrates

- Layered airport terminal, windows, floor perspective, departure board and aircraft.
- Leo in his blue hoodie and Emma in her pink sweater, with independent character
  movement, blinking and gesture animation.
- Ollie as the recurring owl guide.
- A suitcase entrance, gentle lighting movement, and a visible Gate 12 cue.
- CSS keyframes and SVG shapes that can be rendered frame-by-frame and encoded
  to MP4 with a browser renderer and FFmpeg.

## Relationship to Inkling

The public [Inkling project](https://github.com/ahkamboh/inkling) is a small,
MIT-licensed, code-driven explainer-video pipeline. Its key technical idea is
useful here: authored HTML/SVG scenes, deterministic browser frame capture,
then FFmpeg assembly. Its default art direction is hand-drawn mascot explainer
graphics, not cinematic 3D character animation. This study borrows the general
code-driven scene/render approach only; it does not copy Inkling source files.

## Honest quality boundary

This is a motion/production feasibility test, not an approved final art style.
It is custom 2D vector artwork with layered gradients and depth cues. It is not
a photorealistic or Pixar-like 3D render, and the characters are not yet the
final production-quality character models. Review the scene before deciding
whether to extend this pipeline across all 18 shots.

## Next technical step

If the visual direction is approved, build a deterministic renderer that:
1. Loads each scene at a fixed 1920×1080 viewport.
2. Advances a controlled animation clock at 30 fps.
3. Captures each frame without timing drift.
4. Encodes H.264 MP4 with FFmpeg.
5. Runs a short sample render in CI and uploads it as an artifact for review.

Do not replace the existing Gemini image pipeline or the current episode assets
until the user approves the visual test.
