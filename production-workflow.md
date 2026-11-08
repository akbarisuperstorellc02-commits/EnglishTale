# Production Workflow — EnglishTale

## Phase 1 — Pre-production
1. Confirm episode learning goal and CEFR level.
2. Review script for natural British English and accurate Afghan Dari subtitles.
3. Lock character reference designs and continuity details.
4. Create storyboard and shot list.
5. Organize episode assets and maintain a license log.

## Phase 2 — Visual production
1. Build and review the procedural Blender character and airport look-development scene.
2. Lock Leo, Emma, and Ollie appearance, proportions, clothing, and palette.
3. Render the 18-angle Blender 3D still library at 1920×1080.
4. Apply controlled 2.5D camera movement to the 3D stills for the 7-minute master candidate.
5. Use the original SVG scene plates for a separate lightweight review cut and fallback.
6. Reject inconsistent faces, clothing, proportions, or visual artifacts.
7. Never describe a 2.5D shot as continuous full-3D character animation.

## Phase 3 — Audio
1. Generate British English lines locally with Piper TTS; no paid or cloud API is part of the active workflow.
2. Use the committed role-to-speaker map to keep narrator and character voices distinct.
3. Listen to all lines for pronunciation, stress, timing, clipping, and character consistency.
4. Validate all 48 English WAV files with `python tools/tts/validate_voice_assets.py --strict`.
5. Assemble the English track with `python tools/tts/build_english_track.py`.
6. Run `python tools/tts/retime_subtitles.py` to derive subtitle cue ends from measured WAV durations. This is a duration-based first pass, not phoneme-level alignment; listen and review both SRT tracks manually.
7. Afghan Dari is subtitle-only; do not generate or mix Dari voiceover.
8. Use only sound effects and music with documented commercial-use permission. The current automated review candidate is dialogue-only.

## Phase 4 — Editing and export
The automated FFmpeg pipeline creates:
- A 1280×720, 24 fps review cut using the original SVG scene plates.
- A 1920×1080, 30 fps master candidate using the procedural Blender 3D still library with 2.5D camera motion.
- One normalized British English audio stream and separate selectable English and Afghan Dari subtitle streams.

Suggested manual finishing track layout:
- V1: 3D / 2.5D scene shots
- V2: English phrase cards, graphics, logo, end screen
- A1: English dialogue and narration
- A2: optional ambience and sound effects
- A3: optional licensed background music
- Captions: English captions and a separate Afghan Dari subtitle track

## Phase 5 — Learning design and quality review
- Speak the English line first and show the matching English caption.
- Keep the Afghan Dari subtitle concise and aligned with the spoken English.
- Include 2–3 seconds for repeat-after-me moments.
- Teach a manageable number of new phrases.
- Use a quiz with one unambiguous correct answer.
- Watch the entire export with sound and muted, on both a phone and a desktop.
- Review English pronunciation, Dari translation, subtitle timing, framing, visual continuity, and safe areas.

## Phase 6 — Publishing
1. Approve the full-resolution master after human review.
2. Verify every asset and voice-model license for commercial use; include VCTK CC BY 4.0 attribution.
3. Upload the thumbnail, title, description, tags, and separate SRT captions.
4. Add the episode to the correct playlist.
5. Create Shorts only after the long-form episode is approved.

## Free / low-cost approach
Use local Piper TTS and CPU-capable Blender rendering. GPU acceleration is optional. Use the hybrid combination of procedural 3D stills, 2.5D camera motion, and original SVG assets when continuous full-3D character animation is impractical. No paid API is required for the active production path.
