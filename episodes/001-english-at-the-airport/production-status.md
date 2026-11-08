# EnglishTale — Episode 001 Production Status

Last updated: 2026-11-08

## Approved settings

- British English dialogue and narration (en-GB).
- Afghan Dari subtitles only; no Dari voiceover or Dari WAV files.
- Local/offline Piper TTS; no paid API or cloud dependency in the active workflow.
- Hybrid visuals targeting premium cinematic 3D; use high-quality 2.5D only as an honestly labelled fallback.
- GPU acceleration is optional. The pipeline must remain usable on CPU.
- Canonical characters: Leo (blue hoodie), Emma (pink sweater), Ollie (brown owl with cream face/chest, round glasses, navy scarf with gold trim).
- Airport gate: Gate 12.
- Target delivery: 1920×1080, 30 fps, 16:9, H.264 MP4, 420 seconds.

## Completed

- [x] Episode 001 story, teaching sections, character bible, storyboard, and 18-shot production plan.
- [x] Five original airport/airplane SVG scene plates and three animated SVG character rigs.
- [x] English and Afghan Dari SRT subtitle guides with 48 aligned cue boundaries.
- [x] 48-cue English voice manifest with role assignments and Dari subtitle text references only.
- [x] Local British English Piper TTS generator with resumable cue generation.
- [x] Pinned multi-speaker VCTK voice downloader with MD5/size verification and CC BY 4.0 attribution note.
- [x] Role-specific British English speaker IDs committed for narrator, Leo, Emma, airport agent, security officer, and Ollie.
- [x] English WAV assembler that preserves the model's native sample rate and blocks missing, silent, invalid, or overlong clips.
- [x] English-only voice WAV validator; strict release gate requires all 48 English clips.
- [x] Offline end-to-end tests for fake Piper generation, 48-cue assembly, resume behavior, missing-clip rejection, and subtitle retiming.
- [x] WAV-duration subtitle retiming helper that writes separate English and Afghan Dari SRT tracks. Human listening and final manual review remain required.
- [x] FFmpeg/CairoSVG 7-minute scene-plate renderer with optional British English audio and selectable English/Dari subtitle streams.
- [x] 4K YouTube thumbnail and vertical Shorts cover source artwork, renderers, validators, and CI artifacts.
- [x] Procedural Blender 3D look-development scene and successful 1280×720 still render.
- [x] GitHub Actions validation checks for source assets, scripts, TTS pipeline tests, thumbnail outputs, and cover outputs.

## Not yet complete — release blockers

- [ ] Run and verify the GitHub audio-generation workflow; it downloads the pinned VCTK model to the runner, generates all 48 clips, and packages the English WAV plus retimed subtitles. The model is intentionally not stored in Git. VCTK requires CC BY 4.0 attribution.
- [ ] Listen to all 48 generated English WAV clips for pronunciation, pacing, role consistency, clipping, and quality.
- [ ] Assemble the approved English track and retime both subtitle files; duration-based retiming is only a first pass.
- [ ] Complete final 3D/2.5D character animation, scene coverage, hand interactions, and appropriate dialogue acting. The current Blender still is only look-development, not the final character rig.
- [ ] Render the complete seven-minute episode, review the full MP4 with sound and muted, fix issues, and export the final 1080p master.
- [ ] Final human review of thumbnails, licenses, subtitles, audio, and YouTube metadata before publication.

## Verified GitHub checks

- [x] [Offline TTS generation and WAV assembly tests passed](https://github.com/akbarisuperstorellc02-commits/EnglishTale/actions/runs/42503217997).
- [x] [Episode source, TTS, thumbnail, and Shorts validation passed](https://github.com/akbarisuperstorellc02-commits/EnglishTale/actions/runs/42503053663).
- [x] [Procedural 3D still render passed](https://github.com/akbarisuperstorellc02-commits/EnglishTale/actions/runs/42501465316).
- [ ] Short 3D motion-study MP4 render and validation are being tested in GitHub Actions; do not treat it as a completed episode shot until the artifact is verified.

## Local production commands

```bash
python tools/video-pipeline/validate_episode.py
python -m unittest tools/tts/test_validate_voice_assets.py tools/tts/test_local_audio_pipeline.py -v
python tools/tts/download_british_voice.py
python tools/tts/generate_local_english.py --model models/piper/en_GB-vctk-medium/en_GB-vctk-medium.onnx --voices-json tools/tts/episode-001-voices.json --limit 6
python tools/tts/generate_local_english.py --model models/piper/en_GB-vctk-medium/en_GB-vctk-medium.onnx --voices-json tools/tts/episode-001-voices.json
python tools/tts/validate_voice_assets.py --strict
python tools/tts/build_english_track.py
python tools/tts/retime_subtitles.py
```

After human approval of the audio and retimed captions, render the review/master candidate with `tools/video-pipeline/render_episode.py`. See the root README and `production-workflow.md` for the full sequence.

## Release rule

Do not call Episode 001 complete or publish it until real English voice files exist, both subtitle tracks have been reviewed against the recording, the final video has rendered successfully, and the complete export has passed human quality review.
