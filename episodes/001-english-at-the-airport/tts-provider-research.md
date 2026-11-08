# TTS provider research — 2026-11-08

Recommended first audition: Google's Gemini 3.8 Flash TTS, because its official language list explicitly includes both English and Persian (Afghanistan). It is a candidate to audition, not a guarantee of natural Kabul Dari.

Official references:
- Supported TTS languages and API usage: https://ai.google.dev/gemini-api/docs/speech-generation
- Gemini API pricing (including free-tier data use and TTS rates): https://ai.google.dev/gemini-api/docs/pricing
- Gemini API additional terms: https://ai.google.dev/gemini-api/terms
- Google Cloud generative AI service terms: https://cloud.google.com/terms/service-terms

Research notes:
- Gemini 3.8 Flash TTS lists English and Persian (Afghanistan) among supported languages.
- The official pricing page currently shows a free tier, with content used to improve products; the paid tier is listed as not used for product improvement.
- Current published paid output pricing for Gemini 3.8 Flash TTS is $9 per 1M audio tokens through 2026-12-31 and $18 per 1M audio tokens from 2027-01-01. Audio tokenization is estimated by Google at 25 tokens per second. A 14-minute pair of 7-minute tracks would be roughly 21,000 audio tokens, or about $0.19 at the current rate, excluding input tokens and retries. This is an estimate, not a quote.
- Google says it does not claim ownership of generated output under the Gemini API terms; the user remains responsible for legal use.
- TTS is a changing/preview technology. Confirm account access, regional availability, pricing, and current terms immediately before generating a full episode.

Alternative considered:
- ElevenLabs offers Persian TTS, but its Persian page does not establish a distinct Afghan Dari/Kabul voice. Its help documentation states free-plan output is not licensed for commercial use; paid plans include a commercial license subject to terms. For a low-budget first episode, Gemini is the stronger initial audition candidate, subject to native-speaker review.
