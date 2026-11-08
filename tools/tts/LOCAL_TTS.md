# Local English voice generation (approved project setting)

Episode 001 uses **British English audio + Afghan Dari subtitles only**. No Dari voiceover is generated. The active workflow is local/offline Piper TTS; no paid API or cloud service is needed during speech generation after the model has been downloaded.

## Engine and voice model

Install Piper in a Python virtual environment:

```bash
python -m pip install -r tools/tts/local-requirements.txt
```

The selected voice is `en_GB-vctk-medium`, a British English multi-speaker model with 109 speakers and a native 22,050 Hz sample rate. It allows distinct voice identities for Leo, Emma, the narrator, airport staff, and Ollie.

Download the pinned model, config, and model card with integrity checks:

```bash
python tools/tts/download_british_voice.py
```

The files are stored under `models/piper/en_GB-vctk-medium/`. The `models/` directory is git-ignored; voice weights are not committed to the repository.

## License and attribution

The VCTK model card lists the underlying VCTK dataset under **Creative Commons Attribution 4.0 International (CC BY 4.0)**. Commercial use is permitted with attribution and compliance with the license. The downloader saves the model card and an attribution note beside the model. Include the attribution in the episode description or credits:

> VCTK Corpus by CSTR, University of Edinburgh. Voice model: en_GB-vctk-medium from Piper Voices. Dataset licensed under CC BY 4.0.

Sources:
- Model files and speaker map: https://huggingface.co/rhasspy/piper-voices/tree/v1.0.0/en/en_GB/vctk/medium
- Model card: https://huggingface.co/rhasspy/piper-voices/blob/v1.0.0/en/en_GB/vctk/medium/MODEL_CARD
- Dataset license: https://creativecommons.org/licenses/by/4.0/

## Character voice casting

The committed role map is `tools/tts/episode-001-voices.json`. It assigns separate speaker IDs from the same multi-speaker British model:
- Narrator: p225 (female, southern English)
- Leo: p226 (male, Surrey)
- Emma: p228 (female, southern English)
- Airport Agent: p227 (male, Cumbria)
- Security Officer: p226 (male, Surrey)
- Ollie: p229 (female, southern English)

The numeric speaker IDs are mapped by the pinned Piper voice catalog. The generator supports a model path and optional `speaker_id` per role.

## Audition and generation

Generate a six-cue audition first:

```bash
python tools/tts/generate_local_english.py \
  --model models/piper/en_GB-vctk-medium/en_GB-vctk-medium.onnx \
  --voices-json tools/tts/episode-001-voices.json \
  --limit 6
```

Listen to the sample WAVs and confirm pronunciation, character differentiation, pacing, and voice quality. If approved, generate all 48 English cues:

```bash
python tools/tts/generate_local_english.py \
  --model models/piper/en_GB-vctk-medium/en_GB-vctk-medium.onnx \
  --voices-json tools/tts/episode-001-voices.json
```

The generator is resumable. Existing cue WAV files are skipped; pass `--overwrite` to replace them. Output is written to `build/audio/episode-001/en/`.

## Release checks and assembly

```bash
python tools/tts/validate_voice_assets.py --strict
python tools/tts/build_english_track.py
python tools/tts/retime_subtitles.py
```

- Strict validation requires all 48 English WAV clips to be valid, non-silent 16-bit PCM files with consistent sample format and durations that fit the provisional cue slots.
- The assembler creates `build/audio/episode-001-en.wav` and preserves the model's native sample rate.
- The retiming helper creates separate English and Afghan Dari SRT files using measured WAV durations plus a reading tail. This is a duration-based first pass, not phoneme-level alignment; listen to the complete audio and manually review both subtitle files.
- Keep `subtitles-fa.srt` as the Dari learning support. It is not an audio track.
