# ElevenLabs TTS — Afghanistan-friendly fallback candidate

The Gemini API generator is included as an optional backend, but Google's official AI Studio/Gemini API supported-region list currently does not include Afghanistan. Do not assume that Gemini API calls will work from Afghanistan.

ElevenLabs offers Persian TTS and an API. Its current pricing page lists a Starter plan with a commercial license and 30,000 monthly credits; the Free plan has 10,000 credits but does not include a commercial license. Confirm current price and account availability before paying.

## Setup

1. Confirm ElevenLabs is accessible from your account and country.
2. Select a Persian-capable voice for Dari and distinct English voices for the character roles.
3. Subscribe to a plan whose current terms include commercial use before generating assets intended for monetized YouTube publication.
4. Create an API key and set it only in your local terminal:

```powershell
$env:ELEVENLABS_API_KEY = "YOUR_API_KEY"
```

5. List voices available to your account:

```powershell
python tools/tts/generate_elevenlabs_tts.py --list-voices
```

6. Copy chosen voice IDs into `elevenlabs-voices.json`. The file intentionally starts with blank IDs; no voice ID is invented.
7. Generate two sample cues first:

```powershell
python tools/tts/generate_elevenlabs_tts.py --language both --limit 2
```

8. Listen and review. If the Dari voice sounds Iranian rather than Afghan, reject it and select another voice. Do not proceed to all 96 clips until the sample is approved.
9. Generate the complete package:

```powershell
python tools/tts/generate_elevenlabs_tts.py --language both
```

The script saves WAV files into the exact paths in the voice manifest. It resumes by skipping existing clips. FFmpeg is required for MP3-to-WAV conversion.

## API behavior

- Uses the official `POST /v1/text-to-speech/{voice_id}` endpoint and `eleven_multilingual_v2` by default.
- Converts returned MP3 audio to mono 24 kHz PCM WAV for the existing audio assembly tool.
- Requires voice IDs from the user's account.
- Does not create voice clones or use another person's voice without permission.
- Never commit `ELEVENLABS_API_KEY`, voice samples, or private account exports.

## Important language limitation

ElevenLabs' Persian TTS page advertises Persian, but that does not prove the selected voice speaks Afghan Dari naturally. The user must audition the output and obtain native Afghan Dari review before release.
