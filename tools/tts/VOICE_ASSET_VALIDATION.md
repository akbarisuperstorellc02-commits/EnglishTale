# English voice asset validation

The active Episode 001 release uses **48 British English WAV files**. Afghan Dari is subtitle-only; no Dari voice files are expected.

Run the non-strict validator at any time:

```bash
python tools/tts/validate_voice_assets.py
```

Missing English recordings are reported as pending and do not fail source-package checks. Before assembly, use the strict release gate:

```bash
python tools/tts/validate_voice_assets.py --strict
```

The standard-library validator checks:
- 48 sequential cue IDs and valid cue timing.
- Safe in-repository English WAV paths.
- WAV readability, uncompressed 16-bit PCM, mono/stereo audio.
- Supported native sample rates: 22050, 24000, 44100, or 48000 Hz.
- Non-empty, non-silent recordings.
- Consistent audio format across the English clips.
- Clip duration against each provisional cue slot (120 ms default tolerance).

The end-to-end pipeline test uses a deterministic fake Piper executable. It verifies software behavior only; it does not approve voice quality.

A successful technical check does not approve pronunciation, acting, character voice identity, or subtitle synchronization. Listen to all 48 clips and retime both SRT files against the approved English audio before final assembly. The assembler preserves the model's sample rate.
