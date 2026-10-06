---
name: aeo-engine-scan
description: "Use when checking whether a brand actually appears in AI answers across
multiple engines for a query bank, and you want ONE unified presence map instead of
running each engine separately. Triggers on: 'scan my AEO across engines', 'where do
I show up in AI search', 'check ChatGPT/Perplexity/Gemini/Google AI Overviews for my
brand', 'run my query bank across all engines', 'unified AI visibility scan',
'multi-engine citation check'. Wraps the multi-engine scanner (scripts/aeo_audit:
Perplexity, ChatGPT, Claude, Gemini) and adds a documented method for the API-less
surfaces (Google AI Overviews, Copilot). Output feeds the Answer Test section of the Citability Score and the
gap matrix. Also owns decay-over-time tracking (decay mode): 'check for citation
decay', 'did my AI visibility drop', 'am I still cited', 'compare this scan to last
month' — re-runs the saved bank and diffs against the prior scan."
metadata:
  version: 1.0.0
---

# AEO Engine Scan

This is the unified multi-engine citation tester. The toolkit measures AI
visibility through `scripts/aeo_audit/aeo_audit.py --engines
perplexity,chatgpt,claude,gemini`, plus a sampled method for Google AI
Overviews. This skill runs them as one pass against a single
query bank and returns one presence/position/citation map, so the Answer Test section of the
Citability Score can be graded without stitching outputs together.

## What This Measures

For each query × engine, three things:
1. **Presence** — `featured` | `cited` | `mentioned` | `absent`
2. **Position** — where the brand appears (first cited? buried? char position %)
3. **Citation** — which URL/domain the engine cited (own vs competitor vs 3rd-party)

The north-star metric out of this is **Source Control Rate** = citations to owned
domains / total citations — computed across all engines at once.

## Before Starting

You need:
1. **A query bank** — from `/build-query-bank` or `02_query_bank.csv` in an audit.
   If none exists, run `/build-query-bank` first. 20-30 tagged queries.
2. **Brand + domain + competitors** — for presence/citation attribution.
3. **Available engine access** — check which of these are wired:
   - Perplexity API key (`PERPLEXITY_API_KEY`) → `scripts/aeo_audit/aeo_audit.py`
   - Anthropic API key (`ANTHROPIC_API_KEY`) → Claude scan with web_search
   - OpenAI API key (`OPENAI_API_KEY`) → ChatGPT scan
   - Google GenAI key (`GOOGLE_GENAI_API_KEY`) → Gemini scan
   - Google AI Overviews + Copilot → no API; documented manual/WebSearch method

Degrade gracefully: scan whatever engines are available, and clearly label which
engines were measured vs skipped. Never silently drop an engine — the rubric scores
coverage *across 4 engines*, so a missing engine changes the denominator.

## How to Run Each Engine

### Perplexity (retrieval index — the real source ranking)
```
python scripts/aeo_audit/aeo_audit.py batch \
  --input {query_bank}.csv --domain {domain} --company "{Brand}" \
  --competitors "{c1,c2,c3}" --output {out}/perplexity/
```
This gives answer text + citations + per-domain frequency/position. This is the
strongest signal because it exposes the actual ranked sources, not just prose.

### Claude (Anthropic API + web_search)
Run via `aeo_audit.py --engines claude` (Anthropic API with the web_search tool).
Capture: does the answer mention the brand? cite its URL? what position?

### ChatGPT + Gemini (API)
Run via `aeo_audit.py --engines chatgpt,gemini` (`OPENAI_API_KEY` +
`GOOGLE_GENAI_API_KEY`). Both produce the same QueryResult shape as the
Perplexity scan, so the merged map needs no stitching. Historical Ahrefs
Brand Radar pulls (pre-2026-07) live in `research/ahrefs/` for baselines.

### Google AI Overviews + Copilot (no API)
Documented manual/WebSearch method (be explicit that this is a sampled estimate,
not API-exact):
1. For each Tier-1 query, run WebSearch (proxy for the retrieval surface) and record
   whether the brand/domain appears in the top results that an AI Overview would
   synthesize from.
