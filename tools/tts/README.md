# TTS tools

## Active production path

Episode 001 uses **British English audio generated locally with Piper TTS**. Afghan Dari is subtitle-only. No paid API, cloud key, or internet connection is required during speech generation after the model has been obtained.

Read [LOCAL_TTS.md](LOCAL_TTS.md) for installation, model setup, audition, and full generation instructions.

Main tools:
- `generate_local_english.py` — generate the 48 English cue WAV files locally.
- `validate_voice_assets.py` — validate the 48 English WAV files; use `--strict` before assembly.
- `build_english_track.py` — assemble the approved cues into a 7-minute English WAV.
- `test_local_audio_pipeline.py` — run an offline end-to-end test with a fake Piper executable.

The British English voice model is not bundled in the repository. Its individual model card and license must be reviewed before commercial publication. The Piper software license does not automatically grant rights to each voice model.

## Historical alternatives

The Gemini and ElevenLabs scripts and notes are retained for historical reference only. They are **not** part of the approved production workflow and must not be used to introduce paid/cloud dependencies into the active build.
