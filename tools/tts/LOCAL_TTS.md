# Local English voice generation (current project setting)

The active project setting is **British English audio + Afghan Dari subtitles only**. No Dari voice track is generated. No cloud API key or paid TTS API is required.

## Engine

Use Piper TTS locally on CPU. A compatible GPU is optional; the unknown GPU model must not block audio generation.

Install in a Python virtual environment:

```bash
python -m pip install piper-tts
```

Obtain a British English Piper voice model (the default expected filename is `en_GB-alan-medium.onnx`) and its matching `.onnx.json` configuration from the official Piper voice collection. Keep the model outside Git and check the individual voice model card and license before any commercial YouTube use. The Piper software license does not automatically grant rights to every voice model.

Generate a six-line audition first:

```bash
python tools/tts/generate_local_english.py --model /path/to/en_GB-alan-medium.onnx --limit 6
```

If the audition passes listening review, generate all English cues:

```bash
python tools/tts/generate_local_english.py --model /path/to/en_GB-alan-medium.onnx
```

The script is resumable. Existing cue WAV files are skipped; pass `--overwrite` to replace them. It writes only English WAV files to `build/audio/episode-001/en/`.

## Character voice casting

For a consistent single British voice, omit `--voices-json`. For distinct character voices, supply a JSON object mapping role names (Narrator, Leo, Emma, Airport Agent, Security Officer, Ollie) to locally installed, individually licensed British English Piper model paths. All models must be reviewed and auditioned before full generation.

## Release checks

- Listen to every line for natural pronunciation, pacing, clipping, and role consistency.
- Verify that each model's license permits the intended commercial use.
- Retiming the English captions against the actual audio is mandatory.
- Keep `subtitles-fa.srt` as the Dari learning support. It is not an audio track.
- Do not claim final audio or a finished episode until the complete audio and video have passed human review.
