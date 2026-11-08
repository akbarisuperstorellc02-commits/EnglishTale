# Voice and Sound Production

## Voice roles

| Role | Voice direction | Notes |
|---|---|---|
| Narrator | Warm, clear British English; medium pace | Neutral, welcoming, not overly theatrical |
| Leo | Young adult male; curious, slightly nervous at first | Natural conversational delivery |
| Emma | Young adult female; supportive, upbeat | Calm and reassuring |
| Airport agent | Adult; polite, professional | Clear enunciation |
| Security officer | Adult; neutral and courteous | Short, direct instructions |
| Ollie | Cheerful, friendly guide | Slightly playful, still clear |

Use one consistent British English voice model by default. Distinct role models are optional and must each be locally available, auditioned, and individually cleared for commercial use. Do not create a Dari voice role: Afghan Dari is subtitles only.

## Local recording / TTS workflow
1. Generate one English line per WAV file from the 48-cue manifest.
2. Keep the voice identity and speaking style consistent throughout the episode.
3. Listen to every line for British pronunciation, stress, natural pacing, clipping, and clean sentence endings.
4. Regenerate any line that is unclear, robotic, or mispronounced.
5. Preserve the voice model's native sample rate; do not resample blindly.
6. Retiming both English and Afghan Dari subtitle files against the final English audio is mandatory.

## Mix targets
- Dialogue must be clearly intelligible on a phone speaker.
- Keep music well below dialogue; duck it during all spoken lines.
- Avoid clipping and leave headroom on the master.
- Use gentle noise reduction only when needed; avoid metallic artifacts.
- Add subtle airport ambience only in establishing shots and keep it quiet.
- Do not use recognizable copyrighted songs or unlicensed sound effects.

## Free / low-cost approach
Use local Piper TTS and original procedural visual assets. Use only music and sound effects with documented commercial-use permission. Never assume “free to generate” means “free for commercial use.”
