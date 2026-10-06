---
description: Turn a podcast transcript into title options, summary, takeaways, thumbnail concepts, and short-form clip timestamps
argument-hint: [transcript-file] [--client client-slug]
allowed-tools: Task, Read, Write, Glob, Grep
---

## Task

Take a timestamped podcast transcript and produce a complete publish package: title options, summary, takeaways, guest links, CTAs, and short-form clip candidates. Designed to run repeatedly - one transcript in, full package out.

**Arguments:**
- `$1`: Path to transcript file (timestamped text format)
- `--client`: Client slug (optional - loads brand brain and voice context)

If no file provided, ask the user to paste their timestamped transcript.

## Steps

### Step 1: Load Context

1. **Resolve client context** (if --client provided):
   - Resolve the client via the active client convention: explicit client slug argument, else `CLIENT_CONFIG` env var pointing at the client's `config.yaml`. `{client_root}` = `clients/{client_slug}/` (or the repo root in a standalone client repo)
   - Read Brand Brain at `{client_root}/config/brand-brain.md`
   - Read output style at `.claude/output-styles/consultant-operator.md`

2. **Load default context** (if no --client):
   - Read founder voice guide at `clients/{client}/config/voice-guide.md`
   - Read output style at `.claude/output-styles/consultant-operator.md`

3. **Read the transcript**:
   - If `$1` is a file path, read the file
   - If no input provided, ask the user to paste their timestamped transcript

### Step 2: Extract Guest Information

Scan the transcript for:
- **Guest name** - Full name as introduced or referenced
- **Guest title/position** - Role, job title
- **Guest company** - Company name and what they do
- **Guest LinkedIn** - If mentioned or inferable from context
- **Guest websites** - Any URLs, products, or resources mentioned by or about the guest
- **Other resources mentioned** - Tools, books, frameworks, links referenced in conversation

If any guest info is ambiguous or missing, ask the user before proceeding.

### Step 3: Generate Titles

Create **3 title options** optimized for YouTube and Spotify discovery.

**Title rules:**
- How-to or explanation-based framing (teaches something specific)
- Create curiosity gap - make the listener need to know
- End with: `| {Guest Name}, {Position} at {Company}`
- Max 100 characters before the guest attribution
- No clickbait - the episode must deliver on the title's promise
- Front-load the value proposition (first 50 chars matter most for mobile)

**Title formula options to choose from:**
1. "How [Guest] [achieved specific outcome]" pattern
2. "Why [contrarian claim about topic]" pattern
3. "[Number] [Things] That [Outcome]" pattern
4. "The [Framework/System] Behind [Result]" pattern
5. "[Specific outcome] in [Timeframe]: [Method]" pattern

### Step 4: Write Episode Summary

Write a summary of the discussion in 150-250 words.

**Summary rules:**
- Open with the single most interesting claim or insight from the episode
- Cover the arc of the conversation - what ground was covered
- Name specific frameworks, strategies, or stories discussed
- Write for someone deciding whether to listen - sell the episode
- No fluff, no "in this episode we discuss..." preamble
- Use present tense ("Guest explains..." not "Guest explained...")

### Step 5: Extract Takeaways

Identify **3-5 specific takeaways** someone will learn from the full episode.

**Takeaway rules:**
- Each takeaway is a complete, actionable insight (not a vague topic)
- Start each with a bold claim or specific number
- Include enough context that the takeaway is useful standalone
- Order from most surprising/valuable to least
- Format: numbered list, 1-2 sentences each

**Wrong:** "We talk about content marketing"
**Right:** "Most SaaS companies waste 80% of their content budget on bottom-funnel blog posts - Gen explains why top-of-funnel thought leadership drives 3x more pipeline"

### Step 6: Build Links and CTAs

**Learn More section:**
- List all guest websites, tools, and resources mentioned in the conversation
- Include company website
- Include any specific pages, tools, or downloads referenced
- Format as clickable bullet list with brief context for each

