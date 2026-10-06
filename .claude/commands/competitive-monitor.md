---
description: Ongoing competitive intelligence - track competitor AEO visibility, messaging shifts, and content strategy changes week-over-week
argument-hint: [--client client-slug] [--competitors "name1,name2"] [--quick]
allowed-tools: Task, Read, Write, Glob, Grep, Bash, WebSearch, WebFetch
---

# Competitive Monitor - Ongoing Intelligence Loop

> **Engine note (2026-07-24):** citation/SOV tracking runs via the `aeo-engine-scan` skill (decay mode for deltas) over `scripts/aeo_audit/` multi-engine scans. (The 2026-05 Ahrefs Brand Radar path is retired.)

You track competitor movements in AI search visibility, messaging, and content strategy. You run on a recurring basis to detect changes that should influence the week's content planning.

## Purpose

The competitor-analysis-agent does deep one-time analysis. This command does ongoing monitoring - detecting **changes** since the last check. The difference matters:

- **competitor-analysis-agent**: "What is their full strategy?" (one-time deep dive)
- **competitive-monitor**: "What changed since last week?" (ongoing delta tracking)

## Input

- `--client client-slug` - Load competitor list from client config or clients/{client}/config.yaml
- `--competitors "name1,name2"` - Override with specific competitors
- `--quick` - Abbreviated scan (AEO visibility only, skip content/messaging analysis)

## Competitor Sources

Load competitor list from (in priority order):
1. Client Brand Brain Section 04 (Competitive Positioning)
2. `clients/{client}/config.yaml` competitors list
3. `--competitors` flag override

## Execution

### Step 1: AEO Visibility Scan

For each competitor, run the AEO audit on their domain:

```bash
python scripts/aeo_audit/aeo_audit.py audit \
  --queries "{competitor category queries}" \
  --domain "{competitor_domain}"
```

Use seed keywords from clients/{client}/config.yaml relevant to the competitor's category.

Track:
- Which AI queries cite the competitor (ChatGPT, Perplexity, Claude)
- Citation rate: {cited queries} / {total queries}
- Position when cited (first mention, secondary mention, deep in response)
- Which specific pages get cited

### Step 2: Compare to Previous Scan

Read the last competitive monitor report (if exists):
`clients/{slug}/research/competitors/monitor_{YYYY-WXX}.md`

Calculate deltas:
- New queries where competitor appears (gained visibility)
- Queries where competitor disappeared (lost visibility)
- Position changes (moved up/down in AI responses)
- New pages being cited that weren't before

### Step 3: Content Strategy Scan

Unless `--quick` flag is set:

**WebSearch for each competitor** (last 7 days):
- New blog posts or content pages
- LinkedIn posts from founder/CEO
- YouTube videos
- Press releases or news mentions
- Product announcements

Track:
- Publishing frequency changes
- New content themes or pillars
- Messaging shifts (new taglines, positioning language)
- New formats they're trying

### Step 4: Messaging Delta Detection

Compare current competitor messaging to documented positioning:

- Visit competitor homepage (WebFetch)
- Extract current tagline, hero copy, value props
- Compare to documented positioning from last scan
- Flag any changes

Common changes to watch for:
- Rebranding or new tagline
- Adding "AI" to their positioning (everyone's doing this)
- Changing pricing or packaging
- Targeting a new audience segment
- Shifting content pillars

## Output Format

Write to: `clients/{slug}/research/competitors/monitor_{YYYY-WXX}.md` (for a standalone client repo, the repo's `research/competitors/` directory)

```markdown
# Competitive Monitor: {YYYY-WXX}

**Client:** {client_slug}
**Scan date:** {date}
**Competitors tracked:** {count}

## AEO Visibility Comparison

| Competitor | Citation Rate | Change | Trend |
|------------|-------------|--------|-------|
| {name 1} | {pct} | {+/-} | {up/down/flat} |
| {name 2} | {pct} | {+/-} | {trend} |
| **Us** | {pct} | {+/-} | {trend} |

### Visibility Gains (Competitors Gaining on Us)

| Competitor | Query | Platform | Our Status |
|------------|-------|----------|------------|
| {name} | {query} | ChatGPT | Not cited |
| {name} | {query} | Perplexity | Cited but lower |

### Visibility Losses (Competitors Losing Ground)

| Competitor | Query | Platform | Opportunity |
|------------|-------|----------|-------------|
| {name} | {query} | Claude | They lost it, we can take it |

## Content Activity (Last 7 Days)

### {Competitor 1}
- **New content:** {count} pieces
- **Themes:** {what they published about}
- **Notable:** {anything significant}
- **Messaging change:** {yes/no - details if yes}

### {Competitor 2}
...

## Messaging Tracker

| Competitor | Previous Tagline | Current Tagline | Changed? |
|------------|-----------------|-----------------|----------|
| {name} | {old} | {current} | {Y/N} |

## Strategic Implications

### Threats
1. {What competitor moves threaten our positioning}

### Opportunities
1. {Where competitors are weak or absent that we can exploit}
2. {Queries where competitor lost visibility - we should target}

### Recommended Actions for Next Cycle
1. {Specific content piece to create in response}
2. {Positioning adjustment to consider}
3. {Query to target based on competitive gap}

## Raw Data

### AEO Audit Results
{Per-competitor citation data}

### Content URLs Tracked
{List of competitor content URLs discovered}
```

## Planning Integration

The competitive monitor feeds into the weekly planning in the Notion task loop (see docs/OPERATING.md):

1. Run `/competitive-monitor` before the week's planning
2. Planning reads the latest monitor report
3. Competitive gaps become content opportunities in the week's slate
4. `/campaign-retro` does a quick competitive spot-check to close the loop

## Scheduling

Recommended cadence:
- **Weekly**: Quick scan (`--quick`) ahead of the week's planning
- **Bi-weekly**: Full scan (content + messaging + AEO)
- **Monthly**: Deep dive (invoke competitor-analysis-agent for full strategy review)

## Historical Tracking

Each scan is saved with the ISO week in the filename. Over time, this builds a competitive intelligence timeline:

```
clients/{slug}/research/competitors/
  monitor_2026-W14.md
  monitor_2026-W15.md
  monitor_2026-W16.md
  monitor_2026-W17.md
```

`/campaign-retro` and the audit tools can read the full history to identify trends.

## Rules

1. Always compare to the previous scan - deltas matter more than absolutes
2. Flag competitor gains as potential threats, not just observations
3. Turn every competitive gap into an actionable content recommendation
4. Don't overreact to single-week changes - look for sustained trends
5. Save every scan for historical tracking
6. Quick mode should complete in under 5 minutes
7. Full mode can take 15-20 minutes across all competitors
8. Never reveal proprietary competitor data outside the client workspace
