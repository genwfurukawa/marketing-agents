---
description: Run the Citability Audit at any depth — Snapshot (free, 10 prompts), Gameplan (~50 prompts, six sections), Baseline (100 prompts, full deliverable set inside the Sprint), or Pulse (weekly re-run, deltas) — and package the client-facing report. One rubric (visibility-system/citability_score_rubric.md), one comparable score at every depth.
argument-hint: --depth snapshot|gameplan|baseline|pulse --company "Company Name" --domain company.com --competitors "comp1.com,comp2.com" [--canonical-strategy /path/to/founder_strategy.md] [--engines "perplexity,chatgpt,claude,gemini"] [--deal-size 50000]
allowed-tools: Task, Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
---

# Build Audit Report — the Citability Audit, four depths

You run and package the Citability Audit. Six sections (Answer Test, Structure,
Authority, Rivals, Presence, Gate), one 0-100 Citability Score, graded with
`visibility-system/citability_score_rubric.md` (v2). The same rubric powers
every depth, so a prospect's free Snapshot number is directly comparable to
their day-90 Pulse — that continuity is the sales story.

> Engine access (2026-07-24): scans run through
> `scripts/aeo_audit/aeo_audit.py --engines perplexity,chatgpt,claude,gemini`
> (keys: PERPLEXITY_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY,
> GOOGLE_GENAI_API_KEY). Google AI Overviews optionally via `google_aio`
> (SerpAPI/DataForSEO) or the documented sampled method in aeo-engine-scan.
> The Ahrefs Brand Radar path is retired; historical pulls live in
> `research/ahrefs/` as the pre-2026-07 baseline record.

## The four depths

| Depth | Product | Scope | Turnaround |
|---|---|---|---|
| `snapshot` | Free audit (sales tool) | 10 prompts, ChatGPT + Perplexity, score + top 3 gaps | Same day, automated |
| `gameplan` | $500 tripwire | ~50 prompts, 4 engines, all six sections graded, plan + 30-min walkthrough | 1 week |
| `baseline` | Inside the $4,500 Sprint | 100 prompts, 4 engines, all six sections, full deliverable set, 90-day plan | Days 3-10 of Sprint |
| `pulse` | Inside the Loop | Full portfolio re-run, deltas vs Baseline | Weekly, automated |

## Prerequisites (verify, don't assume)

All depths:
1. `clients/{client}/config.yaml` populated (brand identifiers, ICP basics, locked competitors). In a standalone client repo, paths resolve from the repo root.
2. `.env` engine keys for the engines you'll scan. Missing keys: scan what's available and label skipped engines — never silently drop one; the rubric marks unscanned engines "pending".
3. `lessons.md` read.

