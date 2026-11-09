# EnglishTale — Episode 001 Production Status

Last updated: 2026-11-09

## Approved production settings

- British English dialogue and narration (en-GB).
- Afghan Dari subtitles only; no Dari voiceover.
- Local/offline Piper TTS; no paid API or cloud voice dependency.
- CPU-compatible Blender rendering; GPU acceleration is optional.
- Canonical characters: Leo (blue hoodie), Emma (pink sweater), Ollie (small brown owl with cream face/chest, round glasses, navy scarf with gold trim).
- Airport gate: Gate 12.
- Master target: 1920×1080, 30 fps, 16:9, H.264 MP4, 420 seconds.

## Verified outputs

- [x] 48 British English WAV dialogue/narration cues generated and strictly validated.
- [x] 420-second English master WAV assembled at 22,050 Hz mono PCM.
- [x] English and Afghan Dari subtitle files retimed from measured WAV cue durations and embedded as selectable tracks.
- [x] 420-second 1280×720 H.264 review MP4, 24 fps, AAC English audio, two selectable subtitle tracks.
- [x] 420-second 1920×1080 H.264 master candidate, 30 fps, AAC English audio, two selectable subtitle tracks.
- [x] 18 Blender-rendered animated 3D MP4 shots included in the master/review build; each shot is an 8-second, 640×360, 12 fps clip.
- [x] Procedural body bob, simple arm/leg movement, owl tuft movement, shot-specific gesture/walk beats, and subtle camera/lens motion added.
- [x] Camera motion now returns to its starting pose at clip boundaries to reduce visible jumps when an 8-second shot loops.
- [x] 4K YouTube thumbnail (3840×2160) and vertical Shorts cover (2160×3840) rendered as JPEGs; Ollie's crop corrected and re-rendered.
- [x] Brand artwork build now extracts frames from animated MP4s with FFmpeg and is independently rebuildable.
- [x] Main episode pipeline and brand-artwork workflow completed successfully.

## Current artifact links

- [Episode 001 master, review, 48 WAV cues, two subtitle files, and 18 animated 3D shots](https://github.com/akbarisuperstorellc02-commits/EnglishTale/actions/runs/42597115457)
- [Latest corrected YouTube thumbnail and Shorts cover](https://github.com/akbarisuperstorellc02-commits/EnglishTale/actions/runs/42614868902)
- [Latest camera-loop animation build](https://github.com/akbarisuperstorellc02-commits/EnglishTale/actions/runs/42615179681)
- [Latest Blender look-development validation](https://github.com/akbarisuperstorellc02-commits/EnglishTale/actions/runs/42615179710)

## Honest quality limitations — not release-approved

The current 3D characters are simple stylized procedural models, not premium feature-film-quality character assets. Their animation is limited procedural motion; it is not full character acting. The 18 eight-second shots are repeated to fill longer timeline sections, so repeated motion can still be noticed.

The following work remains before describing the episode as a polished cinematic production:

- [ ] Replace primitive toy-like character geometry with production-quality sculpted models, clothing detail, hair/feather detail, and more natural proportions while preserving the approved designs.
- [ ] Build proper character rigs with articulated shoulders, elbows, wrists, hips, knees, and feet; add grounded walk cycles and believable body weight.
- [ ] Add facial expressions, blinking, eye direction, mouth visemes, and dialogue-synchronized lip movement.
- [ ] Animate actual prop interactions: passport handoff, boarding pass, suitcase, security tray/scanner, and boarding gesture.
- [ ] Produce multiple distinct takes for long scenes instead of repeating the same 8-second clip.
- [ ] Add restrained airport ambience and sound effects, mixed below dialogue.
- [ ] Human-listen to all 48 English WAV cues for pronunciation, pacing, role consistency, clipping, and voice quality.
- [ ] Manually review both subtitle tracks against the recording; duration-based retiming is only a first pass.
- [ ] Human-review the complete video with sound and muted, then approve final publishing metadata and artwork.

## Release rule

The technically valid master candidate and artwork are deliverables for review, not proof of cinematic completion. Do not mark Episode 001 publish-ready until the animation, audio, subtitles, sound design, and full video have passed human quality review.

## Local Windows build

Windows PowerShell 5.1 builder: `.\tools\windows\build_episode_001.ps1` (use `-SkipVideo` for audio-only or `-Overwrite` to regenerate voice clips). See the root README and `production-workflow.md` for the complete sequence.
