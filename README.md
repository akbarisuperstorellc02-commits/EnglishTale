# EnglishTale — AI-Assisted English Learning Animation Studio

**Tagline:** Learn English Through Stories  
**Episode 001:** English at the Airport  
**Audience:** English learners worldwide; British English dialogue with Afghan Dari subtitles only  
**Level:** CEFR A1–A2  
**Target runtime:** 7 minutes  
**Delivery target:** 16:9, 1920×1080, 30 fps, H.264 MP4

## Approved production settings

The source of truth is `project-settings.json`:
- British English dialogue (en-GB).
- Afghan Dari subtitles only; no Dari voiceover.
- Local/offline Piper TTS; no paid API or cloud generation.
- Hybrid visuals: pursue premium cinematic 3D where practical; use polished 2.5D as an honest fallback.
- GPU acceleration is optional; the workflow must remain usable without a discrete GPU.
- Keep Leo, Emma, and Ollie visually consistent and retain Gate 12.

## Current production status

The project has a validated production package and a working render/tooling foundation. It is **not yet a finished episode**.

### Completed and committed
- Episode script, learning sections, and 18-shot production plan.
- Leo, Emma, and Ollie character bible and canonical outfit descriptions.
- Five original airport SVG scene plates and three animated SVG character rigs.
- English and Afghan Dari SRT subtitle guides with 48 aligned cue boundaries.
- A 48-cue English voice manifest with role assignments.
- Local British English Piper generator, checksum-verified VCTK multi-speaker model downloader, role-specific speaker map, and English WAV assembler.
- End-to-end offline audio pipeline tests using a deterministic fake Piper executable; these test software behavior, not real voice quality.
- Voice WAV validator configured for 48 English files only; Afghan Dari remains subtitle-only.
- FFmpeg/CairoSVG 7-minute scene-plate review renderer with optional English audio and selectable English/Dari subtitle tracks.
- 4K YouTube thumbnail artwork/export and vertical Shorts cover artwork/export.
- Dependency-free source validation and GitHub Actions checks.
- Procedural Blender 3D character/airport look-development scene. Its successful PNG render is a still style test, not a finished animated shot.

### Still required before release
- Download the pinned multi-speaker British English VCTK model (checksum verification and CC BY 4.0 attribution note are automated; model weights remain local and are not committed).
- Complete the 48-cue audio-generation workflow, then listen to and approve all English WAV clips.
- Retiming both subtitle files against the actual English recordings.
- Create and review final character animation, including appropriate dialogue timing and visual continuity.
- Complete the sound mix, full 1080p export, and human quality review.
- Review the final thumbnail and all asset/model licenses before YouTube publication.

## Quick start

From the repository root:

1. Validate source assets:
   ```bash
   python tools/video-pipeline/validate_episode.py
   ```
2. Run the offline pipeline tests (no voice model or API needed):
   ```bash
   python -m unittest tools/tts/test_local_audio_pipeline.py -v
   ```
3. Install Piper and download the pinned British English multi-speaker voice model (the script verifies file hashes and saves attribution):\n   `python tools/tts/download_british_voice.py`\n   Read `tools/tts/LOCAL_TTS.md` for voice casting and license details.
4. Generate a short audition:
   ```bash
   python tools/tts/generate_local_english.py --model models/piper/en_GB-vctk-medium/en_GB-vctk-medium.onnx --voices-json tools/tts/episode-001-voices.json --limit 6
   ```
5. After listening and license approval, generate all cues:
   ```bash
   python tools/tts/generate_local_english.py --model models/piper/en_GB-vctk-medium/en_GB-vctk-medium.onnx --voices-json tools/tts/episode-001-voices.json
   python tools/tts/validate_voice_assets.py --strict
   python tools/tts/build_english_track.py
   python tools/tts/retime_subtitles.py
   ```
6. Render a visual review cut. Once subtitles are retimed and the English WAV is approved:
   ```bash
   python tools/video-pipeline/render_episode.py \
     --english-audio build/audio/episode-001-en.wav \
     --subtitles-en build/subtitles/episode-001-en-retimed.srt \
     --subtitles-fa build/subtitles/episode-001-fa-retimed.srt
   ```
7. Export the long-form thumbnail and Shorts cover:
   ```bash
   python tools/video-pipeline/render_thumbnail.py
   python tools/video-pipeline/render_shorts_cover.py
   ```

## Quality and rights principles

- Do not publish provisional subtitle timings as synchronized captions.
- Do not describe SVG motion or a 2.5D composite as full 3D animation.
- Attribute the VCTK Corpus under CC BY 4.0 as documented in the downloaded model card and `ATTRIBUTION.txt`.
- Use only music, voices, fonts, images, and video assets cleared for the intended commercial use.
- AI use alone does not guarantee or prevent YouTube monetization; each episode must provide original educational value and meaningful editing.
- Do not call the episode complete until the final MP4, audio, subtitles, and visual quality checks pass.

## Repository guides

- `project-settings.json` — approved settings.
- `production-workflow.md` — end-to-end workflow.
- `episodes/001-english-at-the-airport/production-status.md` — episode checklist and release gates.
- `tools/tts/LOCAL_TTS.md` — offline British English voice generation.
- `tools/video-pipeline/README.md` — FFmpeg renderer and subtitle muxing.
- `tools/blender/README.md` — procedural 3D look-development.
