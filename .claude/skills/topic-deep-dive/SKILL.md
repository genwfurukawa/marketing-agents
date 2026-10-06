---
name: topic-deep-dive
description: >
  Full research package for one chosen content topic. Produces the
  intelligence brief Gen needs before creating any content - video,
  post, or article. Channel-agnostic research that feeds all formats.
trigger: Manual - when a topic is selected from the queue
inputs:
  topic: chosen topic
  keyword: primary keyword
  pillar: which pillar (a slug from the active client's config.yaml content.pillars)
  funnel_stage: awareness / education / activation / conversion
  target_channels: list of channels (youtube, linkedin, blog)
outputs:
  path: clients/{client}/research/{keyword-slug}/deep-dive.md
  format: markdown
---

# Topic Deep Dive Skill

You are a research analyst for the active client. Your job is to produce a complete
intelligence brief for a single content topic. This brief is what Gen reads before
creating any content - video, LinkedIn post, or blog article.

## Before You Start

1. Read `clients/{client}/config.yaml` for pillars (content.pillars), ICP details, positioning, and voice rules
2. Read `clients/{client}/config/voice-guide.md` for Gen's voice patterns and tone
3. Read `lessons.md` for accumulated corrections
4. Read `clients/{client}/config/icp-psyche.md` for the deep ICP profile. Resolve the active client via an explicit client slug argument, else the `CLIENT_CONFIG` env var pointing at the client's config.yaml

## Research Process

Execute these 6 research steps in order. Every stat needs a source.
Every URL needs to be real.

### Step 1: AI Citation Landscape

Run the primary keyword through AI search platforms. For each platform, capture
the full response and note:

- **What sources are cited** (company, URL, content type)
- **What format is cited** (YouTube video, blog post, documentation, research paper)
- **What's missing** from the response (gaps in the answer)
- **What's wrong** in the response (outdated info, inaccuracies)
- **Citation score** (0-3 scale):
  - 0 = Not mentioned at all
  - 1 = Mentioned but not as a primary recommendation
  - 2 = Cited as a source or recommendation
  - 3 = Featured prominently with link/attribution

Platforms to check:
- ChatGPT (latest model)
- Perplexity
- Google AI Overviews (if available for this query)
- Claude (for comparison)

Record the exact queries used and timestamp of each search.

### Step 2: Competing Content Analysis

Search YouTube AND Google for this topic. For the top 5-8 results across both:

**YouTube results:**
- Title, channel name, subscriber count
- View count, like count, comment count
- Video length, publish date
- Chapter structure (if any)
- Description quality (keywords, links, timestamps)
- What they cover well
- What they miss
- What we'd do differently
- Thumbnail style

**Blog/article results:**
- Title, domain, estimated domain authority
- Publish date, word count
- H2 structure
- Whether it has FAQ, schema markup, video embed
- What they cover well
- What they miss
- What we'd do differently

### Step 3: Statistics and Data

Web search for recent statistics (2025-2026 preferred). Each stat needs:
- The exact number or data point
- The source organization
- The publication date
- The URL
- One sentence on how to use it in content

Target 8-12 stats. These are credibility anchors for both video and written content.

Categories to search:
- Market size / adoption numbers
- Behavioral data (how buyers search)
- Performance data (what gets cited, what doesn't)
- Trend data (growth rates, trajectory)

### Step 4: Source URLs and Screenshots

Identify 5-10 specific URLs Gen should reference or show in content:
- The exact URL
- What's notable about the page
- How to use it (show on screen, link in description, cite as source)
- Whether it works as Excalidraw source material (diagrams, frameworks)

### Step 5: Related Queries

Gather related queries from multiple sources:
- YouTube autocomplete suggestions for the keyword
- Google People Also Ask questions
- Related searches from AI platform responses
- Questions from Reddit/forum discussions
- Queries from the same pillar cluster in `clients/{client}/config.yaml` content.pillars

For each related query, tag how to use it:
- **Title/Hook** = strong enough for a headline (YouTube, LinkedIn, blog H1)
- **Chapter/H2** = works as a section header
- **FAQ** = natural question-answer format
- **Depth** = technical detail for body content
- **Future content** = separate piece, not this one

### Step 6: Client Offer Tie-Back

Identify the natural connection to the client's offer (from config.yaml):
- Which offer tier relates (use the offers defined in the active client's config.yaml)
- The logical next step for someone who watches/reads this content
- NOT a pitch - the organic "if you want this done for you" moment
- A specific proof point or case study to reference (if available)

## Output Format

Write the research brief in this exact structure:

```markdown
# Deep Dive: [Topic]

**Keyword:** [primary keyword]
**Pillar:** [pillar name]
**Funnel stage:** [stage]
**Target channels:** [list]
**Research date:** [date]

---

## 1. AI Citation Landscape

### Query: "[exact query]"

**ChatGPT:**
[Full response summary]
- Sources cited: [list]
- Citation score: [0-3]
- Gap: [what's missing]

**Perplexity:**
[Full response summary]
- Sources cited: [list with URLs]
- Citation score: [0-3]
- Gap: [what's missing]

**Google AI Overview:**
[Response or "No AI Overview triggered"]
- Sources cited: [list]
- Citation score: [0-3]

### Landscape Summary
[2-3 sentences: who owns this topic in AI search right now?
What type of content gets cited? Where's the opening?]

---

## 2. Competing Content

### YouTube

| # | Title | Channel | Views | Length | Published | Gap |
|---|-------|---------|-------|--------|-----------|-----|
| 1 | [title] | [channel] | [views] | [length] | [date] | [what they miss] |

**Best-in-class example:** [which video and why]
**Our angle:** [how we differentiate]

### Blog / Articles

| # | Title | Domain | DA | Published | Structure | Gap |
|---|-------|--------|-----|-----------|-----------|-----|
| 1 | [title] | [domain] | [est DA] | [date] | [H2 count, FAQ, schema] | [what they miss] |

**Best-in-class example:** [which article and why]
**Our angle:** [how we differentiate]

---

## 3. Statistics and Data

| # | Stat | Source | Date | Use In |
|---|------|--------|------|--------|
| 1 | [number/data point] | [source + URL] | [date] | [hook / body / CTA] |

---

## 4. Source URLs to Reference

| # | URL | What's There | How to Use | Excalidraw? |
|---|-----|-------------|-----------|-------------|
| 1 | [url] | [description] | [show/cite/link] | [yes/no] |

---

## 5. Related Queries

### Title/Hook Candidates
- [query] - why it works as a hook

### Chapter/H2 Candidates
- [query]

### FAQ Candidates
- [question]

### Depth/Body Candidates
- [query]

### Future Content (Not This Piece)
- [query] - [why it's separate]

---

## 6. Client Offer Tie-Back

**Relevant offer:** [tier]
**Natural next step:** [what the viewer/reader would want next]
**Proof point:** [case study or data point to reference]
**Transition line:** [the organic moment, not a pitch]

---

## Research Notes

[Anything surprising, contrarian angles spotted, things that
changed your initial assumptions about this topic]

### Contrarian Angles (Best for Hooks)
- [angle 1]
- [angle 2]

### Channel-Specific Notes
- **YouTube:** [what makes this work as a video]
- **LinkedIn:** [the standalone insight for a post]
- **Blog:** [the definitive answer angle]
```

## Quality Rules

1. Every statistic MUST have a source URL and date
2. Every competitor analysis must include what they MISS
3. Source URLs must be real, verified pages
4. Include at least 3 reference points that translate to Excalidraw visuals
5. Note contrarian angles - these make better hooks
6. Tag which findings are best for video vs. LinkedIn vs. blog
7. Use ICP language from `clients/{client}/config.yaml` icp section when describing gaps
8. The research brief should be self-contained - Gen shouldn't need to search again
9. Prioritize 2025-2026 sources over older ones
10. If a stat seems too good to be true, flag it with a confidence level
