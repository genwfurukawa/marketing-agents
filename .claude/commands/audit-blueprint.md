---
description: Run the full AEO Blueprint audit (the $3K paid audit deliverable). Produces 10 deliverables in research/audits/{YYYY-MM-DD}/ — visibility scorecard, query bank, 4-engine citation scan, keyword opportunities, competitor gap matrix, citation source map, top 10 content gap briefs, brand brain, 90-day roadmap, strategic memo.
argument-hint: --canonical-strategy /path/to/founder_strategy.md [--competitors "comp1.com,comp2.com,comp3.com,comp4.com,comp5.com"] [--engines "perplexity,claude,brand_radar,gaio"]
allowed-tools: Task, Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
---

# Audit Blueprint

> **Migration notice (2026-05-11):** This command originally drove citation scans through `scripts/aeo_audit/aeo_audit.py` (Perplexity-only). Visibility tracking is moving to **Ahrefs Brand Radar** via the `ahrefs-pull` skill. For new runs, prefer Brand Radar for SOV, cited domains, and mentions data. The legacy Perplexity script remains in `scripts/aeo_audit/` for ad-hoc spot-checks.

You produce the complete AEO Blueprint — the $3K paid audit deliverable. The workflow is the one we executed for Talkadot on 2026-04-23. Reproduce it for any client.

## What this command produces

Ten deliverables in `research/audits/{YYYY-MM-DD}/`:

1. `01_visibility_score.md` — 9-dimension AI Visibility Scorecard with evidence per sub-criterion
2. `02_query_bank.md/.csv/.json` — 25-40 queries (founder baseline + supplementary) tagged for engine + tier + format
3. `03_citation_scan/{engine}/` — Per-engine citation scan results + analysis
4. `04_keyword_opportunities.csv` — Striking-distance + low-difficulty + gap keywords with intent + format
5. `05_gap_matrix.md` — Competitors × queries × engines, WIN/LOSS/ABSENT scoring
6. `06_citation_sources.md` — Top cited domains across all engines + outreach action plan
7. `07_content_gaps/01..10_*.md` — 10 single-page content briefs ready for content team
8. `config/brand-brain.md` — 12-section Context Vault (populated; this is THE source-of-truth doc)
9. `09_90day_roadmap.md` — Sprint-by-sprint execution plan, 3 parallel tracks
10. `10_strategic_memo.md` — 3-5pp CEO-ready synthesis

Plus `00_INDEX.md` as the navigable wrapper.

The rubric used is `visibility-system/ai_visibility_score_rubric.md` (v1+).

## Prerequisites

