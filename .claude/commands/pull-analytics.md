---
description: Pull GA4 + Search Console data for the client. Date-partitioned CSVs and markdown summaries written to research/. Feeds the weekly planning review, /build-audit-report, /campaign-retro, and content-refresh-agent.
argument-hint: [--days 28] [--gsc-only|--ga4-only]
allowed-tools: Bash, Read, Glob
---

# Pull Analytics

Pulls Google Search Console (queries, pages, impressions, CTR, position) and Google Analytics 4 (sessions, sources, landing pages, conversions). Writes date-partitioned CSVs plus markdown summaries that other agents read directly.

## When to run

| Trigger | Why |
|---------|-----|
| `/campaign-retro` | Measure what shipped, week-over-week deltas in sessions, conversions, query positions |
| `/build-audit-report` | Combine GSC traffic data with AEO citation audit |
| `content-refresh-agent` | Auto-flag pages with declining position or impressions |
| Ad hoc | Anytime current performance data is needed |

Run weekly at minimum. The GSC API has a ~2 day lag, so daily pulls offer no signal advantage.

## Prerequisites

1. `.env` populated with:
   - `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`
   - `GOOGLE_OAUTH_TOKEN_PATH` (defaults to `scripts/google/token.json`)
   - `GA4_PROPERTY_ID` (9-digit numeric, from GA4 Admin → Property Settings)
   - `GSC_SITE_URL` (`sc-domain:example.com` for domain properties, `https://example.com/` for URL-prefix)
2. Python venv with deps installed:
   ```
   python3 -m venv venv && source venv/bin/activate
   pip install -r scripts/google/requirements.txt
   ```
3. First run opens browser for OAuth. Token caches at `scripts/google/token.json` (gitignored). Subsequent runs are silent.

If `.env` is missing keys, tell the user which ones and stop. Do not invent values.

## Execution

### Default (both pulls, 28 days)
```bash
source venv/bin/activate && python scripts/google/pull_all.py
```

### With explicit window
```bash
source venv/bin/activate && python scripts/google/pull_all.py --days 90
```

### One source only
```bash
source venv/bin/activate && python scripts/google/gsc_pull.py --days 28
source venv/bin/activate && python scripts/google/ga4_pull.py --days 28
```

## What it writes

```
research/
├── gsc/
│   ├── YYYY-MM-DD_queries.csv         # top 1000 queries: clicks, impressions, CTR, position
│   ├── YYYY-MM-DD_pages.csv           # top 1000 pages: same metrics
│   └── YYYY-MM-DD_summary.md          # top 20 by clicks + "high impressions, low CTR" fix candidates + top pages
└── ga4/
    ├── YYYY-MM-DD_sources.csv         # source/medium x sessions/engaged/conversions/users
    ├── YYYY-MM-DD_landing_pages.csv   # top landing pages with engagement + duration
    ├── YYYY-MM-DD_daily.csv           # daily series for trend math
    └── YYYY-MM-DD_summary.md          # top 15 sources + top 20 landing pages
```

Date-partitioned by execution date (YYYY-MM-DD). Re-running on the same day overwrites that day's files; running on different days creates a diffable history.

## After running

1. Read both `_summary.md` files for the headline numbers
2. For sprint audit: surface fix candidates and surging queries to the planning step
3. For sprint retro: compare today's CSVs to the prior sprint's CSVs for deltas
4. If a CSV is unexpectedly empty or shorter than expected, check `.env` keys and OAuth token validity (delete `scripts/google/token.json` to force a re-auth)

## Output

After successful pull, report:

```
Analytics pulled — {days}d window:
- GSC: {N} queries, {M} pages → research/gsc/{date}_*
- GA4: {sessions} sessions, {conversions} conversions, top source: {source}/{medium} → research/ga4/{date}_*
```

Do not summarize the data further — the summary.md files do that. Other commands consume the files.
