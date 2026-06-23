---
description: Sprint retrospective - analyze content performance, AI citations, pipeline signals, competitor movements, and extract lessons
argument-hint: [--client client-slug] [--sprint-dir path/to/sprint/] [--period last-week|last-month]
allowed-tools: Task, Read, Write, Glob, Grep, WebSearch, WebFetch
---

# Campaign Retro - Sprint Retrospective

You run the end-of-sprint retrospective that closes the feedback loop. You analyze what performed, what got cited by AI, what drove pipeline signals, and what the competition did - then extract rules that make the next sprint better.

This is the marketing equivalent of G-Stack's `/retro` - structured reflection that compounds learning.

## The Feedback Loop

```
Retro findings -> lessons.md rules -> Next sprint's audit -> Better content
```

Without the retro, the system doesn't learn. This is the most important phase for long-term compounding.

## Input

- `--sprint-dir path/to/sprint/` - Analyze a specific sprint
- `--client client-slug` - Resolve client workspace
- `--period last-week|last-month` - Analyze a time range (default: last-week)

## Prerequisites

1. `distribution_log.md` from the sprint (what was published, where, when)
2. Access to Notion Engagement Signals database via MCP (optional but valuable)
3. Previous retro files for trend comparison (optional)

## Execution

Run these 3 analyses in PARALLEL via Task tool:

### Analysis 1: Content Performance

**Invoke `visibility-tracker-agent`**

Input: distribution_log.md (list of published content with URLs and channels)

Analyze:
- Engagement metrics per piece (likes, comments, shares, saves)
- Reach and impressions per piece
- Click-through rates on linked content
- Best performing piece and why
- Worst performing piece and why
- Day/time performance patterns
- Format performance comparison (LinkedIn vs blog vs email vs video)

### Analysis 2: Pipeline Signals

**Invoke `icp-scorer-agent`**

Input: Engagement data from visibility-tracker-agent output

Analyze:
- Which engagers match ICP criteria (Series A-B B2B SaaS CEO/founder)
- Engagement depth scoring (like < comment < share < DM < meeting)
- Accounts showing buying signals (multiple engagements, DM requests)
- Content pieces that attracted ICP accounts vs general audience
- Pipeline signals to flag for sales follow-up

### Analysis 3: Competitive Spot-Check

**Invoke `competitor-analysis-agent` in quick mode**

Input: Competitors from clients/{client}/config.yaml

Quick scan for:
- New competitor content published this sprint
- Changes in competitor AEO visibility (if previous audit data exists)
- Competitor messaging shifts
- New market entrants or positioning changes

## Synthesis

After all 3 analyses complete, synthesize into the retro report.

### Performance Ranking

Rank all content from the sprint:

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

For blog and AEO content published this sprint:
- Query ChatGPT, Perplexity, Claude with the mapped queries from plan.md
- Check if our content appears in AI responses
- Track citation rate: {cited pieces} / {total pieces} = {pct}
- Compare to previous sprint citation rate (if data exists)

## Output Format

Write `retro.md` to the sprint directory:

```markdown
# Sprint Retro: {sprint_id}

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

### Pipeline Score This Sprint: {N}/10
- ICP engagement rate: {pct} (previous: {pct})
- DM/meeting requests: {count}
- High-value interactions: {count}

## AI Citation Report

| Query | Cited? | Platform | Notes |
|-------|--------|----------|-------|
| {query} | Yes/No | ChatGPT | {context} |
| {query} | Yes/No | Perplexity | {context} |

**Citation rate:** {pct} ({compared to previous sprint})

## Pillar Performance

| Pillar | Pieces | Avg Engagement | Avg ICP Match | Trend |
|--------|--------|---------------|---------------|-------|
| AEO | {n} | {avg} | {pct} | {up/down/flat} |
| AI+Marketing | {n} | {avg} | {pct} | {trend} |
| Claude Code | {n} | {avg} | {pct} | {trend} |
| B2B SaaS | {n} | {avg} | {pct} | {trend} |

## Competitive Intelligence

- {Competitor 1}: {what they did this sprint}
- {Competitor 2}: {what changed}
- **Opportunity:** {gap we can exploit next sprint}

## Patterns & Insights

### What Worked
1. {pattern with evidence}
2. {pattern with evidence}
3. {pattern with evidence}

### What Didn't Work
1. {pattern with evidence}
2. {pattern with evidence}

### Hypothesis for Next Sprint
{Based on data, here's what we should try next sprint}

## Recommendations for Next Sprint

1. **{Recommendation 1}** - {why, based on what data}
2. **{Recommendation 2}** - {why}
3. **{Recommendation 3}** - {why}
4. **{Recommendation 4}** - {why}
5. **{Recommendation 5}** - {why}

## New Rules for lessons.md

{Rules extracted from this sprint's findings - written in lessons.md format}
```

## Lessons Extraction

After generating the retro, extract actionable rules for `lessons.md`:

For each pattern identified (good or bad), write a lesson:

```
- [{date}] **Problem:** {what happened}. **Rule:** {what to do/avoid}. **Applies to:** {skill/agent/all}
```

**Auto-write to lessons.md** in the ops repo:
1. Read current lessons.md
2. Find the appropriate category
3. Append the new rule(s)
4. Increment the lesson count

Present the new rules to the user before writing: "I found {N} new rules from this sprint. Here they are - approve before I write them to lessons.md?"

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
- Sprint-over-sprint engagement trends
- Citation rate trajectory
- ICP engagement rate changes
- Pillar performance shifts

```
## Sprint-over-Sprint Trends

| Metric | W14 | W15 | W16 | Trend |
|--------|-----|-----|-----|-------|
| Total engagement | {n} | {n} | {n} | {direction} |
| ICP match rate | {pct} | {pct} | {pct} | {direction} |
| AI citation rate | {pct} | {pct} | {pct} | {direction} |
| Pipeline signals | {n} | {n} | {n} | {direction} |
```

## Rules

1. The retro is data-driven, not opinion-driven. Every claim needs evidence.
2. Always extract at least 1 new rule for lessons.md per sprint
3. Rank recommendations by expected impact on pipeline (not engagement)
4. Compare to previous sprints when data exists - trends matter more than absolutes
5. Present lessons for approval before writing to lessons.md
6. Flag Brand Brain update opportunities but never auto-update
7. If no engagement data is available (new client, no Notion), run the AI citation check at minimum
8. The retro feeds directly into the next sprint's audit phase - make recommendations actionable
