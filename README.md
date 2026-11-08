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
- Original 1280×720 Episode 001 thumbnail artwork in SVG, with a PNG export script.
- Three original 640×640 SVG character rigs with embedded CSS animation.
- 18-shot animation/edit plan for the 7-minute episode.
- English SRT and Afghan Dari SRT, each with 48 matching cue boundaries.
- Voice and subtitle production instructions.
- 48-cue bilingual voice manifest and recording package.
- Separate English/Dari WAV track assembler.
- YouTube metadata and thumbnail brief.

### Not yet produced
- Final voice recordings / TTS audio.
- Waveform-verified subtitle timing and phoneme-accurate lip sync.
- Fully animated, rendered MP4 master.
- Final thumbnail image and final audio mix.
- YouTube upload or publication.

**Important:** The subtitle timecodes are editorial guides across the planned 07:00 runtime. They must be retimed after the real voice track is generated. The SVG character mouth movement is a placeholder, not accurate lip sync. Do not describe this repository as containing a finished episode video.

## Repository map

```text
EnglishTale/
├── README.md
├── production-workflow.md
├── brand/
│   ├── brand-guide.md
│   └── channel-about.md
├── characters/
│   ├── character-bible.md
│   └── prompts.md
├── assets/
│   ├── characters/          # Original static character SVGs
│   ├── scenes/              # Five original scene plates
│   └── thumbnails/          # Original Episode 001 thumbnail artwork
│   └── animation/           # Animated SVG rigs + pipeline notes
├── episodes/
│   └── 001-english-at-the-airport/
│       ├── episode-brief.md
│       ├── script-en-fa.md
│       ├── storyboard.md
│       ├── animation-shot-plan.md
│       ├── voice-and-sound.md
│       ├── voice-subtitle-production.md
│       ├── voice-recording-package.md
│       ├── voice-manifest.json
│       ├── subtitles-en.srt
│       ├── subtitles-fa.srt
│       ├── youtube-metadata.md
│       └── thumbnail-prompt.md
├── prompts/
│   ├── image-generation.md
│   └── image-to-video.md
└── publishing/
    ├── quality-control.md
    └── asset-license-log.csv
```

## Quick start

1. Run the input validator: `python tools/video-pipeline/validate_episode.py`.
2. After recording all cues, assemble the separate language tracks with `python tools/video-pipeline/build_audio_tracks.py`.
3. Build a silent visual review cut: `python tools/video-pipeline/render_episode.py` (requires FFmpeg and CairoSVG; see `tools/video-pipeline/README.md`).
4. Export the thumbnail PNG with `python tools/video-pipeline/render_thumbnail.py`.
5. Read `brand/brand-guide.md` and `characters/character-bible.md`.
6. Review the SVG scene plates in `assets/scenes/` and character rigs in `assets/animation/`.
7. Follow `episodes/001-english-at-the-airport/animation-shot-plan.md` for the edit structure.
8. Generate each speaker line separately using `voice-and-sound.md`; keep English and Dari audio separate.
9. Retiming both SRT tracks against the final audio is mandatory.
10. Assemble and review the video using `production-workflow.md`.
11. Check every item in `publishing/quality-control.md` and verify commercial-use permissions before upload.

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
