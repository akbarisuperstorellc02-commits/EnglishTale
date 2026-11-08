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
- [x] Generated all 48 real British English WAV cues in GitHub Actions using the pinned multi-speaker VCTK model; all 48 passed strict technical validation.
- [x] Assembled the complete 420-second English master WAV at 22,050 Hz mono PCM.
- [x] Generated first-pass English and Afghan Dari retimed SRT files from the measured WAV cue durations.
- [x] Uploaded the English audio, all cue WAVs, retimed SRTs, and VCTK attribution note as a GitHub Actions artifact.
- [x] FFmpeg/CairoSVG 7-minute scene-plate renderer with optional British English audio and selectable English/Dari subtitle streams.
- [x] Complete 420-second 1280×720 H.264 review MP4 rendered with AAC English dialogue and two selectable subtitle tracks; technical stream/duration validation passed.
- [x] 4K YouTube thumbnail and vertical Shorts cover source artwork, renderers, validators, and CI artifacts.
- [x] Procedural Blender 3D look-development scene and successful 1280×720 still render.
- [x] Short 3D character motion-study MP4 rendered and validated at 640×360/24 fps; this is a two-second technical preview, not a finished episode shot.
- [x] GitHub Actions validation checks for source assets, scripts, TTS pipeline tests, thumbnail outputs, and cover outputs.

## Not yet complete — release blockers

- [ ] Listen to all 48 generated English WAV clips for pronunciation, pacing, role consistency, clipping, and quality.
- [ ] Listen to and approve the generated English track; manually review both WAV-duration-retimed subtitle files. Duration-based retiming is only a first pass.
- [ ] Complete final 3D/2.5D character animation, scene coverage, hand interactions, and appropriate dialogue acting. The current Blender still is only look-development, not the final character rig.
- [ ] Human-review the 720p review cut with sound and muted, fix visual/timing issues, complete sound design, then export and review the final 1080p/30fps master.
- [ ] Final human review of thumbnails, licenses, subtitles, audio, and YouTube metadata before publication.

## Verified GitHub checks

- [x] [48 real English WAV cues, 7-minute master, and retimed subtitles generated successfully](https://github.com/akbarisuperstorellc02-commits/EnglishTale/actions/runs/42503923500).
- [x] [Complete 7-minute 720p review MP4 with English audio and two selectable subtitle tracks](https://github.com/akbarisuperstorellc02-commits/EnglishTale/actions/runs/42504251122).
- [x] [Download the review MP4, 48 English cue WAVs, master WAV, retimed SRTs, and VCTK attribution](https://github.com/akbarisuperstorellc02-commits/EnglishTale/actions/runs/42504251122/artifacts/13626981971).
- [x] [Offline TTS generation and WAV assembly tests passed](https://github.com/akbarisuperstorellc02-commits/EnglishTale/actions/runs/42503217997).
- [x] [Episode source, TTS, thumbnail, and Shorts validation passed](https://github.com/akbarisuperstorellc02-commits/EnglishTale/actions/runs/42503053663).
- [x] [Procedural 3D still render passed](https://github.com/akbarisuperstorellc02-commits/EnglishTale/actions/runs/42501465316).
- [x] [3D look-development still and motion-study MP4 artifact uploaded](https://github.com/akbarisuperstorellc02-commits/EnglishTale/actions/runs/42504288974).

## Local production commands

On Windows PowerShell 5.1, run the one-command builder: `.\tools\windows\build_episode_001.ps1` (use `-SkipVideo` to build audio only, or `-Overwrite` to regenerate voice clips).

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
