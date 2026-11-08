# EnglishTale — AI-Assisted English Learning Animation Studio

**Tagline:** Learn English Through Stories  
**Episode 01:** English at the Airport  
**Audience:** English learners worldwide; this first series uses English dialogue with Afghan Dari explanations.  
**Level:** CEFR A1–A2  
**Target runtime:** 6–8 minutes  
**Format:** 16:9, 1920×1080, 30 fps, MP4

## Current production status

Episode 001 has moved beyond the planning-only stage. The repository now includes original coded vector artwork, animated SVG character rigs, an 18-shot edit plan, and aligned English/Dari subtitle guide tracks.

### Completed and committed
- Full episode script and bilingual teaching content.
- Character bible: Leo (blue hoodie), Emma (pink sweater), and Ollie (owl guide).
- Five original 1280×720 airport/airplane SVG scene plates.
- Original 16:9 Episode 001 thumbnail artwork in SVG, exported as a 3840×2160 4K PNG for YouTube.
- Original 9:16 Episode 001 Shorts cover in SVG, exported as a 2160×3840 PNG.
- Three original 640×640 SVG character rigs with embedded CSS animation.
- 18-shot animation/edit plan for the 7-minute episode.
- English SRT and Afghan Dari SRT, each with 48 matching cue boundaries.
- Voice and subtitle production instructions.
- 48-cue bilingual voice manifest and recording package.
- Separate English/Dari WAV track assembler with timeline-gap preservation.
- Resumable Gemini and ElevenLabs TTS generator tools; provider access and commercial rights are documented.
- Dependency-free validator and unit tests for all 96 bilingual WAV recordings, with a strict release gate.
- MP4 export option for selectable English and Afghan Dari audio tracks.
- YouTube metadata and thumbnail brief.
- Four YouTube Shorts cutdown plans for repurposing Episode 001.

### Not yet produced
- Final voice recordings / TTS audio.
- Waveform-verified subtitle timing and phoneme-accurate lip sync.
- Fully animated, rendered MP4 master.
- Final approved thumbnail after manual review and final audio mix.
- YouTube upload or publication.

**Important:** The subtitle timecodes are editorial guides across the planned 07:00 runtime. They must be retimed after the real voice track is generated. The SVG character mouth movement is a placeholder, not accurate lip sync. Do not describe this repository as containing a finished episode video.

## Repository map

```text
EnglishTale/
├── .github/
│   └── workflows/
│       └── validate-episode.yml
├── README.md
├── production-workflow.md
├── brand/
│   ├── brand-guide.md
│   └── channel-about.md
├── characters/
│   ├── character-bible.md
│   └── prompts.md
├── assets/
│   ├── characters/
│   ├── scenes/
│   ├── animation/
│   └── thumbnails/
├── episodes/
│   └── 001-english-at-the-airport/
│       ├── episode-brief.md
│       ├── script-en-fa.md
│       ├── storyboard.md
│       ├── animation-shot-plan.md
│       ├── render-shotlist.json
│       ├── voice-and-sound.md
│       ├── voice-subtitle-production.md
│       ├── voice-recording-package.md
│       ├── voice-manifest.json
│       ├── subtitles-en.srt
│       ├── subtitles-fa.srt
│       ├── youtube-metadata.md
│       ├── thumbnail-prompt.md
│       ├── shorts-plan.md
│       ├── tts-provider-research.md
│       └── production-status.md
├── tools/
│   ├── video-pipeline/
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   ├── render_episode.py
│   │   ├── build_audio_tracks.py
│   │   ├── render_thumbnail.py
│   │   ├── render_shorts_cover.py
│   │   ├── validate_shorts_cover.py
│   │   ├── validate_thumbnail.py
│   │   └── validate_episode.py
│   └── tts/
│       ├── README.md
│       ├── elevenlabs-README.md
│       ├── requirements.txt
│       ├── generate_gemini_tts.py
│       ├── generate_elevenlabs_tts.py
│       ├── voices.json
│       └── elevenlabs-voices.json
├── prompts/
│   ├── image-generation.md
│   └── image-to-video.md
└── publishing/
    ├── quality-control.md
    └── asset-license-log.csv
```

## Quick start

1. Run the input validator: `python tools/video-pipeline/validate_episode.py`.
2. Check generated recordings with `python tools/tts/validate_voice_assets.py`; use `--strict` to require all 96 valid WAV files. See `tools/tts/VOICE_ASSET_VALIDATION.md`.
3. After recording all cues, assemble the separate language tracks with `python tools/video-pipeline/build_audio_tracks.py`.
4. Build a silent visual review cut: `python tools/video-pipeline/render_episode.py` (requires FFmpeg and CairoSVG; see `tools/video-pipeline/README.md`). To include both selectable language tracks, pass `--english-audio` and `--dari-audio`.
5. Export the long-form 4K thumbnail with `python tools/video-pipeline/render_thumbnail.py` and the vertical Shorts cover with `python tools/video-pipeline/render_shorts_cover.py`.
5. Review `tools/tts/README.md` and `tools/tts/elevenlabs-README.md` before generating narration. Do not generate all clips until the English and Afghan Dari sample voices have been auditioned.
6. Read `brand/brand-guide.md` and `characters/character-bible.md`.
7. Review the SVG scene plates in `assets/scenes/` and character rigs in `assets/animation/`.
8. Follow `episodes/001-english-at-the-airport/animation-shot-plan.md` for the edit structure.
9. Generate each speaker line separately using `voice-and-sound.md`; keep English and Dari audio separate.
10. Retiming both SRT tracks against the final audio is mandatory.
11. Assemble and review the video using `production-workflow.md`.
12. Check every item in `publishing/quality-control.md` and verify commercial-use permissions before upload.

## Important production principles

- Keep character designs consistent: Leo's hoodie is blue, Emma's sweater is pink, and Ollie is an owl.
- Keep the airport gate number consistent: Gate 12.
- English is the main learning audio. Dari explanations must not talk over English dialogue.
- Use only music, voices, fonts, images, and video assets that permit the intended commercial use. Keep proof of licenses.
- Do not assume a free plan includes commercial rights. Check each provider's current terms before publishing.
- AI use alone does not guarantee or prevent YouTube monetization. Make each episode original, useful, and meaningfully edited.
- The Dari subtitles are a separate track and can be reviewed by a native Afghan Dari speaker before release.

## Release strategy

Publish one polished long-form episode first. Then create 2–3 useful Shorts from the episode, each with a complete mini-lesson and a pointer to the full story.