Baseline additionally:
4. **Canonical founder strategy doc** via `--canonical-strategy` — the audit treats it as canonical truth (the two AEO games, ICP precision, locked entity description, the founder's baseline prompts VERBATIM, exclusions, proprietary data, pillar weights, voice guardrails). If missing pieces, halt and ask the founder. Do not invent.
5. `clients/{client}/config/icp-psyche.md` populated.

Pulse additionally:
6. A prior Baseline (or Pulse) scan with its saved prompt bank — a diff is only valid on the identical prompt set.

## Depth: snapshot

1. Build 10 high-intent prompts from the five SOP query types ("what is {category}", "best {category} for {ICP}", "{brand} vs {competitor}", "how to {problem}", "{category} pricing") — use `/build-query-bank` logic, don't hand-wave.
2. Scan ChatGPT + Perplexity: `aeo_audit.py batch --engines perplexity,chatgpt`.
3. Score the Answer Test sample per the rubric; spot-check Gate (robots.txt fetch) and Structure (top page).
4. Output one page: score + grade, the top 3 gaps with the actual AI answer shown for each, and who wins instead. Format per the outbound hook: "{Competitor} gets recommended in {X} of them. You show up in {Y}."
5. **Snapshot reports auto-generate but NEVER auto-send.** Human review, always.

## Depth: gameplan

1. Prompt bank: ~50 prompts via `/build-query-bank` (all five query types, tiered, tagged).
2. Scan all 4 engines. Log presence / position / accuracy / sentiment per prompt per engine; save raw outputs.
3. Grade ALL six sections per the rubric: run `ai-crawler-audit-agent` (Gate), extractability checklist on priority pages (Structure), trust-signal grading (Authority), per-losing-prompt winner + format classification (Rivals), off-site inventory (Presence).
4. Deliverable: written report (six sections, each finding as issue / evidence / impact / fix / priority) ending in the exact game plan the Sprint would execute, plus the 30-minute walkthrough agenda.

## Depth: baseline (the full engagement audit — inside the Sprint)

Phased execution (salvaged from the retired /audit-blueprint workflow, regraded to the v2 rubric):

**Phase 0 — Pre-flight:** verify prerequisites, read canonical strategy doc + lessons.md, create `research/audits/{YYYY-MM-DD}/{_inputs,_raw,03_citation_scan/{perplexity,chatgpt,claude,gemini},07_content_gaps}`.

**Phase 1 — Foundation (parallel):** update config.yaml + icp-psyche.md from the canonical doc; WebFetch top site pages → `_inputs/site_extract.md`; research the founder's public voice corpus; run `icp-definition-agent` → `positioning-agent` → `competitor-analysis-agent` (locked competitor set).

**Phase 2 — Prompt bank (1 human step):** run `audience-question-miner-agent` (per ICP); build the 100-prompt bank — founder baseline prompts VERBATIM (they are the success metric) + supplementary head-to-heads, category definers, wedge prompts; tag every prompt (tier, category, intent, source). Output `02_query_bank.md/.csv/.json`. **Stop and confirm the bank with the user before scanning.**

**Phase 3 — Data pulls (parallel):** multi-engine scan `aeo_audit.py batch --input 02_query_bank.csv --engines perplexity,chatgpt,claude,gemini --output 03_citation_scan/`; `ai-crawler-audit-agent` → `_raw/ai_crawler_audit.md`; `/pull-analytics` for GA4/GSC evidence; optional `google_aio` scan. All raw data in `_raw/`.

**Phase 4 — Score:** grade all six sections with the v2 rubric, every sub-criterion traced to `_raw/`/`_inputs/` evidence. No estimating; unmeasurable = "pending". Output `01_citability_score.md`.

**Phase 5 — Deliverables:**
1. `01_citability_score.md` — the scorecard (Phase 4)
2. `02_query_bank.*` — the 100-prompt bank (Phase 2)
3. `03_citation_scan/` — raw per-engine results (Phase 3)
4. `04_gap_matrix.md` — competitors × prompts × engines, WIN/LOSS/ABSENT
5. `05_citation_sources.md` — top cited domains across engines (Presence inventory; fixing off-site stays out of scope)
6. `07_content_gaps/01..10_*.md` — 10 content briefs (per gap: current AI answer, winning competitor + format, displacement strategy, page structure per `templates/aeo_page_types/`, FAQ, schema, links, proprietary-data hooks, impact, voice notes)
7. `clients/{client}/config/brand-brain.md` — populate the 12 sections from Phase 1 inputs
8. `09_90day_roadmap.md` — the 90-day plan: critical fixes, high-impact moves, quick wins, in order, honoring founder pillar weights; score-movement target per month
9. `10_strategic_memo.md` — 3-5pp CEO synthesis (headline, scorecard table, top 5 findings, first-30-day move, 90/180-day projections)
10. `00_INDEX.md` — navigable wrapper

**Phase 6 — Wrap:** verify all deliverables non-empty, capture new lessons via `/compound`, surface the headline + top 3 first-30-day actions.

## Depth: pulse

1. Re-run the FULL prompt portfolio with the identical bank + engines (invoke `aeo-engine-scan` decay mode — it owns the diff/classification logic).
2. Compute per-prompt deltas (presence, position, accuracy, sentiment) vs Baseline and vs last week; update share of voice.
3. Attribute movement where possible: map each new citation to the shipped asset or fix that likely earned it, with ship date as evidence. No invented attribution.
4. Output feeds the Monday report: what moved / what it means / what happens next. Log raw results + deltas to the client repo; flag anomalies.
5. Quarterly: full re-grade of all six sections + prompt portfolio refresh (retire dead prompts, add emerging ones).

## Packaging (client-facing synthesis — all depths above snapshot)

**Scorecard table:**

```markdown
| Company | Citability Score | Grade | Citation Rate | Share of Voice |
|---------|-----------------:|-------|---------------|----------------|
| {client} | {score}/100 | {band} | {X}% | {X}% |
| {competitor_1} | {partial-score note} | — | {X}% | {X}% |
```

Competitors get partial scores only where data is observable (Answer Test,
Rivals, Presence) — labeled as partial, never padded.

**Gap analysis** (top 5, from the gap matrix): per gap show the ACTUAL AI
answer from the raw JSON (never paraphrase), sources cited, the winning
format, the mapped page-type template (only templates that exist in
`templates/aeo_page_types/`), and a starter brief.

**Executive summary** — exactly 3 paragraphs (current state / competitive gap /
recommended next steps), specific numbers only. Pipeline estimate formula:
`quarterly_pipeline = displacement_count × deal_size × 0.05 × 3`, always
labeled "directional estimate", never a guarantee.

## Quality gates

- [ ] Every number traces to a saved raw result (no fabricated metrics, no findings without evidence)
- [ ] Founder baseline prompts included verbatim (baseline depth)
- [ ] Engines labeled measured / sampled / pending / skipped — no silent drops
- [ ] Schema findings from rendered checks only (a static-fetch "no schema" is a false finding)
- [ ] Accuracy misses logged as their own fix category
- [ ] Gap briefs map only to templates that exist
- [ ] No banned phrases (`voice.never_say` + lessons.md) in anything client-facing
- [ ] Pipeline estimate labeled directional with the formula shown
- [ ] **Human review by Gen before anything reaches the client. Never auto-send. Snapshot included.**

## Output routing

Baseline: `research/audits/{YYYY-MM-DD}/` (numbered deliverables above).
Snapshot/Gameplan: `research/audits/{YYYY-MM-DD}_{depth}.md` (single file).
Pulse: `research/aeo-scans/{YYYY-MM-DD}_decay/` (via engine-scan decay mode).
All paths resolve from the client repo root (or `clients/{slug}/` for the demo).

After generating, present the summary (score, grade, top gaps, files written)
and wait for approval. Never mark complete without the human gate.
