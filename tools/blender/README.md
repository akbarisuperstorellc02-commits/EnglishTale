# Blender 3D look-development

The procedural scene builds the canonical Leo, Emma, and Ollie designs in a Gate 12 airport terminal using original Blender geometry and materials. It is an early look-development proof, not the final production character rig or finished episode.

## Local render

Install Blender 4.x or newer, then run:

```bash
blender -b -t 2 --python tools/blender/render_character_lookdev.py -- --output build/episode-001-3d-lookdev.png
```

The scene renders on CPU; GPU acceleration is optional. The GitHub Actions workflow also renders a 1280×720 preview and uploads it as an artifact.

## Production notes

- Keep Leo in a blue hoodie and dark jeans, Emma in a pink sweater and dark jeans, and Ollie as a small brown owl with cream face/chest, round glasses, and navy scarf with gold trim.
- Gate signage must remain Gate 12.
- This scene is a procedural look-dev draft. Inspect the rendered artifact before reusing the design in production.
- The hybrid pipeline may combine approved 3D shots with 2.5D compositing, parallax, camera movement, and original motion graphics.
- Do not call a 2.5D fallback full 3D.
