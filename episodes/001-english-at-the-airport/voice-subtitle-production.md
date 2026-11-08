# Episode 001 — Voice & Subtitle Production

## Current deliverables
- `subtitles-en.srt`: English subtitle guide covering the 7-minute editorial timeline.
- `subtitles-fa.srt`: Afghan Dari subtitle guide aligned cue-for-cue with English.
- Both subtitle tracks contain 48 cues and can be muxed as selectable subtitle streams in the MP4.

## Approved language policy
- Generate British English audio only.
- Afghan Dari is subtitles only. Do not generate a Dari voiceover or Dari WAV track.
- English is the main learning audio; Dari captions support comprehension.

## Timing workflow
The committed SRT files are editorial timing guides, not waveform-verified captions. After the 48 English WAV clips are generated and reviewed:

1. Assemble the English track with `python tools/tts/build_english_track.py`.
2. Run `python tools/tts/retime_subtitles.py` to derive first-pass cue ends from measured WAV durations.
3. Listen to the complete English track and manually review both generated SRT files. The helper is duration-based, not phoneme-level speech recognition.
4. Render with the approved English WAV and retimed subtitle tracks.

## Voice generation order
1. Narrator hook and scene transitions.
2. Leo and Emma dialogue.
3. Airport agent and security officer announcements.
4. Ollie recap, repeat-after-me prompts, quiz, and closing.

## Recording rules
- Export each English line separately as WAV.
- Keep one stable voice identity per character.
- Say “Gate Twelve” in spoken English; display “Gate 12” in captions and graphics.
- Leave learner repetition pauses silent; do not read pause instructions aloud.
- Listen to every generated clip before editing. Correct pronunciation, clipped endings, unnatural stress, and inconsistent character voices.
- Keep the Afghan Dari subtitle track separate from English captions; do not overlap it as a second narration.

## Current limitation
No final voice audio has been generated or uploaded yet. This repository contains the script, subtitle guides, character artwork, shot plan, and production tools—not a finished seven-minute MP4.
