# Generate voice assets through GitHub Actions

This workflow is manual and never runs on ordinary pushes.

## One-time secure setup

1. In the repository, open **Settings → Secrets and variables → Actions → New repository secret**.
2. Name the secret exactly \`ELEVENLABS_API_KEY\` and paste the key there. Do not commit it or put it in chat.
3. Open \`tools/tts/elevenlabs-voices.json\` and fill the English role voice IDs and the Persian-capable Dari voice ID from your own ElevenLabs account. Voice IDs must be chosen and auditioned by the project owner. Do not assume a Persian voice is Afghan Dari.
4. Commit the voice ID configuration only after selecting the actual voices.

## Run it

Open **Actions → Generate Episode 001 voice assets → Run workflow**.

- \`list-voices\`: prints the account's available voice names and IDs in the workflow log. This does not generate audio.
- \`audition-samples\`: generates 12 WAV samples (six selected cues in English and Dari). Download the artifact and listen before approving casting.
- \`generate-all\`: generates all 96 clips, runs strict technical validation, assembles both language tracks, and uploads the audio artifact. It stops if any clip is missing, invalid, silent, or longer than its provisional slot.

The generated artifact is retained for 14 days. Download it and keep a separate backup. The workflow does not commit audio files or secrets into the repository.

## Important approval gate

Do not run \`generate-all\` until the English voices and the Afghan Dari accent have been auditioned and approved. Technical validation cannot determine whether a Dari voice sounds authentically Afghan. The cue timings are provisional; if a generated line exceeds its slot, the workflow stops rather than silently speeding up or cutting off speech.
