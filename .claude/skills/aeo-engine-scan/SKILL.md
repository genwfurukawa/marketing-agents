---
name: aeo-engine-scan
description: "Use when checking whether a brand actually appears in AI answers across
multiple engines for a query bank, and you want ONE unified presence map instead of
running each engine separately. Triggers on: 'scan my AEO across engines', 'where do
I show up in AI search', 'check ChatGPT/Perplexity/Gemini/Google AI Overviews for my
brand', 'run my query bank across all engines', 'unified AI visibility scan',
'multi-engine citation check'. Wraps the Perplexity scanner, Claude direct scan, and
Ahrefs Brand Radar, and adds a documented method for the API-less surfaces (Google
AI Overviews, Copilot). Output feeds Dimension 3 + 9 of the visibility rubric and the
gap matrix. For decay-over-time tracking, see citation-decay-monitor."
metadata:
  version: 1.0.0
---

# AEO Engine Scan

This is the unified multi-engine citation tester. Today the toolkit measures AI
visibility in three separate places — `scripts/aeo_audit/` (Perplexity), a Claude
direct scan, and `ahrefs-pull` (Brand Radar for ChatGPT/Gemini) — plus Google AI
Overviews is checked by hand. This skill runs them as one pass against a single
query bank and returns one presence/position/citation map, so Dimension 3 (AI Search
Presence) and Dimension 9 (Citation Share) can be scored without stitching outputs
together.

## What This Measures

For each query × engine, three things:
1. **Presence** — `featured` | `cited` | `mentioned` | `absent`
2. **Position** — where the brand appears (first cited? buried? char position %)
3. **Citation** — which URL/domain the engine cited (own vs competitor vs 3rd-party)

The north-star metric out of this is **Source Control Rate** = citations to owned
domains / total citations — same definition as `ahrefs-pull`, computed here across
all engines at once.

## Before Starting

You need:
1. **A query bank** — from `/build-query-bank` or `02_query_bank.csv` in an audit.
   If none exists, run `/build-query-bank` first. 20-30 tagged queries.
2. **Brand + domain + competitors** — for presence/citation attribution.
3. **Available engine access** — check which of these are wired:
   - Perplexity API key (`PERPLEXITY_API_KEY`) → `scripts/aeo_audit/aeo_audit.py`
   - Anthropic API key → Claude direct scan with web_search
   - Ahrefs Brand Radar MCP → ChatGPT + Gemini (and historical)
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
Run each Tier 1 + Tier 2 query through the Anthropic API with the web_search tool.
Capture: does the answer mention the brand? cite its URL? what position? Reuse the
`_inputs/claude_direct_scan.py` pattern from `/audit-blueprint`.

### ChatGPT + Gemini (Ahrefs Brand Radar)
Invoke `ahrefs-pull` (or the Brand Radar MCP tools directly) for SOV, mentions,
cited domains/pages, and sample AI responses. Brand Radar lags 1-2 weeks after
prompts are seeded — if prompts aren't populated yet, mark these engines
`pending`, not `absent`.

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

3. Save the query bank used alongside, so `citation-decay-monitor` can re-run the
   identical set later.

## Hand-offs

- Absent-but-competitor-cited queries → `cited-page-teardown` (why do they win?)
- The whole `engine_map.json` → feeds Dimension 3 + 9 scoring in the rubric and the
  `05_gap_matrix` deliverable
- Re-run on a cadence → `citation-decay-monitor` diffs successive scans

## Quality Gate

- [ ] Every engine labeled measured / sampled / pending / skipped — no silent drops
- [ ] AIO + Copilot results flagged `method: sampled`, never presented as exact
- [ ] Brand Radar engines marked `pending` (not `absent`) when prompts aren't seeded
- [ ] Source Control Rate computed with the owned-domain list stated
- [ ] Absent-but-competitor-cited queries surfaced for teardown
- [ ] Query bank saved with the scan for reproducible decay tracking
