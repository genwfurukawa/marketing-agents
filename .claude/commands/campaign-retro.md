---
description: Campaign retrospective - analyze content performance, AI citations, pipeline signals, competitor movements, and extract lessons
argument-hint: [--client client-slug] [--campaign-dir clients/{slug}/production/distribution/{period}/] [--period last-week|last-month]
allowed-tools: Task, Read, Write, Glob, Grep, WebSearch, WebFetch, Skill, Bash
---

# Campaign Retro - Content Cycle Retrospective

You run the end-of-cycle retrospective that closes the feedback loop. You analyze what performed, what got cited by AI, what drove pipeline signals, and what the competition did - then extract rules that make the next cycle better.

This is the marketing equivalent of G-Stack's `/retro` - structured reflection that compounds learning.

## The Feedback Loop

```
Retro findings -> /compound -> lessons/ rules -> Next cycle's planning (the Notion task loop, see docs/OPERATING.md) -> Better content
```

Without the retro, the system doesn't learn. This is the most important step for long-term compounding.

## Input

- `--campaign-dir path/` - Analyze a specific campaign directory (under `clients/{slug}/production/distribution/`)
- `--client client-slug` - Resolve client workspace
- `--period last-week|last-month` - Analyze a time range (default: last-week)

## Prerequisites

1. `distribution_log.md` from the campaign (what was published, where, when)
2. Access to Notion Engagement Signals database via MCP (optional but valuable)
3. Previous retro files for trend comparison (optional)

## Execution

Run these 3 analyses in PARALLEL via Task tool:

### Analysis 1: Content Performance

**Analyze inline** from distribution_log.md + the Notion Engagement Signals DB via MCP (no agent):

Analyze:
- Engagement metrics per piece (likes, comments, shares, saves)
- Reach and impressions per piece
- Click-through rates on linked content
- Best performing piece and why
- Worst performing piece and why
- Day/time performance patterns
- Format performance comparison (LinkedIn vs blog vs email vs video)

### Analysis 2: Pipeline Signals

**Analyze inline** from the Analysis 1 engagement data (no agent):

Analyze:
- Which engagers match the ICP criteria from the active client's `config.yaml` (icp section) and `config/icp-psyche.md`
- Engagement depth scoring (like < comment < share < DM < meeting)
- Accounts showing buying signals (multiple engagements, DM requests)
- Content pieces that attracted ICP accounts vs general audience
- Pipeline signals to flag for sales follow-up

### Analysis 3: Competitive Spot-Check

**Invoke `competitor-analysis-agent` in quick mode**

Input: Competitors from clients/{client}/config.yaml

Quick scan for:
- New competitor content published this period
- Changes in competitor AEO visibility (if previous audit data exists)
- Competitor messaging shifts
- New market entrants or positioning changes

## Synthesis

After all 3 analyses complete, synthesize into the retro report.

### Performance Ranking

Rank all content from the campaign:

```
| Rank | Piece | Channel | Engagement | ICP Match | AI Cited | Score |
|------|-------|---------|------------|-----------|----------|-------|
| 1 | {title} | LinkedIn | {metrics} | {pct} | {Y/N} | {1-10} |
| 2 | {title} | Blog | {metrics} | {pct} | {Y/N} | {1-10} |
```

Score = weighted combination of engagement (30%), ICP match (30%), AI citation (20%), pipeline signals (20%)

### Pattern Extraction

Identify patterns from top and bottom performers:

**What worked:**
- Hook style: {which hook types performed best}
- Content pillar: {which pillar drove most engagement}
- Format: {which format performed best}
- Day/time: {when did content perform best}
- Evidence type: {what kind of proof resonated}

**What didn't work:**
- {patterns from underperforming content}

### AI Citation Check

For blog and AEO content published this period:
- Query ChatGPT, Perplexity, Claude with each piece's mapped queries (from its content brief or the client's query bank)
- Check if our content appears in AI responses
- Track citation rate: {cited pieces} / {total pieces} = {pct}
- Compare to the previous retro's citation rate (if data exists)

## Output Format

Write `retro.md` to the campaign directory (under `clients/{slug}/production/distribution/`):

