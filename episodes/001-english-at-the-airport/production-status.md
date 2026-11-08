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

## Quality notes
- Subtitle timestamps are editorial estimates, not measured against recorded audio.
- Animated SVG mouth movement is a placeholder; it is not phoneme-accurate lip sync.
- The five scene plates are static vector backgrounds. They are not a rendered animation.
- The voice and sound plan is documentation only. No voice audio files have been generated yet.
- The script targets seven minutes, but final runtime must be measured after narration and dialogue are recorded.

## Automation and local tooling
- Run `python tools/video-pipeline/validate_episode.py` to validate source assets, subtitle/timeline integrity, and voice-manifest alignment.
- The voice manifest lists 48 English cue files and 48 Dari cue files. No audio clips have been generated yet.
- Once all clips are recorded and reviewed, run `python tools/video-pipeline/build_audio_tracks.py` to assemble two separate WAV tracks.
- Run `python tools/video-pipeline/render_episode.py` to create a silent visual review cut. FFmpeg, FFprobe, and CairoSVG must be installed locally.
- The GitHub Actions workflow is configured, but its first hosted run has not yet been independently confirmed in this status update.

## Next production sequence
1. Select a TTS/voice workflow whose commercial-use license covers YouTube publication.
2. Generate and audition each English character/narrator line separately.
3. Generate the Dari explanation track separately if Dari narration is retained in the final edit.
4. Replace placeholder pauses with real timing and retime both subtitle tracks to the final audio.
5. Render character and scene animation, then assemble a low-resolution review cut.
6. Fix timing, pronunciation, visual continuity, sound mix, and caption readability.
7. Render the final 1080p master and create the thumbnail.

## Release gate
Do not publish until voice licensing, asset licensing, pronunciation, subtitle timing, and the full video review are complete.
