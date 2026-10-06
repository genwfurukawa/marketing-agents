---
description: Create a YouTube video - scaffold folder, write script, design thumbnail, optimize SEO, or generate full publish package from Descript transcript
argument-hint: [subcommand] [args...]
allowed-tools: Task, Read, Write, Grep, Glob, WebSearch, WebFetch
---

**Read `@clients/{client}/config.yaml` and `@clients/{client}/config/voice-guide.md` before generating content.**

## Task
Complete YouTube content creation system covering idea generation, scripting (long-form & shorts), thumbnail design, and SEO optimization.

**Subcommands:**
- `new [slug-or-title]` - Scaffold a new video folder with input/output structure
- `publish [video-slug]` - Generate complete publish package from Descript transcript exports
- `ideas [topic/niche]` - Generate video ideas based on trends and audience analysis
- `script [type] [topic]` - Write scripts (type: long-form, shorts, green-screen)
- `thumbnail [concept]` - Design thumbnail concepts with A/B variants
- `seo [video-title]` - Optimize title, description, tags, timestamps
- `full [topic]` - Complete end-to-end workflow for a video concept

**Arguments:**
- $1: Subcommand (ideas/script/thumbnail/seo/full)
- $2+: Context-specific arguments based on subcommand

## Architecture

This skill orchestrates 3 specialized agents plus 1 research skill:

1. **youtube-competitor-research skill** - Market research and ideation grounded in real YouTube Data API outlier data
2. **youtube-script-agent** - Script writing with hooks, pacing, retention optimization
3. **youtube-thumbnail-agent** - Thumbnail psychology, design concepts, A/B testing
4. **youtube-seo-agent** - Metadata optimization for discovery and CTR

## Subcommand Details

### `/youtube new [slug-or-title]`

Scaffold a new video folder with the correct structure and instructions.

**What it does:**
- Generates a URL-safe slug from the title (or uses the slug directly)
- Creates `{client_root}/production/youtube/videos/{slug}/input/` and `output/`
- Writes `DROP_FILES_HERE.md` with Descript export instructions
- Prints the exact files the user needs to paste

**Uses:** `scripts/youtube/scaffold_video.py`

**Example:**
```
/youtube new "How I replaced my marketing team with AI agents"
/youtube new ai-agents-marketing-2026
```

---

### `/youtube publish [video-slug]`

Generate the complete publish package from Descript transcript exports.

**Prerequisite:** Run `/youtube new` first, then paste `transcript.txt` and `transcript.srt` from Descript into the `input/` folder.

**What it does:**
- Validates input files exist (transcript.txt + transcript.srt)
- Parses SRT for chapter timestamp candidates
- Calls Claude to generate: title variants, full description with chapters, 20-30 tags, pinned comment, thumbnail concept
- Calls Nano Banana to generate `thumbnail.png` (16:9, 2K)
- Writes all outputs to `output/` folder
- Presents ready-to-use publish checklist

**Uses:** youtube-publish-agent

**Output:**
```
{video-slug}/
  output/
    metadata.json          - All structured metadata
    thumbnail_prompt.json  - Nano Banana image prompt
    thumbnail.png          - Generated YouTube thumbnail
    description.txt        - Paste into YouTube Studio
    pinned_comment.md      - First comment to post
    captions_en.srt        - Upload via Subtitles tab
```

**Example:**
```
/youtube publish ai-agents-marketing-2026
/youtube publish  # prompts for slug interactively
```

---

### `/youtube ideas [topic/niche]`

Generates 10-15 video ideas with predicted performance metrics.

**What it does:**
- Analyzes trending topics in your niche
- Reviews competitor content gaps
- Suggests hooks and angles for each idea
- Estimates search volume and competition
- Provides virality potential score

**Uses:** youtube-competitor-research skill (real YouTube Data API outlier data)

**Output:** Markdown file with ranked video ideas

**Example:**
```
/youtube ideas "AI marketing automation"
/youtube ideas
```

---

### `/youtube script [type] [topic]`

Writes complete video scripts optimized for retention.

**Types:**
- `long-form` - 8-15 minute educational/tutorial videos
- `shorts` - 30-60 second short-form content
- `green-screen` - Scripts designed for green screen B-roll overlays

**What it does:**
- Crafts hook (first 3-8 seconds)
- Structures content for maximum retention
- Adds pattern interrupts and engagement cues
- Includes CTA placement
- Suggests visual/editing notes
- Provides green screen background ideas (if type=green-screen)

**Uses:** youtube-script-agent

**Output:** Complete script with timestamps and production notes

**Example:**
```
/youtube script long-form "How to automate content marketing with AI"
/youtube script shorts "3 ChatGPT prompts for better blog posts"
/youtube script green-screen "Why most content strategies fail"
```

---

### `/youtube thumbnail [concept]`

Designs thumbnail concepts with A/B test variations.

