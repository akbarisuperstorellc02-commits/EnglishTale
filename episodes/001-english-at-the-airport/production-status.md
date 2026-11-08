# EnglishTale — Episode 001 Production Status

Last updated: 2026-11-08

## Completed
- [x] Approved story script and character identities.
- [x] Five original coded vector scene plates (1280×720).
- [x] Three original animated SVG character rigs.
- [x] Gate signage corrected to Gate 12 to match the script.
- [x] Eighteen-shot production/edit plan covering 00:00–07:00.
- [x] English subtitle guide with 48 cues.
- [x] Afghan Dari subtitle guide with 48 matching cue boundaries.
- [x] Voice recording and subtitle synchronization instructions.
- [x] Repository README updated to reflect actual assets and remaining work.
- [x] Machine-readable 18-shot render timeline (420 seconds) committed.
- [x] FFmpeg/CairoSVG review-render script committed for local silent preview generation.
- [x] Dependency-free validator committed for shot timing, scene files, Gate 12, and subtitle alignment.
- [x] GitHub Actions validation workflow added for pushes and pull requests.
- [x] Bilingual 48-cue voice manifest created with role assignments and WAV file paths.
- [x] Audio assembler added to build separate 7-minute English and Dari WAV tracks from reviewed cue recordings.
- [x] Validator extended to check voice-manifest alignment with both SRT tracks.
- [x] Original 1280×720 vector thumbnail artwork added, using the canonical blue Leo / pink Emma / owl Ollie identities.
- [x] Thumbnail PNG export script added.
- [x] Thumbnail PNG dimension validator added to CI.
- [x] FFmpeg renderer corrected to avoid multiplying frames on still-image zoom shots.
- [x] MP4 export supports selectable English and Afghan Dari audio tracks.
- [x] Audio assembler preserves any intentional subtitle timeline gaps with silence.
- [x] GitHub Actions run #20 passed: Python compile, source validation, thumbnail render, and artifact upload.
- [x] Resumable Gemini TTS generator added for 48 English and 48 Dari cue files.
- [x] ElevenLabs TTS fallback generator added with voice-listing and WAV conversion.
- [x] Provider research updated: Gemini API regional restriction and ElevenLabs commercial-plan caveat documented.
- [x] Both TTS generators support a six-role audition sample set before full generation.
- [x] CI smoke-tests both TTS generators in dry-run mode without API keys.

## Quality notes
- Subtitle timestamps are editorial estimates, not measured against recorded audio.
- Animated SVG mouth movement is a placeholder; it is not phoneme-accurate lip sync.
- The five scene plates are static vector backgrounds. They are not a rendered animation.
- The voice and sound plan is documentation only. No voice audio files have been generated yet.
- The script targets seven minutes, but final runtime must be measured after narration and dialogue are recorded.

## Automation and local tooling
- Run `python tools/video-pipeline/validate_episode.py` to validate source assets, subtitle/timeline integrity, and voice-manifest alignment.
- The voice manifest lists 48 English cue files and 48 Dari cue files. No audio clips have been generated yet.
- TTS generation tools are ready, but API credentials and user-selected voice IDs are not present. Gemini API's official supported-region list excludes Afghanistan; ElevenLabs is the practical alternative to audition, but Persian output must pass Afghan Dari review.
- Export the vector thumbnail with `python tools/video-pipeline/render_thumbnail.py` (CairoSVG required).
- Once all clips are recorded and reviewed, run `python tools/video-pipeline/build_audio_tracks.py` to assemble two separate WAV tracks.
- Run `python tools/video-pipeline/render_episode.py` to create a silent visual review cut. FFmpeg, FFprobe, and CairoSVG must be installed locally.
- For one MP4 with selectable language audio, use `--english-audio build/audio/episode-001-en.wav --dari-audio build/audio/episode-001-fa.wav`.
- GitHub Actions run #20 completed successfully. It compiled the pipeline scripts, passed the episode/SVG/manifest validator, rendered the 1280×720 PNG thumbnail, and uploaded the thumbnail artifact.

## Next production sequence
1. Confirm an accessible TTS provider and a plan with commercial-use rights; audition Persian output for Afghan Dari before committing.
2. Generate and audition each English character/narrator line separately.
3. Generate the Dari explanation track separately if Dari narration is retained in the final edit.
4. Replace placeholder pauses with real timing and retime both subtitle tracks to the final audio.
5. Render character and scene animation, then assemble a low-resolution review cut.
6. Fix timing, pronunciation, visual continuity, sound mix, and caption readability.
7. Render the final 1080p master and create the thumbnail.

## Release gate
Do not publish until voice licensing, asset licensing, pronunciation, subtitle timing, and the full video review are complete.
