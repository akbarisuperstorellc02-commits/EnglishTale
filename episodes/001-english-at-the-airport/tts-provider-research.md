# TTS provider research — 2026-11-08

Gemini 3.8 Flash TTS has the best explicit language match on paper because its official language list includes both English and Persian (Afghanistan). However, Google's official Gemini API supported-region list currently excludes Afghanistan. Therefore it is not the default practical route for a user operating from Afghanistan; use only if the account/calling environment is legitimately supported. It remains an optional backend, not a guarantee of natural Kabul Dari.

Practical fallback to audition: ElevenLabs Persian TTS. Its Starter plan currently advertises a commercial license and 30,000 monthly credits; Free has 10,000 credits but no commercial license. Persian support does not guarantee Afghan Dari pronunciation. Confirm service availability and review a sample with a native Afghan Dari speaker before buying or generating the full package.

Official references:
- Supported TTS languages and API usage: https://ai.google.dev/gemini-api/docs/speech-generation
- Gemini API supported regions (Afghanistan is not listed): https://ai.google.dev/gemini-api/docs/available-regions
- ElevenLabs Persian TTS: https://elevenlabs.io/text-to-speech/persian
- ElevenLabs current plan pricing and commercial license: https://elevenlabs.io/pricing
- ElevenLabs TTS API: https://elevenlabs.io/docs/api-reference/text-to-speech/convert
- Gemini API pricing (including free-tier data use and TTS rates): https://ai.google.dev/gemini-api/docs/pricing
- Gemini API additional terms: https://ai.google.dev/gemini-api/terms
- Google Cloud generative AI service terms: https://cloud.google.com/terms/service-terms

Research notes:
- Gemini 3.8 Flash TTS lists English and Persian (Afghanistan) among supported languages.
- The official pricing page currently shows a free tier, with content used to improve products; the paid tier is listed as not used for product improvement.
- Current published paid output pricing for Gemini 3.8 Flash TTS is $9 per 1M audio tokens through 2026-12-31 and $18 per 1M audio tokens from 2027-01-01. Audio tokenization is estimated by Google at 25 tokens per second. A 14-minute pair of 7-minute tracks would be roughly 21,000 audio tokens, or about $0.19 at the current rate, excluding input tokens and retries. This is an estimate, not a quote.
- Google says it does not claim ownership of generated output under the Gemini API terms; the user remains responsible for legal use.
- TTS is a changing/preview technology. Confirm account access, regional availability, pricing, and current terms immediately before generating a full episode.

ElevenLabs practical notes:
- The current pricing page lists Free at 10,000 credits/month and Starter at 30,000 credits/month with a commercial license; listed Starter monthly price is subject to change and taxes.
- The TTS API supports voice IDs selected from the user's own account. The project includes a generator, but voice IDs are intentionally blank until the user chooses voices.
- A Persian voice is not automatically Afghan Dari. The six representative role samples must be reviewed; reject any voice unless its accent and pronunciation pass native Afghan Dari review.
