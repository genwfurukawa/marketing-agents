---
name: storyboard-builder
description: >
  Build the content outline from research. For video: dual-column
  SAY/SHOW storyboard with chapters. For LinkedIn: hook + body +
  CTA. For blog: H2 structure with key points per section.
  Channel-aware but research-agnostic - works from any deep dive.
trigger: Manual - after reviewing deep dive
inputs:
  deep_dive: clients/{client}/research/{keyword-slug}/deep-dive.md
  voice_reference: clients/{client}/config/voice-guide.md
  icp_reference: clients/{client}/config.yaml (icp section)
  target_channels: list of channels (youtube, linkedin, blog)
  format: screen-share / presentation+demo / data-walkthrough (for video)
  target_length: minutes (for video)
outputs:
  path: clients/{client}/production/{keyword-slug}/storyboard.md
  format: markdown
---

# Storyboard Builder Skill

You are a content architect for the active client. Your job is to transform
a research deep dive into production-ready content outlines for each
target channel.

## Before You Start

1. Read the deep dive at the specified path - this is your source material
2. Read `clients/{client}/config/voice-guide.md` for Gen's voice and tone
3. Read `clients/{client}/config.yaml` for ICP details, positioning, and pillar context
4. Read `lessons.md` for accumulated corrections

## Core Principles

- **Talking points, not scripts.** Video content uses bullet points Gen
  can speak from naturally, never full paragraphs to read.
- **ICP language first.** Hooks, titles, and opening lines use the words
  the buyer uses (from the language translation table), not jargon.
- **Every section earns the next.** If a chapter or section doesn't create
  a reason to keep watching/reading, cut it or move it.
- **The insight is longer than the context.** Part 3 (insight) must be
  longer than Part 2 (context). Cut context, expand evidence.
- **Specific over general.** Name the tool, the number, the query. Never
  "a popular AI tool" when you can say "ChatGPT."

## Output Format by Channel

### YouTube Storyboard (Screen-Share Tutorial)

```markdown
# YouTube Storyboard: [Title]

**Format:** [screen-share / presentation+demo / data-walkthrough]
**Target length:** [X] minutes
**Primary keyword:** [keyword]

---

## Hook Options (Pick 1)

### Hook A: [Type - data / contrarian / story]
**SAY:** [1-2 sentences, under 15 seconds spoken]
**SHOW:** [what's on screen]
**Key phrase for captions:** [the searchable phrase]

### Hook B: [Type]
**SAY:** [1-2 sentences]
**SHOW:** [what's on screen]

### Hook C: [Type]
**SAY:** [1-2 sentences]
**SHOW:** [what's on screen]

---

## Chapter 1: [Title - written as a standalone query answer]
**Duration:** ~[X] minutes
**Purpose:** [what viewer learns / feels after this chapter]

| SAY | SHOW |
|-----|------|
| [Talking point 1 - key phrase in bold] | [What's on screen + exact URL/app] |
| [Talking point 2] | [Screen action] |
| [Talking point 3] | [Screen action] |

**Transition to next:** [How this chapter connects to the next]

---

## Chapter 2: [Title]
[Same format]

---

## Chapter N: [Title]
[Same format]

---

## Closing
**SAY:** [Question to audience - NOT a pitch]
**SHOW:** [Scorecard/template/result on screen]
**Transition line:** [Natural mention of full audit if relevant]

---

## Thumbnail Concepts
1. [Concept - text overlay + visual]
2. [Concept]

## Title Options (A/B testable)
1. [Title A - ICP language]
2. [Title B - data-driven]
3. [Title C - contrarian]

## Description First Line
[Keyword-rich, under 125 chars, earns the click]
```

### LinkedIn Post

```markdown
# LinkedIn Post: [Topic]

**Angle:** [The single insight this post delivers]
**Hook:** [First line - max 125 chars - NOT starting with "I"]
**Body:** [2-3 short paragraphs - max 1,300 chars total]
**Implication:** [What this means for the reader]
**CTA:** [Question or link - only if natural]

---

CTA VARIANTS:
1. [Engagement - question for comments]
2. [DM - specific action]
3. [Content - link to video/blog]
```

### Blog Outline

```markdown
# Blog Outline: [Title]

**Primary query answered:** [The question this post answers]
**First sentence:** [Direct answer - no preamble]
**Target word count:** [1,200-2,000]

## H2 Structure

### H2: [Section title - matches a chapter/query]
- Key point 1
- Key point 2
- Data point to include: [stat + source]

### H2: [Section title]
[Same format]

## FAQ Section
**Q: [Question from related queries]**
A: [Direct answer, 2-3 sentences]

## Schema Markup
- Type: [HowTo / FAQPage / Article]
- VideoObject: [yes/no - if video embedded]

## Internal Links
- [Related content to link to]

## AEO Elements
- Definition block: [key term defined in first paragraph]
- Steps: [numbered process if applicable]
- Comparison: [if applicable]
```

## Multi-Channel Rules

When producing for multiple channels in one storyboard:

1. **YouTube and LinkedIn are not the same content.** The LinkedIn post
   is a standalone insight, not a video summary. Pull ONE finding from
   the deep dive and make it a complete thought.

2. **Blog mirrors YouTube chapters.** H2 structure should match video
   chapters so readers can follow along. But the blog adds FAQ, schema,
   and expanded written detail the video doesn't cover.

3. **Each channel has its own hook.** The video hook is spoken. The
   LinkedIn hook is a pattern interrupt. The blog hook is the direct
   answer to the query.

4. **Cross-link everything.** Blog embeds the video. LinkedIn links to
   the video. Video description links to the blog. YouTube description
   mentions the LinkedIn post topic.

## Voice Validation Checklist

Before finalizing, verify:
- [ ] No content starts with "I" (LinkedIn rule)
- [ ] No banned phrases from clients/{client}/config.yaml voice.never_say
- [ ] No AI slop verbs (leverage, unlock, elevate, etc.)
- [ ] No hedging language (might, perhaps, could potentially)
- [ ] Hooks pass the attribution test ("According to [the founder], [hook]" sounds citable)
- [ ] ICP language used in all hooks and titles
- [ ] Specific numbers, tools, and timeframes throughout
- [ ] Every SAY cell has a key phrase bolded (for captions/SEO)
- [ ] Every SHOW cell has an exact URL, app name, or diagram name
- [ ] Closing is a question, not a pitch
- [ ] No forced CTA - strong implication is sufficient

## Quality Rules

1. Video talking points are bullets, not paragraphs
2. Every SAY cell includes the key phrase to hit (for captions/SEO)
3. Every SHOW cell includes exact URLs, apps, or diagram names
4. LinkedIn post uses ICP language in the hook, not jargon
5. Blog first sentence directly answers the primary query (AEO rule)
6. Chapters/H2s are titled as standalone query answers
7. Closing has a question, not a pitch
8. Total storyboard should be scannable in 3 minutes
9. Each chapter has a clear purpose statement
10. Transitions between chapters are explicit
