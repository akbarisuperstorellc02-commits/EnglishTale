# Gemini image generation — Episode 001

This workflow generates original scene illustrations through the Gemini Developer API.
It uses the current `gemini-3.1-flash-image` image model, the official `GEMINI_API_KEY`
GitHub Actions secret, and the existing Leo/Emma/Ollie SVG character artwork as visual
references. The reference SVGs are rasterized locally before being sent to the API.

## Run it

1. Open **Actions** in the EnglishTale GitHub repository.
2. Select **Generate Episode 001 images**.
3. Click **Run workflow**.
4. First choose **audition**. This generates four representative images and uploads them
   as the artifact `englishtale-episode-001-images-audition`.
5. Review the images for character consistency, composition, and visual quality.
6. Only after approving the audition, run **generate-all** to generate all 12 scene images.

Generated files are stored in the workflow artifact under
`build/images/episode-001/`. They are not automatically committed to the public repository.

## Security and cost

- The API key is read only from the GitHub Actions secret `GEMINI_API_KEY`; never put it
  in source files, prompts, logs, or chat messages.
- GitHub Actions cannot reveal whether a secret exists or whether its value is valid.
  The workflow checks it at runtime without printing it.
- Image generation consumes the Google API quota and may incur charges depending on the
  account, model availability, and billing status. Check Google AI Studio usage and pricing
  before running the full batch.
- The workflow skips already generated non-empty image files if rerun in the same workspace;
  a new GitHub Actions run starts with a clean workspace.
- Generated images are review assets, not a finished animated video. Human review remains
  required before publication.

## Character and composition rules

- Leo: blue hoodie.
- Emma: pink sweater.
- Ollie: small owl.
- Keep Gate 12 consistent, but add readable text in editing rather than asking the image
  model to render it.
- The workflow begins with a four-image audition to reduce unnecessary API use.
