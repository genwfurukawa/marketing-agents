---
name: citation-decay-monitor
description: "Use when checking whether content that used to be cited in AI answers
still is — catching citation decay before it costs pipeline. Triggers on: 'check for
citation decay', 'did my AI visibility drop', 'am I still cited', 'monitor my AEO
over time', 'what content lost its AI citations', 'compare this scan to last month'.
Re-runs a saved query bank, diffs against the prior aeo-engine-scan, and flags pages
that lost presence. Runs manually or on a schedule. Note: this is the read-only
monitor — the autonomous remediation loop is a separate, gated capability."
metadata:
  version: 1.0.0
---

# Citation Decay Monitor

AI answers are not stable. A page that Perplexity cited last month can vanish when a
competitor publishes something fresher, when the engine reweights sources, or when
the content goes stale. Audits are point-in-time; this skill makes visibility a
*tracked* metric by diffing successive `aeo-engine-scan` runs and flagging decay.

This is a **monitor** — it detects and reports. It does not auto-fix or auto-publish.
(The autonomous reflect→prioritize→execute loop that acts on these signals is a
separate, gated capability and is intentionally not part of this skill.)

## Before Starting

You need:
1. **A prior scan** — `aeo-engine-scan` output at
   `clients/{slug}/research/aeo-scans/{date}/engine_map.json`. If only one scan
   exists, there's nothing to diff — run `aeo-engine-scan` now to establish the
   baseline and tell the user to re-run this in 2-4 weeks.
2. **The saved query bank** from that prior scan (so the new run is identical — a
   diff is only valid if the query set matches).

## How It Works

### Step 1 — Re-run the identical scan
Invoke `aeo-engine-scan` with the **same query bank** and the same engines as the
baseline. Same inputs in → comparable outputs. Save the new scan to a fresh dated
folder.

### Step 2 — Diff the two engine maps
For each query × engine, compare prior vs current presence and citation:

| Transition | Meaning | Severity |
|------------|---------|----------|
| `featured`/`cited` → `absent` | **Hard decay** — lost the citation entirely | 🔴 high |
| `featured` → `mentioned`/`cited` | **Soft decay** — demoted | 🟠 medium |
| owned URL cited → competitor URL cited | **Displacement** — someone took the slot | 🔴 high |
| `absent` → `cited`/`featured` | **Gain** — new win | 🟢 (report as wins) |
| no change | stable | — |

Also roll up the headline metrics and their deltas: Source Control Rate, answer
rate, per-engine coverage, share of voice — vs the prior scan.

### Step 3 — Attribute and prioritize
For each hard decay or displacement:
- Which **page** lost the citation (map the previously-cited URL)
- Which **competitor** displaced it, if any (→ hand to `cited-page-teardown`)
- Likely cause hypotheses, ranked: content went stale (check publish/update date),
  competitor published fresher/better-structured content, engine reweighting, or the
  page changed/moved (check it still 200s and still has its definition block + FAQ).

## Output

Write to `clients/{slug}/research/aeo-scans/{YYYY-MM-DD}_decay/`:

1. `decay_report.md`:
   - **Headline:** "{n} citations lost, {n} displaced, {n} gained since {prior date}.
     Source Control Rate {x}% → {y}% ({±z})."
   - **🔴 Hard decay table** — query, engine, page that lost it, competitor now cited,
     hypothesis, recommended action
   - **🟠 Soft decay / demotions**
   - **🟢 New wins** (don't bury the good news — these prove the system works)
   - **Watchlist** — queries trending the wrong way but not yet lost
2. `decay.json` — structured diff for trend charts and for Notion sync (append a row
   to the Visibility Scores DB with the period and deltas, matching `ahrefs-pull`).

## Hand-offs

- Displacement rows → `cited-page-teardown` (reverse-engineer the winner)
- Stale-content decay → `content-refresh-agent` (refresh the page) then re-publish
  **through the human gate**, never auto
- Recurring decay on a key query → flag for the strategy backlog (gated loop)

## Cadence

Recommend monthly for most clients, biweekly for competitive categories. This skill
can be invoked on a schedule, but it only ever *reports* — any action it recommends
stays a human decision.

## Quality Gate

- [ ] New scan used the identical query bank + engines as the baseline
- [ ] Every transition classified (hard/soft/displacement/gain/stable)
- [ ] Decay attributed to a specific page where possible
- [ ] Headline metric deltas (esp. Source Control Rate) reported vs prior
- [ ] Wins reported alongside losses
- [ ] Recommended actions named, but nothing published/changed by this skill