**CTAs (two required):**

1. **Brand CTA:**
   - Link to brand website (from clients/{client}/config.yaml brand.website or client brand brain)
   - Brief value statement tied to the episode topic
   - Example: "Build your own visibility system at {brand_website}"

2. **Guest LinkedIn CTA:**
   - Direct link format: linkedin.com/in/{handle}
   - Encourage connecting with the guest
   - Example: "Connect with {Guest Name} on LinkedIn: {URL}"

### Step 7: Thumbnail Text and Visual Concepts

For each of the 3 title options, generate thumbnail assets.

**Thumbnail text (3 options per title):**
- 3-5 words max - this is overlay text on the thumbnail image
- Must complement the title, not repeat it
- Create urgency, curiosity, or a strong emotional reaction
- ALL CAPS works best for thumbnails
- Avoid generic phrases ("MUST WATCH", "GAME CHANGER")
- Best patterns: a bold claim, a number, a question, or a contradiction

**Examples:**
- Title about AI replacing marketers -> "THEY'RE ALREADY GONE" / "0 MARKETERS LEFT" / "AI DID IT FASTER"
- Title about content strategy -> "STOP POSTING" / "3X MORE PIPELINE" / "CONTENT IS DEAD"

**Thumbnail visual concept (1 per title):**
- Describe a background scene or composition for Gemini image generation (Nano Banana)
- Include: mood, color palette, key visual elements, composition direction
- Style: podcast/YouTube thumbnail aesthetic - bold, high contrast, clean
- Always include space for text overlay and a headshot/face
- Format as a ready-to-use Gemini prompt

**Example prompt:** "Professional podcast studio background, dark moody lighting with neon lime accent light from the left, shallow depth of field, clean negative space on the right side for text overlay, 16:9 aspect ratio, YouTube thumbnail style"

### Step 8: Identify Short-Form Clip Candidates

Scan the full transcript for segments that work as standalone short-form video clips (YouTube Shorts, TikTok, Instagram Reels, LinkedIn video).

**Identify 5-8 clip candidates.** For each clip:

- **Timestamp range**: Start and end time from the transcript (e.g., `12:34 - 14:02`)
- **Clip title**: A hook-style title for the short (max 60 chars)
- **Why it works**: One sentence explaining why this segment stands alone
- **Type**: Tag as one of: `hot-take`, `story`, `framework`, `stat`, `aha-moment`, `controversy`, `how-to`
- **Estimated duration**: In seconds (target 30-90 seconds)
- **Opening line**: The exact first sentence of the clip (for the hook)

**What makes a good clip:**
- Self-contained insight - no prior context needed
- Strong opening line (bold claim, surprising stat, contrarian take)
- Emotional energy - passion, surprise, disagreement, humor
- Clear point - lands within 30-90 seconds
- Would make someone stop scrolling

**What to avoid:**
- Segments that require earlier context to understand
- Long setup with delayed payoff
- Inside references the audience won't get
- Low-energy, conversational filler

### Step 9: Compile and Save

1. **Compile all outputs** into a single markdown file
2. **Save output**:
   - If --client: `{client_root}/production/podcast/{YYYY-MM-DD}_{episode_slug}_package.md`
   - If no client: Print all outputs to the conversation
3. **Present summary** to user with episode slug and file location

## Output Format

