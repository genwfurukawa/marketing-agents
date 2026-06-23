---
description: Create an image prompt and optionally generate the image via Nano Banana (Gemini)
argument-hint: [description] [--generate] [--client client-slug] [--preset single_image|story|banner|carousel_slide|thumbnail] [--batch count] [--output-dir path]
allowed-tools: Task, Read, Write, Glob, Grep, Bash
---

## Task

Create structured image prompt JSON files for Nano Banana (Gemini) image generation. Every image gets its own JSON file with structured prompt data. With `--generate`, also runs image generation automatically.

**Arguments:**
- `$1`: Description of the image(s) to create - what they should show, their purpose, or the content they accompany
- `--generate`: Auto-generate images after writing JSON files (requires GOOGLE_GENAI_API_KEY in .env)
- `--client`: Client slug (optional - loads brand brain for visual context)
- `--preset`: Preset that sets aspect ratio and base style automatically (optional - defaults to single_image)
  - `single_image` - 1:1 square post image
  - `story` - 9:16 vertical story
  - `banner` - 4:1 wide banner
  - `carousel_slide` - 4:5 carousel slides
  - `thumbnail` - 16:9 YouTube thumbnail (2K resolution, no brand watermark)
- `--batch`: Number of images to create (for carousel sets or campaign batches)
- `--output-dir`: Where to save JSON files (default: client content dir or current dir)

## Schema Reference

Every JSON file MUST follow this structure:

```json
{
  "prompt": "Core visual description - what the image shows",
  "output_filename": "snake_case_name.png",
  "model": "flash-preview",
  "preset": "single_image",
  "resolution": "2K",
  "style": "Visual style direction",
  "brand": "{client_slug}",
  "layout": {
    "headline": "Text to render as headline",
    "subheadline": "Secondary text",
    "stat": "Key number to display",
    "body_text": "Supporting copy",
    "cta": "Call to action text",
    "logo_position": "bottom-right"
  },
  "negative_prompt": "What to avoid",
  "metadata": {
    "client": "client-slug",
    "campaign": "campaign-name",
    "content_id": "linked-brief-id",
    "created_at": "2026-03-01",
    "notes": "Internal notes"
  }
}
```

## Steps

1. **Load Context** (if --client provided):
   - Resolve `{client_root}` from `clients_registry.json`
   - Read Brand Brain at `{client_root}/03_insight_layer/brand_brain.md` for visual identity
   - Read brand kit at `clients/{client}/brand/brand-kit.md`
   - Note the client's colors, font, logo, and design principles

2. **Analyze the Request**:
   - Determine how many images are needed
   - Identify the purpose: LinkedIn post, carousel, banner, campaign asset
   - Determine if these are text-heavy (use layout) or visual-only (skip layout)
   - Select the right preset and aspect ratio

3. **Write Image Prompt Rules** (apply to every prompt you write):
   - **Be specific about composition**: describe foreground, background, text placement
   - **Specify text exactly**: any text on the image must be in quotes in the prompt AND in the layout fields
   - **Include style direction**: flat vector, photo-realistic, typographic, abstract, etc.
   - **Describe color palette**: reference brand colors by hex or name
   - **Avoid ambiguity**: "professional graphic" is vague. "Bold typographic poster on black background with neon lime accent bar" is specific
   - **Negative prompts**: always include what to avoid (stock photo feel, clip art, emojis, gradients unless requested)

4. **Generate JSON Files**:
   - Create one JSON file per image
   - Filename convention: `{purpose}_{descriptor}.json` (e.g., `post_ai_search_visibility.json`)
   - For carousel batches: `carousel_{topic}_{slide_number}.json`
   - For campaign sets: `{campaign}_{variant}.json`
   - Save to the specified output directory

5. **Generate or Provide Command**:

   **If `--generate` flag is present:**
   - Load the API key from .env and run generation immediately:
   ```bash
   export $(grep -v '^#' .env | grep 'GOOGLE_GENAI_API_KEY' | xargs) && python3 scripts/image/generate_from_json.py -i path/to/prompt.json -o output/dir/
   ```
   - For batch: point `-i` at the directory containing all JSON files
   - After generation, display each image to the user for review
   - If generation fails (missing API key, rate limit), show the error and fall back to providing the manual command

   **If `--generate` flag is NOT present:**
   - Show the exact command to run later:
   ```
   # Single image
   python3 scripts/image/generate_from_json.py -i path/to/prompt.json -o output/images/

   # Batch (all JSON files in directory)
   python3 scripts/image/generate_from_json.py -i path/to/prompts/ -o output/images/

   # Dry run (preview prompts without generating)
   python3 scripts/image/generate_from_json.py -i path/to/prompts/ -o output/images/ --dry-run
   ```

## Prompt Writing Guidelines

### For Text-Heavy Images (LinkedIn posts, carousels)
- Always use the `layout` object to specify exact text
- Keep headlines under 8 words
- Stats should be a single number + unit
- Describe the typographic hierarchy: what's big, what's small, what's emphasized
- Specify text color for each element

### For Visual Images (hero shots, abstract, illustrations)
- Describe the scene in detail: subject, environment, lighting, mood
- Reference specific art styles or visual references
- Include color palette direction
- Describe depth: foreground, midground, background

### For Campaign Sets
- Establish visual consistency rules in the first image
- Reference the visual identity in subsequent images
- Use the same style, color palette, and layout grid across the set

## Output

For each image, a JSON file containing:
- Complete prompt optimized for Gemini image generation
- All technical settings (model, ratio, resolution)
- Layout instructions for text rendering
- Metadata for tracking
- Plus the CLI command to run generation

## Thumbnail Preset

When `--preset thumbnail` is used, apply these defaults:
- `aspect_ratio`: `16:9`
- `resolution`: `2K`
- `brand`: `none` (thumbnails use channel brand, not client watermark)
- `layout.logo_position`: `none`
- Style: Bold, high-contrast, readable at small sizes, YouTube thumbnail aesthetic
- Negative prompt always includes: no small text, no busy backgrounds, readable at mobile sizes

For thumbnails, derive the visual concept from the title/topic:
- Extract the core tension or benefit
- Pick a psychology trigger: contrast, curiosity, value_signal, fear, or authority
- Design for the 3-second scroll test - would you click this?

## Example Usage

```
# JSON only (review before generating)
/image-prompt "LinkedIn post image for 'AI search is the new SEO' article"
/image-prompt "5-slide carousel about the visibility system" --preset carousel_slide --batch 5

# JSON + auto-generate in one step
/image-prompt "YouTube thumbnail for 'Build a Brand Brain'" --preset thumbnail --generate
/image-prompt "campaign hero images for AEO launch" --client {client_slug} --batch 3 --generate
/image-prompt "banner for YouTube video about founder-led content" --preset banner --generate
```