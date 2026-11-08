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
- A first set of 48 real English cue WAVs was generated and technically validated; the boarding-pass quiz wording has since been corrected in the voice manifest and both subtitle tracks, and the updated audio is being regenerated.
- FFmpeg/CairoSVG 7-minute scene-plate renderer; both a 420-second 720p review MP4 and a 420-second 1080p30 H.264 master candidate with loudness-normalized AAC English dialogue and selectable English/Dari subtitles passed technical validation. The earlier 1080p candidate used the SVG 2.5D fallback. All 18 procedural Blender 3D stills have passed 1920×1080 validation; the new hybrid master render is in progress. The current cut is dialogue-only; music/ambience and final sound design remain release-stage decisions.
- [Download the 1080p30 master candidate, 720p review, English WAVs, retimed subtitles, and VCTK attribution](https://github.com/akbarisuperstorellc02-commits/EnglishTale/actions/runs/42504752349/artifacts/13626009753).
- Initial 4K thumbnail and vertical Shorts artwork/export; a new post-render workflow now creates matching 3D-character thumbnail and Shorts artwork from the approved Blender stills.
- YouTube title, description, chapter markers, tags, pinned comment, VCTK attribution, and upload checklist in `episodes/001-english-at-the-airport/youtube-publishing-package.md`.
- Dependency-free source validation and GitHub Actions checks.
- Procedural Blender 3D character/airport scene with a validated 1280×720 look-development still, an 18-angle 1920×1080 shot library, and a separate two-second 640×360 character motion-study MP4. The still library supports the hybrid master with 2.5D camera motion; it is not continuous full-3D character animation.
- [Download the 3D look-development still and motion-study MP4](https://github.com/akbarisuperstorellc02-commits/EnglishTale/actions/runs/42504752366/artifacts/13626574637).

### Still required before release
- Listen to and approve all 48 generated English WAV clips for pronunciation, acting, pacing, and role consistency.
- Manually review both WAV-duration-retimed subtitle files against the actual English recordings.
- Complete and validate the 1080p master render from the 18 Blender 3D stills; complete dialogue-specific character animation and visual continuity. The Blender motion study is only a short technical preview.
- Human-review the 720p review cut and 1080p30 master candidate with sound and muted; revise visual/timing issues and decide whether additional sound design is needed before publication.
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
3. Install Piper and download the pinned British English multi-speaker voice model (the script verifies file hashes and saves attribution):
   ```bash
   python tools/tts/download_british_voice.py
   ```
   Read `tools/tts/LOCAL_TTS.md` for voice casting and license details.
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

## Windows PowerShell 5.1

A one-command local build script is provided:

```powershell
.\tools\windows\build_episode_001.ps1
```

Use `-SkipVideo` to generate and validate audio/subtitles without FFmpeg, or `-Overwrite` to regenerate all English voice clips. The script creates a local virtual environment, downloads the pinned voice model, builds the English audio and retimed subtitles, and renders the 720p review plus 1080p30 master candidate when FFmpeg is installed. If Blender is also installed, it renders and uses the 18-shot 3D library; otherwise it clearly falls back to the SVG 2.5D shot list.

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
- `publishing/youtube-metadata-episode-001.md` — title, description, chapters, tags, attribution, and upload checklist.
