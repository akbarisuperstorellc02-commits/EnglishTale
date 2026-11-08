# Blender 3D look-development and motion study

The procedural scene builds the canonical Leo, Emma, and Ollie designs in a Gate 12 airport terminal using original Blender geometry and materials. It is an early look-development proof, not the final production character rig or finished episode.

## Still render

Install Blender 4.x or newer, then run:

```bash
blender -b -t 2 --python tools/blender/render_character_lookdev.py -- --output build/episode-001-3d-lookdev.png
```

## 18-shot 3D still library

Render the procedural airport scene from the 18 planned camera angles:

```bash
blender -b -t 2 --python tools/blender/render_character_lookdev.py -- --shot-library --shots-dir build/3d-shots --width 1920 --height 1080
```

This creates `shot-01.png` through `shot-18.png` at 1920×1080. The 3D shot list `episodes/001-english-at-the-airport/render-shotlist-3d.json` maps each still to its timeline duration. The final renderer applies gentle 2.5D camera motion to each 3D still. This is a hybrid 3D-still/2.5D edit, not continuous full-3D character animation. Shot 16 includes an in-world 3D board with five airport phrases, and shot 17 includes a matching 3D quiz board; the check-in close-ups include enlarged passport and boarding-pass props.

## Short motion study

The same scene can render a short 3D motion study with subtle character body movement and a slow camera push. The CI proof is intentionally 640×360 at 24 fps to keep CPU rendering practical; the look-development still remains 1280×720:

```bash
blender -b -t 2 --python tools/blender/render_character_lookdev.py -- --animation --duration 2 --fps 24 --output build/episode-001-3d-motion-study.mp4
```

This is an animation pipeline proof, not the final seven-minute episode. The motion is deliberately limited to test the scene, camera, character grouping, and MP4 export path. Dialogue-specific acting, hand interactions, detailed facial rigging, and lip sync remain production tasks.

The scene renders on CPU; GPU acceleration is optional. GitHub Actions renders both a 1280×720 still and the short MP4 motion study, validates their output, and uploads them as one artifact.

## Production notes

- Keep Leo in a blue hoodie and dark jeans, Emma in a pink sweater and dark jeans, and Ollie as a small brown owl with cream face/chest, round glasses, and navy scarf with gold trim.
- Gate signage must remain Gate 12.
- Inspect every rendered artifact before reusing the design in production.
- The hybrid pipeline may combine approved 3D shots with 2.5D compositing, parallax, camera movement, and original motion graphics.
- Do not call a 2.5D fallback full 3D.