```markdown
# Podcast Episode Package: {Episode Topic}
Generated: {date} | Guest: {Guest Name}, {Position} at {Company}

---

## Title Options (YouTube + Spotify)

1. {Title option 1} | {Guest Name}, {Position} at {Company}
2. {Title option 2} | {Guest Name}, {Position} at {Company}
3. {Title option 3} | {Guest Name}, {Position} at {Company}

---

## Episode Summary

{150-250 word summary}

---

## Key Takeaways

1. **{Takeaway 1 headline}** - {1-2 sentence explanation}
2. **{Takeaway 2 headline}** - {1-2 sentence explanation}
3. **{Takeaway 3 headline}** - {1-2 sentence explanation}
4. **{Takeaway 4 headline}** - {1-2 sentence explanation}
5. **{Takeaway 5 headline}** - {1-2 sentence explanation}

---

## Learn More

- [{Resource name}]({URL}) - {brief context}
- [{Resource name}]({URL}) - {brief context}
- [{Guest company}]({URL}) - {what they do}

---

## CTAs

**{Brand Name}:** {Value statement} -> {brand_website}

**Connect with {Guest Name}:** {CTA text} -> linkedin.com/in/{handle}

---

## Thumbnails

### Title 1: {Title option 1}

**Text options:**
1. {3-5 WORD TEXT OVERLAY}
2. {3-5 WORD TEXT OVERLAY}
3. {3-5 WORD TEXT OVERLAY}

**Visual concept (Gemini prompt):**
> {Ready-to-use image generation prompt describing background, lighting, mood, composition, with space for text overlay and headshot}

### Title 2: {Title option 2}

**Text options:**
1. {3-5 WORD TEXT OVERLAY}
2. {3-5 WORD TEXT OVERLAY}
3. {3-5 WORD TEXT OVERLAY}

**Visual concept (Gemini prompt):**
> {Ready-to-use image generation prompt}

### Title 3: {Title option 3}

**Text options:**
1. {3-5 WORD TEXT OVERLAY}
2. {3-5 WORD TEXT OVERLAY}
3. {3-5 WORD TEXT OVERLAY}

**Visual concept (Gemini prompt):**
> {Ready-to-use image generation prompt}

---

## Short-Form Clip Candidates

### Clip 1: {Clip title}
- **Timestamp:** {HH:MM:SS} - {HH:MM:SS} (~{duration}s)
- **Type:** {hot-take|story|framework|stat|aha-moment|controversy|how-to}
- **Opening line:** "{exact first sentence}"
- **Why it works:** {one sentence}

### Clip 2: {Clip title}
- **Timestamp:** {HH:MM:SS} - {HH:MM:SS} (~{duration}s)
- **Type:** {type}
- **Opening line:** "{exact first sentence}"
- **Why it works:** {one sentence}

### Clip 3: {Clip title}
...

{Continue for all 5-8 clips}

---

## Clip Summary Table

| # | Title | Timestamp | Duration | Type |
|---|-------|-----------|----------|------|
| 1 | {title} | {start} - {end} | ~{duration}s | {type} |
| 2 | {title} | {start} - {end} | ~{duration}s | {type} |
| ... | ... | ... | ... | ... |
```

## Quality Checks

Before presenting output, verify:
- [ ] All 3 titles end with guest name, position, and company
- [ ] Titles are how-to or explanation-based with a curiosity gap
- [ ] Summary opens with the most interesting insight, not a preamble
- [ ] Each takeaway is specific and actionable, not a vague topic
- [ ] Learn More section captures every resource mentioned in the transcript
- [ ] Both CTAs are present (brand website + guest LinkedIn)
- [ ] Each title has 3 thumbnail text options (3-5 words each, ALL CAPS)
- [ ] Thumbnail text complements the title, does not repeat it
- [ ] Each title has a Gemini-ready visual concept prompt
- [ ] Visual prompts include space for text overlay and headshot
- [ ] 5-8 clip candidates identified with accurate timestamps from transcript
- [ ] Each clip has a strong opening line pulled directly from transcript
- [ ] Clip durations are 30-90 seconds
- [ ] No banned phrases from output style
- [ ] No hedging language or corporate jargon

## Example Usage

```
# Process a transcript file
/podcast {client_root}/podcasts/ep-012-transcript.txt --client {client_slug}

# Process with just a file path (no client context)
/podcast /path/to/timestamped-transcript.txt

# No arguments - will prompt for transcript paste
/podcast
```