```markdown
# Campaign Retro: {period_id}

**Client:** {client_slug}
**Period:** {start_date} - {end_date}
**Content published:** {count} pieces across {channels}

## Performance Summary

### Top Performers
1. **{title}** ({channel}) - {why it worked}
   - Engagement: {metrics}
   - ICP matches: {count}
   - AI cited: {Y/N}

2. **{title}** ({channel}) - {why it worked}
   ...

### Underperformers
1. **{title}** ({channel}) - {why it underperformed}
   - Engagement: {metrics}
   - Diagnosis: {what went wrong}
   - Lesson: {what to do differently}

## Pipeline Signals

### Hot Accounts (ICP Match + High Engagement)
| Account | Role | Engagement | Content | Signal |
|---------|------|------------|---------|--------|
| {name} | {title} | {type} | {piece} | {recommendation} |

### Pipeline Score This Period: {N}/10
- ICP engagement rate: {pct} (previous: {pct})
- DM/meeting requests: {count}
- High-value interactions: {count}

## AI Citation Report

| Query | Cited? | Platform | Notes |
|-------|--------|----------|-------|
| {query} | Yes/No | ChatGPT | {context} |
| {query} | Yes/No | Perplexity | {context} |

**Citation rate:** {pct} ({compared to previous retro})

## Pillar Performance

One row per pillar from the active client's `config/pillars.md`:

| Pillar | Pieces | Avg Engagement | Avg ICP Match | Trend |
|--------|--------|---------------|---------------|-------|
| {pillar_1} | {n} | {avg} | {pct} | {up/down/flat} |
| {pillar_2} | {n} | {avg} | {pct} | {trend} |
| {pillar_n} | {n} | {avg} | {pct} | {trend} |

## Competitive Intelligence

- {Competitor 1}: {what they did this period}
- {Competitor 2}: {what changed}
- **Opportunity:** {gap we can exploit next cycle}

## Patterns & Insights

### What Worked
1. {pattern with evidence}
2. {pattern with evidence}
3. {pattern with evidence}

### What Didn't Work
1. {pattern with evidence}
2. {pattern with evidence}

### Hypothesis for Next Cycle
{Based on data, here's what we should try next cycle}

## Recommendations for Next Cycle

1. **{Recommendation 1}** - {why, based on what data}
2. **{Recommendation 2}** - {why}
3. **{Recommendation 3}** - {why}
4. **{Recommendation 4}** - {why}
5. **{Recommendation 5}** - {why}

## New Rules Captured (via /compound)

{For each pattern extracted this cycle: the problem, the falsifiable rule, and the scope it applies to - the candidates handed to /compound below}
```

## Lessons Extraction

After generating the retro, capture each durable pattern as a lesson through the `/compound` skill - never by hand-editing the store. `/compound` classifies the learning, checks for overlap with existing lessons (updating instead of duplicating), writes `lessons/{category}/{slug}.md`, and regenerates the `lessons.md` index.

1. From the retro's "What Worked / What Didn't Work" patterns, draft the candidate lessons: problem (the concrete symptom) + the falsifiable rule + the scope it applies to. A pattern with no reusable rule is not a lesson - skip it.
2. **Interactive runs:** present the candidates first - "I found {N} new rules from this cycle. Approve before I capture them?" - then for each approved candidate invoke `/compound mode:headless` with the problem/rule/scope as context. Headless mode runs the capture mechanics without re-prompting (approval already happened here).
3. **Automated / scheduled runs (no human):** invoke `/compound mode:headless` directly for each candidate. It classifies and writes conservatively, and defers a genuinely ambiguous scope to a `workflow` lesson rather than guessing.
4. Do not append to `lessons.md` or edit `lessons/` files directly - `/compound` is the single capture path and owns index regeneration (the lesson count is derived, not incremented).

## Brand Brain Updates

If the retro reveals patterns that should update the Brand Brain:

- Top-performing hooks -> Section 08 (Writing Style Rules) or Section 10 (Reference Examples)
- Pillar performance shifts -> Section 05 (Brand POV) pillar weighting
- CTA conversion data -> Section 11 (CTAs)
- Platform-specific findings -> Section 12 (Platform Guidelines)

Flag these for the user: "These retro findings suggest updating Brand Brain sections {X, Y}. Want me to draft the updates?"

Do NOT auto-update the Brand Brain. Always get approval first.

## Trend Tracking

If previous retro files exist, compare:
- Cycle-over-cycle engagement trends
- Citation rate trajectory
- ICP engagement rate changes
- Pillar performance shifts

```
## Cycle-over-Cycle Trends

| Metric | W14 | W15 | W16 | Trend |
|--------|-----|-----|-----|-------|
| Total engagement | {n} | {n} | {n} | {direction} |
| ICP match rate | {pct} | {pct} | {pct} | {direction} |
| AI citation rate | {pct} | {pct} | {pct} | {direction} |
| Pipeline signals | {n} | {n} | {n} | {direction} |
```

## Rules

1. The retro is data-driven, not opinion-driven. Every claim needs evidence.
2. Capture at least 1 new lesson per retro via `/compound` (when a reusable pattern exists)
3. Rank recommendations by expected impact on pipeline (not engagement)
4. Compare to previous retros when data exists - trends matter more than absolutes
5. Present candidate lessons for approval before capturing them via `/compound mode:headless` (interactive runs)
6. Flag Brand Brain update opportunities but never auto-update
7. If no engagement data is available (new client, no Notion), run the AI citation check at minimum
8. The retro feeds directly into the next planning cycle in the Notion task loop (see docs/OPERATING.md) - make recommendations actionable
