# English-only local audio assembly

The current release path is British English narration/dialogue with Afghan Dari subtitles only. This replaces the older bilingual audio assembler for active production.

## Generate and assemble

1. Install Piper and obtain a British English voice model. Review the model's license.
2. Generate an audition and listen:
   `python tools/tts/generate_local_english.py --model /path/to/en_GB-alan-medium.onnx --limit 6`
3. Generate the remaining cues:
   `python tools/tts/generate_local_english.py --model /path/to/en_GB-alan-medium.onnx`
4. Assemble the English track:
   `python tools/tts/build_english_track.py`

The assembler requires all 48 WAV clips, mono 16-bit PCM, a consistent sample rate, non-silent audio, and every line to fit its provisional cue slot. It preserves the 07:00 timeline with silence between dialogue cues. If a line does not fit, fix the audio or retime the episode and subtitles; never silently truncate speech.

After assembly, retime `subtitles-en.srt` to the actual spoken words. `subtitles-fa.srt` remains a separate Afghan Dari subtitle track and must be checked for readability and translation quality.