**What it does:**
- Creates 3 thumbnail design concepts
- Applies proven CTR psychology principles
- Suggests color schemes and text overlays
- Provides A/B test variants
- Includes facial expression/emotion guidance
- Analyzes competitor thumbnails

**Uses:** youtube-thumbnail-agent

**Output:** Thumbnail design brief with mockup descriptions

**Example:**
```
/youtube thumbnail "AI agent breaks down marketing workflow"
/youtube thumbnail "surprised reaction to new Claude features"
```

---

### `/youtube seo [video-title]`

Optimizes all metadata for maximum discoverability.

**What it does:**
- Generates 5-7 title variations (A/B testing)
- Writes SEO-optimized description (with timestamps)
- Suggests 20-30 relevant tags
- Identifies keyword opportunities
- Creates chapter timestamps
- Suggests pinned comment and end screen

**Uses:** youtube-seo-agent

**Output:** Complete metadata package ready to paste

**Example:**
```
/youtube seo "Complete guide to AI content marketing"
```

---

### `/youtube full [topic]`

Complete end-to-end workflow combining all agents.

**What it does:**
1. Generate video concept & research (youtube-competitor-research skill)
2. Write complete script (script-agent)
3. Design thumbnail concepts (thumbnail-agent)
4. Optimize all metadata (seo-agent)

**Uses:** The research skill + all 3 agents in sequence

**Output:** Complete production package with all deliverables

**Example:**
```
/youtube full "How I use Claude Code to automate my marketing"
```

---

## Workflow Integration

### For Single Brand (Current Setup)

Store outputs in:
```
{client_root}/production/youtube/
  ├── videos/                          # Per-video publish packages
  │   └── [video-slug]/
  │       ├── input/                   # Drop Descript exports here
  │       │   ├── DROP_FILES_HERE.md
  │       │   ├── transcript.txt
  │       │   └── transcript.srt
  │       └── output/                  # Generated by /youtube publish
  │           ├── metadata.json
  │           ├── thumbnail.png
  │           ├── description.txt
  │           ├── pinned_comment.md
  │           └── captions_en.srt
  ├── ideas/
  │   └── [date]-video-ideas.md
  ├── scripts/
  │   ├── long-form/
  │   ├── shorts/
  │   └── green-screen/
  ├── thumbnails/
  │   └── [video-title]-concepts.md
  └── seo/
      └── [video-title]-metadata.md
```

### Context Sources

Agents will automatically pull context from:
- `{client_root}/research/founder-sessions/*/atoms.json` - Your unique insights (from `/founder-session`)
- `{client_root}/research/ao_search/aeo_questions.json` - Audience questions
- `{client_root}/research/competitors/competitive_atoms.json` - Competitor analysis
- Client brand voice guidelines (if available)

### Example Full Workflow

```bash
# Pre-production
/youtube ideas "AI automation for marketers"
/youtube script long-form "5 AI agents that run my entire marketing team"

# Record & edit in Descript...

# Post-production (NEW)
/youtube new "5 AI agents that run my entire marketing team"
# Drop transcript.txt + transcript.srt from Descript into input/ folder
/youtube publish 5-ai-agents-that-run-my-entire-marketing-team
# Review outputs, paste into YouTube Studio, upload thumbnail
```

**Pre-production only workflow:**
```bash
/youtube full "5 AI agents that run my entire marketing team"
```

## Output Format

All outputs are saved as markdown files with:
- Clear headings and sections
- Actionable next steps
- Production notes
- Performance predictions
- Iteration suggestions

## Success Metrics

Track these after implementation:
- CTR (Click-Through Rate) - Goal: >8% for first 48 hours
- AVD (Average View Duration) - Goal: >50%
- Engagement rate - Goal: >4%
- Search ranking for target keywords - Goal: Top 10 within 30 days

## Next Steps After Running

1. **Review & Refine** - AI outputs need human touch for authenticity
2. **Film/Record** - Use script as guide, allow for natural delivery
3. **Edit** - Follow retention cues and pacing notes
4. **A/B Test** - Test thumbnail variants (change after 24-48 hours if CTR <6%)
5. **Analyze** - Review YouTube Analytics, feed learnings back into system

## Tips for Best Results

- **Be Specific:** Instead of "/youtube ideas", use "/youtube ideas AI marketing automation"
- **Iterate:** Run script generation multiple times with different angles
- **Test Thumbnails:** Always create 2-3 variants and A/B test
- **Update Context:** Keep your atoms and research files current for better recommendations
- **Track Winners:** Document which video formats perform best, inform future ideation

## Error Handling

If agents can't find required context:
1. Check that founder-session atoms exist under `{client_root}/research/founder-sessions/`
2. Ensure `{client_root}/research/` has recent research
3. Provide more specific topic/niche in command arguments
4. Run research phase first if starting fresh

---

## Related Skills

- `youtube-packaging-first` skill - title + thumbnail first, full idea-to-publish pipeline
- `youtube-idea-validation` skill - go/no-go scoring before scripting
- `youtube-competitor-research` skill - outlier data before ideation
