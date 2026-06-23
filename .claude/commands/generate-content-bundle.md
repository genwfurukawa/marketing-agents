---
description: Turn one input (transcript, voice memo, or notes) into drafts across LinkedIn, blog, email, video script, and carousel
argument-hint: [input-file-or-text] [--client client-slug] [--formats linkedin,blog,email,video,carousel]
allowed-tools: Task, Read, Write, Glob, Grep
---

## Task

Take a single founder input - transcript, voice memo, rough notes, or pasted text - and produce ready-to-use content across multiple formats in one run. This is the "create once, publish everywhere" command.

**Arguments:**
- `$1`: Path to input file (transcript, notes, voice memo transcript) OR raw text pasted inline
- `--client`: Client slug (optional - loads brand brain and voice context)
- `--formats`: Comma-separated list of formats to generate (default: all)
  - Options: `linkedin`, `blog`, `email`, `video`, `carousel`
  - Example: `--formats linkedin,blog,email`

## How It Works

This command chains three stages:

1. **Extract** - Pull atomic insights from the raw input
2. **Brief** - Create format-specific content briefs for each requested format
3. **Generate** - Produce draft content for each format

One input. Multiple outputs. Under 5 minutes.

## Steps

### Stage 1: Load Context

1. **Resolve client context** (if --client provided):
   - Resolve `{client_root}` from `clients_registry.json`, or default to `../clients/{client_slug}/`
   - Read Brand Brain at `{client_root}/03_insight_layer/brand_brain.md`
   - Read voice framework at `{client_root}/03_insight_layer/pillars/voice_framework_*.json`
   - Read positioning framework at `{client_root}/03_insight_layer/pillars/positioning_framework_*.json`
   - Read output style at `.claude/output-styles/consultant-operator.md`

2. **Load default context** (if no --client):
   - Read founder voice guide at `clients/{client}/config/voice-guide.md`
   - Read brand kit at `clients/{client}/brand/brand-kit.md`
   - Read output style at `.claude/output-styles/consultant-operator.md`

3. **Read the input**:
   - If `$1` is a file path, read the file
   - If `$1` is inline text, use it directly
   - If no input provided, ask the user to paste their transcript or notes

4. **Parse requested formats**:
   - Default: all 5 formats (linkedin, blog, email, video, carousel)
   - If `--formats` specified, only generate those formats

### Stage 2: Extract Atoms

Use the **insight-capture-agent** (lightweight mode) to extract atoms from the raw input:

1. Identify discrete insights, quotes, stories, pain points, outcomes, and beliefs
2. Score each atom for confidence (0.5+ required)
3. Tag each atom with suggested content pillar alignment
4. Minimum 3 atoms required to proceed (if fewer found, warn and continue with what exists)

**Note:** This is a lightweight extraction - skip foundation prerequisite checks. The goal is speed for demo and iteration, not pipeline compliance.

Present atoms to the user:

```
## Extracted Atoms ({count})

| # | Type | Content (preview) | Confidence |
|---|------|-------------------|------------|
| 1 | insight | {first 80 chars}... | 0.85 |
| 2 | quote | {first 80 chars}... | 0.92 |
...

Proceeding to generate {n} formats: {format_list}
```

### Stage 3: Generate Content (Per Format)

Run each format generation in sequence. For each format, use the appropriate agent.

#### LinkedIn Post (if requested)
Use **linkedin-post-agent**:
- Auto-select best post type based on atom types (story atoms -> story post, insight atoms -> insight post)
- Generate primary post + 3 hook variants + 3 CTA variants
- Max 1,300 characters
- Scan for banned phrases

#### Blog Outline (if requested)
Generate an AEO-structured blog outline:
- Headline with contrarian angle drawn from atoms
- Meta description (max 160 chars)
- 4-6 section outline with H2/H3 structure
- Map atoms to sections
- Include: TL;DR, FAQ section (3-5 questions), definition callout
- Target: 1,200-2,000 words when drafted
- Note: This produces the outline + key section drafts, not a full 2,000-word post

#### Email/Newsletter (if requested)
Generate a newsletter edition:
- 3 subject line options (curiosity gap, direct value, specific insight)
- Preview text (max 90 chars)
- Body: 250-400 words, one core idea from strongest atom
- Single clear CTA
- Founder voice throughout

