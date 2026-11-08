# Blender 3D look-development and motion study

The procedural scene builds the canonical Leo, Emma, and Ollie designs in a Gate 12 airport terminal using original Blender geometry and materials. It is an early look-development proof, not the final production character rig or finished episode.

## Still render

Install Blender 4.x or newer, then run:

```bash
blender -b -t 2 --python tools/blender/render_character_lookdev.py -- --output build/episode-001-3d-lookdev.png
```

## Short motion study

The same scene can render a short 3D motion study with subtle character body movement and a slow camera push:

```bash
blender -b -t 2 --python tools/blender/render_character_lookdev.py -- --animation --duration 4 --fps 24 --output build/episode-001-3d-motion-study.mp4
```

This is an animation pipeline proof, not the final seven-minute episode. The motion is deliberately limited to test the scene, camera, character grouping, and MP4 export path. Dialogue-specific acting, hand interactions, detailed facial rigging, and lip sync remain production tasks.

The scene renders on CPU; GPU acceleration is optional. GitHub Actions renders both a 1280×720 still and the short MP4 motion study, validates their output, and uploads them as one artifact.

## Production notes

- Keep Leo in a blue hoodie and dark jeans, Emma in a pink sweater and dark jeans, and Ollie as a small brown owl with cream face/chest, round glasses, and navy scarf with gold trim.
- Gate signage must remain Gate 12.
- Inspect every rendered artifact before reusing the design in production.
- The hybrid pipeline may combine approved 3D shots with 2.5D compositing, parallax, camera movement, and original motion graphics.
- Do not call a 2.5D fallback full 3D.
