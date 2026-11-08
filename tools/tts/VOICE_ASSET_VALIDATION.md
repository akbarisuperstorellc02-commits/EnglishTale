# Voice asset validation

Run the non-strict validator at any time, including before audio has been generated:

\`\`\`bash
python tools/tts/validate_voice_assets.py
\`\`\`

Missing recordings are reported as **pending** and do not fail the source-package check. Once all 96 files have been generated, run the release gate:

\`\`\`bash
python tools/tts/validate_voice_assets.py --strict
\`\`\`

The validator uses only Python's standard library. It checks the 48-cue bilingual manifest, safe in-repository paths, WAV readability, uncompressed 16-bit PCM, supported 24/44.1/48 kHz rates, mono/stereo channels, non-empty/non-silent audio, consistent format within each language, and clip duration against each provisional cue slot (120 ms default tolerance).

A successful technical check does not approve pronunciation, voice identity, acting, or Afghan Dari dialect. Listen to all 96 clips and retime captions against the final audio before assembly. The audio assembler normalizes accepted clips to 48 kHz stereo.
