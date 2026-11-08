# Episode 001 English Voice Recording Package

The manifest contains **48 English dialogue/narration cues**. Each cue has a role, English text, provisional start/end time, and English WAV filename. Afghan Dari text is retained for subtitle validation only; there is no Dari voice recording.

## Recording file locations

Save the reviewed English clips at the paths listed in `voice-manifest.json`:

- English: `audio/episode-001/en/001.wav` through `048.wav`
- Afghan Dari: `subtitles-fa.srt` only; do not create Dari WAV files.

Create the English folder locally; Git does not retain empty folders. Use uncompressed 16-bit PCM WAV. Preserve the Piper model's native sample rate (commonly 22050 Hz for this voice family), mono output preferred. Do not upload private voice samples or provider credentials.

## Voice consistency

- Narrator: warm, clear British English.
- Leo: young adult male, curious and slightly nervous early in the story.
- Emma: young adult female, reassuring and upbeat.
- Airport agent: professional and polite.
- Security officer: neutral and concise.
- Ollie: cheerful guide voice.

A single stable British English voice model is the default. Distinct role models are optional; each must be locally available, auditioned, and individually cleared for commercial use. Listen to every clip and reject clipped words, unnatural stress, mispronunciations, or abrupt endings.

## Generate and validate

Read `tools/tts/LOCAL_TTS.md` for Piper installation and model licensing.

Generate a six-line audition first:

```bash
python tools/tts/generate_local_english.py --model /path/to/en_GB-alan-medium.onnx --limit 6
```

After listening and approving the model, generate all cues:

```bash
python tools/tts/generate_local_english.py --model /path/to/en_GB-alan-medium.onnx
python tools/tts/validate_voice_assets.py --strict
```

The validator checks 48 English WAV files for readability, PCM format, sample rate, channel count, silence, consistent format, safe paths, and duration against provisional cue slots. It cannot judge pronunciation or performance.

## Assemble and retime

After all 48 English WAV files pass strict validation:

```bash
python tools/tts/build_english_track.py
python tools/tts/retime_subtitles.py
```

The assembler creates `build/audio/episode-001-en.wav`. The retiming helper creates separate English and Afghan Dari SRT files using measured WAV durations plus a small reading tail. This is a duration-based first pass, not phoneme-level alignment; listen to the full audio and manually review both subtitle files.

## Critical timing note

The 48 cue slots are editorial estimates, not waveform measurements. If a generated clip does not fit its slot, do not speed up speech unnaturally or cut off words. Revise the timing plan and subtitle boundaries, then regenerate/reassemble as needed.