2. Where possible, note if the query triggers an AI Overview at all (many B2B
   queries don't).
3. Flag every AIO/Copilot result as `method: sampled` so it's never confused with
   API-measured presence.

## Output

Write to `clients/{slug}/research/aeo-scans/{YYYY-MM-DD}/`:

1. `engine_map.json` — the structured matrix:
```json
{
  "scanned_at": "{YYYY-MM-DD}",
  "engines_measured": ["perplexity", "claude", "chatgpt", "gemini"],
  "engines_sampled": ["google_aio"],
  "engines_skipped": ["copilot"],
  "queries": [
    {
      "query": "best conversation intelligence tools",
      "tier": 1,
      "engines": {
        "perplexity": {"presence": "absent", "position_pct": null, "cited_url": null,
                       "competitor_cited": ["gong.io"]},
        "claude": {"presence": "mentioned", "position_pct": 0.7, "cited_url": null}
      }
    }
  ],
  "rollup": {
    "answer_rate": 0.42,
    "source_control_rate": 0.18,
    "per_engine_coverage": {"perplexity": 0.30, "claude": 0.55},
    "share_of_voice": {"{brand}": 0.12, "gong.io": 0.34}
  }
}
```

2. `engine_map.md` — human-readable scorecard:
   - A query × engine grid (✅ featured / ◐ cited / · mentioned / ✗ absent / ⏳ pending)
   - Rollup metrics + which engines were measured vs sampled vs skipped
   - Top 5 queries where the brand is absent but a competitor is cited → these are
     the inputs to `cited-page-teardown`
   - Source Control Rate with the owned-domain list used

3. Save the query bank used alongside, so a later decay-mode run can re-run the
   identical set.

## Decay Mode — comparing successive scans

AI answers are not stable: a page cited last month can vanish when a competitor
publishes fresher content or the engine reweights sources. Decay mode makes
visibility a *tracked* metric. It detects and reports only — it never auto-fixes
or auto-publishes.

**Prerequisite:** a prior scan at `research/aeo-scans/{date}/engine_map.json` plus
its saved query bank. A diff is only valid on the identical query set + engines.
If only one scan exists, run the normal scan now as baseline and re-run in 2-4 weeks.

1. Re-run the identical scan (same bank, same engines) to a fresh dated folder.
2. Diff the two engine maps, classifying every query × engine transition:

| Transition | Meaning | Severity |
|------------|---------|----------|
| `featured`/`cited` → `absent` | **Hard decay** — lost the citation | 🔴 high |
| `featured` → `mentioned`/`cited` | **Soft decay** — demoted | 🟠 medium |
| owned URL cited → competitor URL cited | **Displacement** | 🔴 high |
| `absent` → `cited`/`featured` | **Gain** — new win | 🟢 report as wins |
| no change | stable | — |

3. Roll up headline deltas vs prior: Source Control Rate, answer rate, per-engine
   coverage, share of voice.
4. Attribute each hard decay/displacement: which page lost it, which competitor
   took it (→ `cited-page-teardown`), ranked cause hypotheses (stale content,
   fresher competitor page, engine reweighting, page moved/changed).

Write to `research/aeo-scans/{YYYY-MM-DD}_decay/`: `decay_report.md` (headline,
🔴 hard-decay table with hypotheses + recommended actions, 🟠 demotions, 🟢 wins —
don't bury the good news — and a watchlist) plus `decay.json` for trend charts and
the Notion Visibility Scores row. Stale-content decay hands to
`content-refresh-agent`; anything re-published goes **through the human gate**,
never auto. Cadence: monthly; biweekly for competitive categories.

## Hand-offs

- Absent-but-competitor-cited queries → `cited-page-teardown` (why do they win?)
- The whole `engine_map.json` → feeds the Answer Test scoring in the Citability rubric and the
  `05_gap_matrix` deliverable
- Re-run on a cadence in decay mode to diff successive scans

## Quality Gate

- [ ] Every engine labeled measured / sampled / pending / skipped — no silent drops
- [ ] AIO + Copilot results flagged `method: sampled`, never presented as exact
- [ ] Unscanned engines marked `pending` (not `absent`) — never silently dropped
- [ ] Source Control Rate computed with the owned-domain list stated
- [ ] Absent-but-competitor-cited queries surfaced for teardown
- [ ] Query bank saved with the scan for reproducible decay tracking