#### Video Script Hook (if requested)
Generate a short-form video script:
- Hook (0-3 seconds): Problem or bold claim from strongest atom
- Context (3-15 seconds): Why this matters
- Content (15-60 seconds): Key insight, framework, or proof
- CTA (final 5-10 seconds): Single clear action
- Include delivery notes and visual suggestions

#### Carousel Framework (if requested)
Generate carousel structure:
- Cover slide: Hook from strongest contrarian atom
- 5-8 content slides with primary text (80 chars max) and supporting text (120 chars max)
- Final CTA slide
- Design direction notes (colors, layout suggestions per brand kit)

### Stage 4: Compile and Save

1. **Compile all outputs** into a single markdown file with clear sections per format
2. **Save output**:
   - If --client: `{client_root}/04_content_engine/repurposed/{YYYY-MM-DD}_{topic_slug}_bundle.md`
   - If no client: Print all outputs to the conversation
3. **Present summary** to user

## Output Format

```markdown
# Content Bundle: {topic}
Generated: {date} | Source: {input_filename_or_"inline_text"} | Formats: {count}

---

## Source Atoms ({count} extracted)

| # | Type | Content | Pillar |
|---|------|---------|--------|
| 1 | {type} | {content} | {pillar} |

---

## LinkedIn Post

**Post Type:** {auto-selected type}

{full post text - ready to copy-paste}

### Hook Variants
1. {hook_variant_1}
2. {hook_variant_2}
3. {hook_variant_3}

### CTA Variants
1. {cta_variant_1}
2. {cta_variant_2}
3. {cta_variant_3}

---

## Blog Outline

**Headline:** {headline}
**Meta Description:** {meta_description}

### TL;DR
{2-3 sentence summary}

### Outline
1. **{H2 Section}** - {brief description + atom reference}
2. **{H2 Section}** - {brief description + atom reference}
3. **{H2 Section}** - {brief description + atom reference}
4. **{H2 Section}** - {brief description + atom reference}

### FAQ Section
1. **{question}** - {direct answer}
2. **{question}** - {direct answer}
3. **{question}** - {direct answer}

---

## Email / Newsletter

**Subject Lines:**
1. {curiosity_gap_version}
2. {direct_value_version}
3. {specific_insight_version}

**Preview Text:** {preview_text}

{full email body - 250-400 words}

---

## Video Script

**Format:** Short-form ({duration})

HOOK (0-3s): {hook}
[Delivery note: {note}]

CONTEXT (3-15s): {context}

CONTENT (15-60s): {content}
[Visual: {suggestion}]

CTA: {cta}

---

## Carousel

**Slides:** {count}
**Type:** {carousel_type}

| Slide | Primary Text | Supporting Text | Visual Direction |
|-------|-------------|-----------------|------------------|
| Cover | {hook} | {subtext} | {direction} |
| 2 | {text} | {supporting} | {direction} |
| ... | ... | ... | ... |
| CTA | {cta_text} | {supporting} | {direction} |
```

## Quality Checks (Applied to All Formats)

Before presenting output, verify each format passes:
- [ ] No banned phrases from output style
- [ ] Character limits respected (LinkedIn 1,300, email subject 50, etc.)
- [ ] Voice-aligned (matches founder voice guide or Brand Brain)
- [ ] Every format has a clear CTA
- [ ] No hedging language, no corporate jargon
- [ ] Specific numbers or timeframes included where possible

## Example Usage

```
# Full repurpose from a transcript file
/repurpose clients/acme/01_founder_capture/raw/podcast_episode_12.txt --client acme

# Just LinkedIn and email from pasted notes
/repurpose "AI search is replacing Google for B2B buyers. 73% of decision-makers now use ChatGPT before vendor calls..." --formats linkedin,email

# All formats for a specific client
/repurpose clients/{client}/config/voice-guide.md --client {client_slug}

# Quick demo with inline text (no client context)
/repurpose "Most SaaS founders post on LinkedIn 3x a week and get zero pipeline from it. The problem isn't frequency. The problem is they're optimizing for likes instead of citations."
```

## Demo Script

When showing this on a sales call:

1. Open Claude Code
2. Paste 2-3 paragraphs of the prospect's own content (from their LinkedIn, blog, or website)
3. Run: `/repurpose "{pasted text}" --formats linkedin,blog,email`
4. Watch 3 formats generate in under 2 minutes
5. Show how each format maintains their voice but optimizes for the channel

The prospect sees their own ideas turned into a multi-channel content system. That's the sale.
