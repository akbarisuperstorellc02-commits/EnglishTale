# Episode 001 Voice Recording Package

The recording manifest contains 48 cue pairs. Each cue has:
- An English line assigned to a character/narrator role.
- An Afghan Dari equivalent for the separate explanation track.
- A provisional start/end time and exact WAV filename.

## Recording file locations

Save the reviewed clips at the paths listed in `voice-manifest.json`:

- English: `audio/episode-001/en/001.wav` through `048.wav`
- Dari: `audio/episode-001/fa/001.wav` through `048.wav`

Create the folders locally; Git does not retain empty folders. WAV PCM is preferred (44.1 or 48 kHz, mono or stereo). Do not upload private voice samples or provider credentials.

## Voice consistency
- Narrator: warm, clear, neutral English.
- Leo: young adult male, curious and slightly nervous early in the story.
- Emma: young adult female, reassuring and upbeat.
- Airport agent: professional, polite.
- Security officer: neutral and concise.
- Ollie: cheerful guide voice.
- Dari track: one natural Afghan Dari explainer voice, with consistent pronunciation.

Keep one voice identity for each role across all cues. Listen to every clip and reject clipped words, unnatural stress, mispronunciations, or abrupt endings. Verify that the TTS provider's selected plan explicitly allows commercial YouTube use before production.

## Validate the recordings

After generating clips, run the technical validator:

```bash
python tools/tts/validate_voice_assets.py
```

Missing clips are reported as pending. Before assembly, require all 96 valid clips:

```bash
python tools/tts/validate_voice_assets.py --strict
```

The validator checks PCM WAV integrity, 16-bit depth, supported sample rates, mono/stereo channels, silence, consistent formats, safe file paths, and cue-slot duration. It cannot judge pronunciation or performance; listen to every clip and confirm Afghan Dari with a native speaker.

## Assemble the two tracks

After all 96 WAV clips pass strict validation and are approved by listening:

```bash
python tools/video-pipeline/build_audio_tracks.py
```

The tool creates:
- `build/audio/episode-001-en.wav`
- `build/audio/episode-001-fa.wav`

It refuses to assemble if any clip is missing or longer than its provisional slot. Short clips are padded with silence to keep the provisional 07:00 timeline. This does not replace human listening or subtitle retiming.

## Critical timing note

The 48 slots are editorial estimates, not waveform measurements. Natural dialogue may require longer or shorter timing. If clips do not fit, update the SRT timecodes and voice manifest after listening; never speed up speech unnaturally or cut off words just to satisfy the current guide.
