# Production Workflow — EnglishTale

## Phase 1 — Pre-production
1. Confirm episode learning goal and CEFR level.
2. Review script for natural British English and accurate Afghan Dari subtitles.
3. Lock character reference designs and continuity details.
4. Create storyboard and shot list.
5. Organize episode assets and maintain a license log.

## Phase 2 — Visual production
1. Build and review the 3D character look-development scene first.
2. Lock Leo, Emma, and Ollie appearance, proportions, clothing, and palette.
3. Create 3D shots where feasible; use layered 2.5D compositing, parallax, camera movement, and selective character animation for remaining shots.
4. Reject inconsistent faces, clothing, proportions, or visual artifacts.
5. Use lighting, depth of field, atmospheric perspective, and controlled camera movement to create a cohesive cinematic look.
6. Never describe a 2.5D shot as full 3D.

## Phase 3 — Audio
1. Generate British English lines locally with Piper TTS; no paid or cloud API is part of the active workflow.
2. Keep dialogue roles consistent; use individually licensed local voice models only when needed.
3. Listen to all lines for pronunciation, stress, timing, clipping, and character consistency.
4. Assemble the English track with `python tools/tts/build_english_track.py`.
5. Afghan Dari is subtitle-only; do not generate or mix Dari voiceover.
6. Use only sound effects and music with documented commercial-use permission. Keep music quiet beneath dialogue.

## Phase 4 — Editing
Suggested CapCut track layout:
- V1: 3D / 2.5D animated scene shots
- V2: English phrase cards, graphics, logo, end screen
- A1: English dialogue and narration
- A2: ambience and sound effects
- A3: licensed background music
- Captions: English captions and a separate Afghan Dari subtitle track

Suggested export settings:
- 1920×1080, 16:9, 30 fps
- MP4 / H.264
- Safe margins for both subtitle languages
- No Dari narration track

## Phase 5 — Learning design
- Speak the English line first and show the matching English caption.
- Keep the Afghan Dari subtitle concise and aligned with the spoken English.
- Include 2–3 seconds for repeat-after-me moments.
- Teach a manageable number of new phrases.
- Use a quiz with one unambiguous correct answer.

## Phase 6 — Publishing
1. Export a full-resolution master.
2. Watch the entire video on a phone with headphones and a phone speaker.
3. Review English pronunciation, Dari translation, subtitle timing, and text safe areas.
4. Verify every asset and voice-model license for commercial use.
5. Upload the thumbnail, title, description, and tags.
6. Add the episode to the correct playlist.
7. Create 2–3 Shorts only after the long-form episode is complete.

## Free / low-cost approach
Use local Piper TTS and CPU-capable Blender rendering. GPU acceleration is optional. Use a hybrid mix of original 3D shots and 2.5D scenes when rendering every shot in full 3D is impractical. No paid API is required for the active production path.
