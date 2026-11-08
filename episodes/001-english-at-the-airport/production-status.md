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
- [x] Audio assembler added to build the 7-minute British English WAV track from reviewed cue recordings; Dari remains subtitle-only.
- [x] Validator extended to check voice-manifest alignment with both SRT tracks.
- [x] Original 16:9 vector thumbnail artwork added, using the canonical blue Leo / pink Emma / owl Ollie identities; export upgraded to YouTube's recommended 3840×2160 resolution.
- [x] Thumbnail PNG export script added.
- [x] Thumbnail PNG validator checks 3840×2160 dimensions and desktop upload size; warns when mobile's 2 MB limit is exceeded.
- [x] A separate 9:16 Shorts cover and 2160×3840 renderer/validator added; both thumbnail formats are now checked and uploaded by CI.
- [x] FFmpeg renderer corrected to avoid multiplying frames on still-image zoom shots.
- [x] MP4 export supports selectable English and Afghan Dari audio tracks.
- [x] Audio assembler preserves any intentional subtitle timeline gaps with silence.
- [x] GitHub Actions run #20 passed: Python compile, source validation, thumbnail render, and artifact upload.
- [x] Resumable Gemini TTS generator added for 48 English and 48 Dari cue files.
- [x] ElevenLabs TTS fallback generator added with voice-listing and WAV conversion.
- [x] Provider research updated: Gemini API regional restriction and ElevenLabs commercial-plan caveat documented.
- [x] Both TTS generators support a six-role audition sample set before full generation.
- [x] CI smoke-tests both TTS generators in dry-run mode without API keys.
- [x] Expanded validator checks shot IDs/durations, voice roles and paths, bilingual subtitle text/timing, Gate 12, scene dimensions, and SVG XML.
- [x] GitHub Actions run #68 passed all compile, validation, TTS smoke, 4K thumbnail render, 3840×2160 dimension validation, and artifact upload. The generated 4K PNG artifact is 354,197 bytes (within YouTube's 2 MB mobile upload limit). [Open run #68](https://github.com/akbarisuperstorellc02-commits/EnglishTale/actions/runs/42496181400).
- [x] Vertical Shorts cover artwork, 2160×3840 renderer, and PNG validator added; CI now exports and checks both cover formats.
- [x] GitHub Actions run #75 passed the full pipeline and uploaded both thumbnail previews as one 827,839-byte artifact. [Open run #75](https://github.com/akbarisuperstorellc02-commits/EnglishTale/actions/runs/42496255600).
- [x] Vertical Shorts cover added to the asset license log.
- [x] Four vertical YouTube Shorts cutdown plans prepared for post-release promotion.
- [x] Dependency-free voice asset validator added for the 48 English WAV clips, including strict release mode and unit tests.
- [x] CI now runs voice validator unit tests and reports missing recordings as pending without falsely failing the source-package build.
- [x] English audio assembly automatically blocks until all 48 English WAV clips pass strict technical validation.

## Quality notes
- Subtitle timestamps are editorial estimates, not measured against recorded audio.
- Animated SVG mouth movement is a placeholder; it is not phoneme-accurate lip sync.
- The five scene plates are static vector backgrounds. They are not a rendered animation.
- The voice and sound plan is documentation only. No voice audio files have been generated yet.
- The script targets seven minutes, but final runtime must be measured after narration and dialogue are recorded.

## Automation and local tooling
- Run `python tools/video-pipeline/validate_episode.py` to validate source assets, subtitle/timeline integrity, and voice-manifest alignment.
- The voice manifest contains 48 English dialogue cues. Afghan Dari text is retained only to cross-check the 48-cue Dari subtitle file; no Dari WAV files are expected.
- Run `python tools/tts/validate_voice_assets.py` to inspect available clips; run `python tools/tts/validate_voice_assets.py --strict` before audio assembly to require all 48 technically valid English WAVs.
- TTS generation tools are ready, but API credentials and user-selected voice IDs are not present. Gemini API's official supported-region list excludes Afghanistan; ElevenLabs is the practical alternative to audition, but Persian output must pass Afghan Dari review.
- Export the vector thumbnail with `python tools/video-pipeline/render_thumbnail.py` (CairoSVG required).
- Once all 48 English clips are generated and reviewed, run `python tools/tts/build_english_track.py` to assemble the English WAV track.
- Run `python tools/video-pipeline/render_episode.py` to create a silent visual review cut. FFmpeg, FFprobe, and CairoSVG must be installed locally.
- For an MP4 with British English audio and selectable subtitles, use `--english-audio build/audio/episode-001-en.wav --subtitles-en episodes/001-english-at-the-airport/subtitles-en.srt --subtitles-fa episodes/001-english-at-the-airport/subtitles-fa.srt`.
- GitHub Actions run #65 completed successfully. It compiled all tools, passed the expanded episode validator, smoke-tested both TTS generators without API credentials, rendered and validated the 1280×720 PNG thumbnail, and uploaded the thumbnail artifact. [Open run #65](https://github.com/akbarisuperstorellc02-commits/EnglishTale/actions/runs/42495946177).

## Next production sequence
1. Confirm an accessible TTS provider and a plan with commercial-use rights; audition the Persian voice for natural Afghan Dari before committing.
2. Generate and audition each English character/narrator line separately.
3. Keep Afghan Dari as a separate subtitle track; do not generate Dari narration.
4. Replace placeholder pauses with real timing and retime both subtitle tracks to the final audio.
5. Render character and scene animation, then assemble a low-resolution review cut.
6. Fix timing, pronunciation, visual continuity, sound mix, and caption readability.
7. Render the final 1080p master and create the thumbnail.

## Release gate
Do not publish until voice licensing, asset licensing, pronunciation, subtitle timing, and the full video review are complete.


## Approved settings — 2026-11-08
- [x] User approved British English as the spoken accent.
- [x] User approved Afghan Dari subtitles only; Dari voiceover is disabled.
- [x] User approved local/offline audio generation; paid or cloud TTS APIs are not part of the active workflow.
- [x] User approved a hybrid visual pipeline: pursue a premium cinematic 3D look where feasible, with high-quality 2.5D compositing and controlled camera/character motion as the honest fallback.
- [x] GPU model is unknown; audio generation and the fallback visual workflow must work without GPU acceleration.
- [x] Machine-readable settings committed at `project-settings.json`.
- [x] Local Piper British English TTS generator committed at `tools/tts/generate_local_english.py`.
- [x] Local TTS setup, model-license checks, audition, and generation guide committed at `tools/tts/LOCAL_TTS.md`.

## Current blockers / release gates
- The British English Piper voice model has not yet been downloaded or auditioned. Its individual model license must be checked before commercial publication.
- The final English audio files do not yet exist. The manifest has 48 English cue files; its Dari text fields are subtitle references only and do not imply Dari voice generation.
- Subtitle timestamps are provisional and must be retimed to the generated English audio.
- The six-second SVG render is only a technical test. It is not the seven-minute episode master and not a 3D animation.
- Full 3D rendering is not promised until the machine's capabilities are known; the hybrid fallback remains available without a discrete GPU.
