# Gemini cinematic 3D image generation — Episode 001

This workflow generates original, premium 3D animated feature-film-style scene artwork
through the Gemini Developer API. The art direction explicitly rejects flat vector art,
simple SVG illustrations, clipart and 2D cartoon rendering.

## Run it

1. Open **Actions** in the EnglishTale GitHub repository.
2. Select **Generate Episode 001 images**.
3. Click **Run workflow**.
4. First choose **audition**. This generates four representative images and uploads them
   as the artifact `englishtale-episode-001-images-audition`.
5. Review the faces, dimensional 3D rendering, lighting, clothing and character continuity.
6. Only after approving the audition, run **generate-all** to generate all 12 scene images.

Generated files are stored in the workflow artifact under
`build/images/episode-001/`. They are not automatically committed to the public repository.

## Visual direction

- Premium original 3D animated feature-film frames, with dimensional models and sculpted detail.
- Expressive natural faces, detailed hair and fabric, soft global illumination and cinematic lighting.
- Rich airport environments with foreground, middle ground, background and atmospheric depth.
- No flat vector/SVG appearance, clipart, logos, watermarks or generated readable text.
- Wide 16:9 compositions with subtitle-safe space.

## Character continuity

Character identity is supplied as detailed text direction rather than the old flat SVG artwork,
because using flat vector references could pull the generated result toward a simple 2D look.

- Leo: 19-year-old young man, tousled brown hair, brown eyes, blue hoodie, dark jeans, white sneakers.
- Emma: 19-year-old young woman, shoulder-length brown hair, brown eyes, pink sweater, dark jeans, white sneakers.
- Ollie: small brown owl, cream face/chest, large eyes, round glasses, navy scarf with gold accent.
- Gate 12 must be added as editable text in post-production.

## Security and cost

- The API key is read only from the GitHub Actions secret `GEMINI_API_KEY`; never put it
  in source files, prompts, logs, or chat messages.
- The workflow checks the secret at runtime without printing it.
- Image generation consumes Google API quota and may incur charges depending on model
  availability and account billing. Check Google AI Studio usage and pricing before a full batch.
- The four-image audition is intended to catch visual-direction problems before generating all 12.
- Generated images are review assets, not a finished animated video. Human review remains required.
