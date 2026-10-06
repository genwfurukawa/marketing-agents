---
description: Generate the monthly CEO-grade AI visibility briefing - pulls weekly citation-scan data and retro deltas, and produces a standalone HTML report + strategic memo for client delivery.
argument-hint: [--client client-slug] [--month YYYY-MM] [--competitors "name1,name2,name3"]
allowed-tools: Task, Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
---

# Monthly Briefing

You produce the monthly CEO-grade AI visibility briefing. One artifact: a self-contained HTML file the client double-clicks. No login, no third-party tool. Backed by weekly citation scans (aeo-engine-scan) and four weekly retros (`/campaign-retro`).

---

## What This Produces

Three artifacts in `clients/{slug}/production/briefings/{YYYY-MM}/`:

1. **`report.html`** - self-contained HTML report, embedded CSS, inline chart.js for time-series. Client opens it locally or you host it.
2. **`strategic_memo.md`** - one-page CEO-language memo. Pipeline implications, not technical metrics.
3. **`briefing_data.json`** - the data the report was generated from (audit trail, regenerate-friendly).

---

## Inputs

Optional:
- `--client` - client slug (defaults to the active client: `CLIENT_CONFIG` env var pointing at the client's config.yaml)
- `--month` - target month YYYY-MM (defaults to last completed month)
- `--competitors` - override competitor list (defaults to `clients/{client}/config.yaml` competitors)

---

## Process

1. **Verify prerequisite data exists:**
   - At least 4 weekly scans in `clients/{slug}/research/aeo-scans/` (historical months may use `research/ahrefs/` pulls)
   - At least 4 weekly retros (`/campaign-retro` output) in `clients/{slug}/intelligence/retros/`
   - Current month's pull-analytics output in `clients/{slug}/research/analytics/`

   If any missing, list which and stop. Don't generate a briefing on incomplete data.

2. **Read context in parallel:**
   - `clients/{client}/config.yaml` (brand, competitors, visual_style)
   - `clients/{client}/config/brand-brain.md`
   - `clients/{client}/config/voice-guide.md`
   - The 4 weekly `engine_map.json` scan files for the month
   - The 4 weekly retros
   - The latest pull-analytics summary
   - Prior month's briefing (for MoM context)

3. **Compute monthly aggregates:**
   - SOV: month-end value, MoM delta, trend direction
   - Mentions: total for month, MoM delta
   - Impressions: total for month, MoM delta
   - **Source Control Rate**: month-end value, MoM delta (north-star metric, highlight prominently)
   - Top 5 cited pages on owned domains (new this month)
   - Top 5 winning queries (SOV improved most)
   - Top 5 gap queries (where client should win but doesn't)
   - New cited domains discovered this month (potential earned-authority targets)
   - Sentiment distribution

4. **Identify what moved.**
   - Pages published this month that drove citations
   - LinkedIn posts that drove engagement
   - Founder session atoms that surfaced in winning queries
   - Earned-authority placements (Reddit threads, G2 reviews, bylined content)

5. **Generate next-month plan.**
   - Top 5 content priorities (from gap-to-content-mapper-agent + the scan's gap queries)
   - Top 3 earned-source placements (from cited-domains analysis)
   - Expected score impact per priority

6. **Generate the strategic memo.** One page. CEO language. Read `clients/{client}/config/voice-guide.md` first. The memo must:
   - Lead with the headline number that matters (Source Control Rate or biggest delta)
   - Explain pipeline implications, not technical metrics
   - Name competitors and where you're winning/losing vs them
   - End with the single most important action for the next 30 days
   - No charts, no tables, just clear writing

   Example memo opening:
   > "Your Source Control Rate hit 34% this month, up from 19% three months ago. That means when buyers ask Claude or Perplexity about {category}, your owned content shapes the answer in 1 of every 3 responses. Three months ago, you weren't named at all."

7. **Render the HTML report.** Use the template at `templates/monthly_briefing/report.html.template`. Substitute:
   - `{{client_name}}`, `{{client_logo}}`, `{{client_colors}}` (from clients/{client}/config.yaml visual_style)
   - `{{month_label}}`, `{{generated_at}}`
   - `{{scorecard}}` - the 4 metric scorecard with deltas + arrows
   - `{{sov_history_chart}}` - inline chart.js time-series of SOV over 90 days
   - `{{source_control_chart}}` - SCR trend (the north star)
   - `{{competitor_table}}` - SOV vs 3 named competitors
   - `{{winning_queries}}`, `{{gap_queries}}` - bullet lists with metrics
   - `{{new_cited_domains}}` - bulleted list
   - `{{next_month_plan}}` - 3-section plan
   - `{{strategic_memo}}` - the one-page memo, rendered inline

8. **Write all outputs** to `clients/{slug}/production/briefings/{YYYY-MM}/`.

9. **Notion sync.**
   - Upload the HTML to a Notion page (or attach as file)
   - Append a "Monthly Briefings" row to the Visibility Scores DB with month, headline metric, link

10. **Render scorecard inline** via Ahrefs `render-scorecard` so the user previews the result in chat.

---

## HTML Report Requirements

- **Single file.** All CSS inline. Chart.js loaded from CDN (or inlined if offline delivery needed).
- **Brand the client, not the methodology.** Pull client visual_style from clients/{client}/config.yaml.
- **Print-friendly.** Test that "Print to PDF" produces a clean output - critical for client forwarding.
- **No external dependencies.** Image data is base64 or omitted. Fonts are system-safe.
- **Mobile-readable.** Single column on narrow screens.

Sections (in order):
1. Header: client logo, month, "AI Visibility Briefing"
2. Scorecard: 4 metric tiles with delta arrows
3. Source Control Rate spotlight (the north star)
4. SOV trend chart (90 days)
5. Competitor comparison table
6. What moved this month (3 bullets)
7. Winning queries (top 5 with metrics)
8. Gap queries (top 5 with content plan callouts)
9. New cited domains (earned-authority targets)
10. Next month plan (content + earned source + expected impact)
11. Strategic memo (full text)
12. Footer: methodology link, "Generated by {brand} (visibility ops methodology)"

---

## Critical Rules

1. **Never generate on incomplete data.** Missing weekly pulls = incomplete picture = bad decision. List missing data and stop.

2. **Source Control Rate is the headline.** Always lead with it. If it dropped MoM, that's the lead - not a metric to bury.

3. **CEO language only in the memo.** "Your buyers ask AI before they ask sales. You're now in 34% of those answers." Not "SOV improved by 0.15 to 0.34."

4. **Honest about losses.** If a competitor passed you on a key query, say so. The memo is a strategic asset, not a marketing piece. CEOs trust honesty.

5. **No metric without context.** Every number gets a MoM delta, a vs-competitor comparison, or a benchmark. Raw numbers are noise.

6. **The next-month plan must be specific.** "Build 3 comparison pages" is not specific. "Build comparison pages for {Brand} vs {C1}, {C2}, {C3} - expected SCR impact +5-8 points" is.

7. **No banned phrases.** Read `clients/{client}/config.yaml` voice.never_say. The memo applies voice rules just like LinkedIn content does.

8. **Print-test the HTML.** A briefing the CEO can't easily forward to their board is a briefing that doesn't get shared.

---

## Cron Cadence

This command runs automatically on Day 1 of each month at 6am via the `schedule` skill. Output is also Notion-synced and a Slack alert goes to the ops channel.

---

## Related

- Data source: weekly `aeo-engine-scan` runs + scorecard history (feed this monthly briefing)
- Analytics: `/pull-analytics` (GSC + GA4)
- Weekly retro: `/campaign-retro`
- Gap-to-content mapping: `gap-to-content-mapper-agent`
- HTML template: `templates/monthly_briefing/report.html.template`
- Memo voice: `clients/{client}/config/voice-guide.md`
