# TTS tools — active and legacy paths\n\n**Active project decision:** British English audio generated locally with Piper; Afghan Dari is subtitles only. Use [LOCAL_TTS.md](LOCAL_TTS.md). No paid API or cloud key is required for the active workflow. The voice model's own license must be reviewed before commercial use.\n\nThe Gemini and ElevenLabs sections below are retained as historical optional alternatives only; they are not the current production path.\n\n---\n\n# Gemini TTS voice generation

This optional tool generates one WAV per voice-manifest cue and language. It supports resume: existing clips are skipped unless `--overwrite` is supplied.

## Setup

Python 3.10+ is required.

```bash
python -m pip install -r tools/tts/requirements.txt
```

Set `GEMINI_API_KEY` in your local environment. Never put the key in this repository, a script, a screenshot, or a GitHub Actions secret for this manual production workflow.

PowerShell example (current terminal only):

```powershell
$env:GEMINI_API_KEY = "YOUR_API_KEY"
python tools/tts/generate_gemini_tts.py --language both --cue-ids 1,4,5,11,24,34
```

This representative set auditions Narrator, Leo, Emma, Airport Agent, Security Officer, and Ollie, plus the single Dari explainer voice. Review every sample before generating the remaining clips:

```powershell
python tools/tts/generate_gemini_tts.py --language both
```

Generate only one language if desired:

```powershell
python tools/tts/generate_gemini_tts.py --language en
python tools/tts/generate_gemini_tts.py --language fa
```

Use `--dry-run` to list selected outputs without sending an API request. Use `--start-id 10 --limit 5` to resume a selected range. Existing clips are skipped by default.

## Voice casting

Initial English voice assignments are in `voices.json`. They are audition candidates, not approved final casting. Generate a few samples and listen before producing the complete set. Dari uses one consistent voice and a style instruction requesting Afghan Dari/Kabul pronunciation. A native Dari speaker should review the result.

## Model and language support

The configured model is `gemini-3.8-flash-tts`. Google's current TTS language list explicitly includes English and Persian (Afghanistan). However, Google's official Gemini API supported-region list currently does not include Afghanistan. This backend is only an option if the user's API account and calling environment are legitimately in a supported region; do not assume it will work from Afghanistan. The model detects input language automatically; the Afghan Dari style instruction is only guidance and does not guarantee a perfect regional accent.

For an alternative, see `tools/tts/elevenlabs-README.md`. ElevenLabs advertises Persian TTS and has a paid plan with a commercial license, but the selected Persian voice still needs Afghan Dari audition.

## Cost and data-use caution

Check the current official pricing before generation. The published Gemini TTS pricing lists a free tier, but free-tier inputs/outputs may be used to improve Google products; paid-tier data is listed as not used for product improvement. The paid price shown for Gemini 3.8 Flash TTS is currently an output-token rate, so the final bill depends on actual generated audio tokens and text. Prices may change.

The Google Gemini API terms state Google does not claim ownership of generated content, while responsibility for legal use remains with the user. Confirm current terms, regional availability, account age requirements, and YouTube/commercial suitability before production. Do not treat preview availability or a free quota as a permanent guarantee.

## Audio quality gate

- Keep each character's voice identity consistent across all lines.
- Check names, contractions, airport vocabulary, stress, and sentence endings.
- Confirm Dari pronunciation with a native Afghan Dari speaker.
- Reject clipped, robotic, or mispronounced lines and regenerate them.
- Do not force speech into a provisional slot by speeding it up; update the SRT/manifest after reviewing actual audio duration.
- Only after all clips are approved, run `python tools/video-pipeline/build_audio_tracks.py`.