Before running, the following must be in place (verify, don't assume):

1. **Canonical founder strategy doc** at the path passed via `--canonical-strategy`. This is the document the audit treats as canonical truth. For Talkadot it was `talkadot_aeo_strategy_arel.md`. Without this, the audit is generic.
2. **`clients/{client}/config.yaml` populated** with brand identifiers, ICP basics, positioning, voice rules, locked competitors, content pillars, brand colors, success metrics. (See Talkadot's `clients/{client}/config.yaml` for the schema.)
3. **`config/icp-psyche.md` populated** with deep ICP psyche.
4. **`.env` keys**: `ANTHROPIC_API_KEY`, `PERPLEXITY_API_KEY`, optional Ahrefs MCP connection.
5. **`scripts/aeo_audit/aeo_audit.py`** present and Python venv ready (`pip install -r scripts/aeo_audit/requirements.txt`).
6. **`scripts/google/`** present for GA4/GSC data pulls (`/pull-analytics`).
7. **Ahrefs MCP** connected (or `--engines` excludes Brand Radar).

If any prerequisite is missing, halt and tell the user what to populate. Do not invent.

## Execution sequence (6 phases over ~5 hours wall time)

### Phase 0: Pre-flight (5 min)
- Verify all prerequisites above
- Read canonical strategy doc from `--canonical-strategy`
- Read `lessons.md` (compounding rules)
- Create audit directory at `research/audits/{YYYY-MM-DD}/{_inputs,_raw,03_citation_scan/{perplexity,claude,brand-radar-chatgpt,brand-radar-gemini},07_content_gaps}`

### Phase 1: Foundation (45-60 min, mostly autonomous)

Run in parallel where possible:

1. **Update `clients/{client}/config.yaml`** with locked positioning, voice rules, brand colors, success metrics from canonical strategy doc.
2. **Write/update `config/icp-psyche.md`** from canonical doc + ICP psyche capture.
3. **Add to `lessons.md`** any new rules from the canonical doc (banned phrases, never-include rules, planner-first rules, etc.).
4. **WebFetch top pages** from client domain → `_inputs/{client}_site_extract.md`.
5. **Web research the founder** (LinkedIn, podcasts, talks, articles) → `_inputs/{founder}_voice_corpus.md`. Use general-purpose agent.
6. **Run icp-definition-agent** with config + canonical doc → `_inputs/icp_profile.json`. Quality gates must pass.
7. **Run positioning-agent** (after ICP) → `_inputs/positioning_framework.json`. Quality gates must pass.
8. **Run competitor-analysis-agent** with locked 5 competitors → `_inputs/competitive_analysis.md`.

### Phase 2: Query bank + Brand Radar prompt seeding (45 min, includes 1 human step)

1. **Run audience-question-miner-agent** TWICE — once for primary ICP, once for secondary ICP (if dual-ICP) → `_inputs/audience_questions_*.md`
2. **Build query bank** by writing/running `_inputs/build_query_bank.py`:
   - Include founder baseline queries VERBATIM (the success metric)
   - Add supplementary: competitor head-to-heads, category-defining queries, data-led wedge queries
   - Tag every query: side (per ICP), tier (1-3), category, intent, source, baseline-or-supplementary
   - Honor founder's content pillar weights
3. **Output** `02_query_bank.md`, `.csv` (for aeo_audit.py batch), `.json`
4. **Generate Brand Radar prompt list** (top 30) → `_inputs/brand_radar_prompts.md`
5. **HUMAN STEP** — Stop here. Show the user the query bank + the 30 prompts. Confirm bank or adjust. User pastes 30 prompts into Ahrefs Brand Radar UI. (Brand Radar populates 1-2 weeks; not on critical path for this audit cycle.)

### Phase 3: Multi-source data pulls (75 min, mostly parallel)

**Ahrefs Site Explorer** (per domain × all 6: client + 5 competitors):
- `site-explorer-metrics` (DR, traffic, refdomains snapshot)
- `site-explorer-domain-rating-history` (12-month)
- `site-explorer-top-pages` (top 15-25)
- `site-explorer-organic-competitors` (validate locked set, surface unknowns)
- `site-explorer-refdomains-history` (12-month)

**Ahrefs Keywords Explorer**:
- `keywords-explorer-matching-terms` for category seeds (find striking-distance KD<30 keywords)

**Ahrefs Brand Radar** (limited until prompts populate):
- `brand-radar-sov-overview` (baseline only)
- Re-run after 1-2 weeks for trend data

**Multi-engine citation scan**:
- **Perplexity**: `python scripts/aeo_audit/aeo_audit.py batch --input 02_query_bank.csv --output 03_citation_scan/perplexity/`. Then run `_inputs/analyze_perplexity.py` to compute Talkadot vs competitor coverage.
- **Claude**: Run `_inputs/claude_direct_scan.py` (uses Anthropic SDK with web_search tool on Tier 1+2 queries). Computes coverage same shape as Perplexity analysis.
- **ChatGPT + Gemini** via Brand Radar (deferred, populates over 1-2 weeks).
- **Google AI Overviews** — manual SERP capture for top 10 queries (optional Phase 5 follow-up).

**Site audit**:
- Run `ai-crawler-audit-agent` on client domain → `_raw/ai_crawler_audit.md` with 0-100 score.

All raw data lands in `_raw/`.

### Phase 4: Author/apply 9-dim Visibility Score Rubric (30 min)

If the rubric doesn't exist yet at `visibility-system/ai_visibility_score_rubric.md`, write it (one-time work; the rubric is reusable across all clients).

Then score the client against it, dimension by dimension. Each dimension's score must trace to a specific data source from `_raw/` or `_inputs/`. No estimating.

Output: `01_visibility_score.md` with full sub-criteria breakdown.

### Phase 5: Build the 10 deliverables (90-120 min)

1. **`01_visibility_score.md`** — Already done in Phase 4
2. **`02_query_bank.*`** — Already done in Phase 2
3. **`03_citation_scan/`** — Already populated in Phase 3
4. **`04_keyword_opportunities.csv`** — Run `_inputs/build_data_deliverables.py` (or write client-specific version)
5. **`05_gap_matrix.md`** — Same script
6. **`06_citation_sources.md`** — Same script
7. **`07_content_gaps/01..10_*.md`** — Write each brief manually using the data from gap matrix + Perplexity/Claude per-query winners + the 14 AEO page templates as structural reference. Each brief: query, current AI answer, winning competitor, what it takes to displace, page structure, FAQ candidates, schema requirements, internal links, proprietary-data hooks, estimated impact, voice notes.
8. **`config/brand-brain.md`** — Populate the 12 sections from Phase 1 inputs (icp-psyche + positioning + competitive analysis + voice corpus + locked entity description from canonical doc).
9. **`09_90day_roadmap.md`** — Sprint-by-sprint plan honoring founder's pillar weights. Three parallel tracks: Content, Technical, Authority/PR. Mark each task with owner + effort + output. Score-movement target per month.
10. **`10_strategic_memo.md`** — 3-5pp CEO synthesis. Headline picture, why-the-pattern, 9-dim scorecard table, top 5 critical findings, recommended next move (first 30 days), 90/180-day score projections, document map.

Plus `00_INDEX.md` as navigable wrapper.

### Phase 6: Wrap (10 min)

1. Verify all 10 deliverables exist and are non-empty
2. Update `lessons.md` with any new rules learned during the audit
3. Tell the user the audit is ready and surface the headline finding + the top 3 priority actions for the first 30 days

## Inputs from `--canonical-strategy`

The canonical founder strategy doc must contain (or you must clarify with the founder before running):

- **The two AEO games** — which one the founder prioritizes (Game A brand vs Game B category)
- **ICP precision** — primary + secondary, with explicit excluded personas
- **Locked entity description** — verbatim sentence
- **The N baseline queries that ARE the success metric** — verbatim
- **What we are NOT chasing** — exclusion rules
- **Unfair advantage / proprietary data** — what's published or publishable
- **Content pillars + weights**
- **Third-party validation targets** (directories + earned media)
- **Technical foundation requirements** (schema, llms.txt, etc.)
- **Measurement framework** (90-day + 180-day success metrics)
- **Voice guardrails** (banned words, brand colors, what we don't do)

If any are missing, halt and ask the founder.

## Helper scripts (reuse these)

These scripts are agency-portable. Copy from existing client repo to new client repo at start of each engagement:

- `scripts/aeo_audit/aeo_audit.py` — Perplexity citation scan (already exists in template)
- `scripts/google/auth.py` + `gsc_pull.py` + `ga4_pull.py` — GA4 + GSC pulls (`/pull-analytics`)
- Audit-time Python builders (lightweight, write fresh per client because data shape varies):
  - `_inputs/build_query_bank.py` — query bank generator
  - `_inputs/analyze_perplexity.py` — citation matrix from aeo_audit.py output
  - `_inputs/claude_direct_scan.py` — Claude Anthropic API scan
  - `_inputs/build_data_deliverables.py` — builds deliverables 04, 05, 06 from raw data

These scripts use only standard libs + `anthropic` + `python-dotenv`. Cost per audit: ~$1.50 in API calls (~$0.20 Perplexity + ~$1.30 Claude with web_search).

## Quality gates

Audit is complete only when:

- [ ] All 10 deliverables exist with non-empty content
- [ ] Visibility scorecard has every dimension scored with evidence per sub-criterion (no "TBD" without a documented reason)
- [ ] Query bank includes founder's baseline queries verbatim
- [ ] At least 2 of 4 AI engines measured (Brand Radar can be deferred but acknowledged)
- [ ] Gap matrix shows all locked competitors × all queries × measured engines
- [ ] 10 content gap briefs each have: current AI answer, winning competitor, displace strategy, page structure, FAQ, schema, links, proprietary-data hooks, impact estimate, voice notes
- [ ] Brand brain has all 12 sections populated (none with bracket placeholders)
- [ ] 90-day roadmap has sprint-by-sprint task assignments with owners
- [ ] Strategic memo includes the headline picture, scorecard table, top 5 findings, first-30-day recommendation
- [ ] INDEX links to all deliverables
- [ ] `clients/{client}/config.yaml`, `config/icp-psyche.md`, `config/brand-brain.md` are populated and consistent

## Output

After successful run, report to the user:

```
Audit complete: research/audits/{YYYY-MM-DD}/

Headline: {client} scored {N}/90 on the AI Visibility Scorecard (Grade {X}).
- Strongest dimensions: {top 2-3}
- Critical gaps: {bottom 2-3}
- 90-day target: {N+expected_movement}

Read in this order:
1. 10_strategic_memo.md (CEO-ready)
2. 01_visibility_score.md (the scorecard)
3. 09_90day_roadmap.md (the execution plan)

First 30-day priorities:
1. {top action}
2. {second action}
3. {third action}
```

## Reference

- Authoring example: `research/audits/2026-04-23/` — the Talkadot self-audit, first run of this command.
- Methodology source: `visibility-system/ai_visibility_score_rubric.md` v1
- Pricing context: This is the $3K AEO Blueprint deliverable. Two-week paid audit. Refundable if it doesn't surface 3+ quantified visibility gaps.
