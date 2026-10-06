# Citability Score — Six-Section Rubric (v2)

**Authored:** 2026-07-24
**Source:** SOP 1 (Citability Audit) in the business repo, with measurable
sub-criteria ported from the retired 9-dimension AI Visibility Score rubric
(v1, 2026-04-23 — see git history for the full v1 text).
**Status:** Canonical. One rubric powers every depth: Snapshot, Gameplan,
Baseline, Pulse. The number a prospect sees in a free Snapshot is directly
comparable to their day-90 Pulse.

---

## Scoring scale

One 0-100 score across six sections. Section weights are fixed by SOP 1:

| Section | Weight |
|---|---|
| 1. Answer Test | 30 |
| 2. Structure | 20 |
| 3. Authority | 20 |
| 4. Rivals (gap severity, inverted) | 10 |
| 5. Presence | 10 |
| 6. Gate | 10 |

**Gate override:** a hard Gate failure (AI retrieval bots blocked, or
site-wide noindex) caps the total score at 40 regardless of other sections —
nothing else matters until it's fixed.

**Grade bands:** 0-39 Invisible · 40-59 Present · 60-79 Cited · 80+ Recommended.

The rubric is **inputs-driven**: every score traces to a tool output, a logged
engine response, or a documented inspection. If you cannot point to the data,
you cannot give the score. Mark unmeasurable sub-criteria "pending", never
estimated.

---

## Section 1: The Answer Test (30 pts) — are you in the answer?

Run the prompt portfolio across ChatGPT, Perplexity, Claude, and Gemini
(`python scripts/aeo_audit/aeo_audit.py --engines perplexity,chatgpt,claude,gemini`),
log presence / position / accuracy / sentiment per prompt per engine.

| Sub-criterion | Points | How to measure |
|---|---|---|
| Citation rate across 4 engines | 0-12 | Per engine: (prompts where present / total) × 3. Each engine contributes 0-3. Unscanned engine = "pending", not 0. |
| Position when present | 0-6 | Avg presence quality: featured = 3, cited = 2, mentioned = 1, absent = 0, normalized to 6. First-recommendation slots weigh double. |
| Share of voice vs top 3 competitors | 0-6 | Brand citations / (brand + top-3-competitor citations): 40%+ = 6, 25-40% = 4, 10-25% = 2, <10% = 0 |
| Accuracy | 0-4 | Does the engine describe product, ICP, and pricing correctly? Score each logged answer 0-2, average, ×2. Every accuracy miss is also logged as a distinct fix item — wrong answers are a different defect class from absence. |
| Sentiment | 0-2 | Mostly positive framing = 2, neutral = 1, negative = 0 |

**QA gate:** raw engine outputs saved to the client repo
(`research/aeo-scans/` or the audit's `03_citation_scan/`). No
summarized-from-memory results, ever.

## Section 2: Structure (20 pts) — can AI extract you?

Score each priority page against the extractability checklist; the fail list
becomes the Structure fix queue.

| Sub-criterion | Points | How to measure |
|---|---|---|
| Answer-first blocks | 0-6 | Direct answer in the first paragraph + key answers in 40-60 word self-contained blocks: pass rate across priority pages × 6 |
| Question-format H2/H3 | 0-3 | 50%+ of headings phrased the way people ask = 3, 25-50% = 2, some = 1, none = 0 |
| Tables and lists for the winning formats | 0-3 | Comparison tables on "vs" content + numbered lists on process content = 3, partial = 1-2, none = 0 |
| FAQ blocks with natural-language questions | 0-2 | Present on priority pages = 2, some = 1, none = 0 |
| Schema present and correct | 0-3 | Article/FAQPage/HowTo/Product/Organization where applicable, verified by RENDERED check (never a static fetch) = 3, partial = 1-2, none = 0 |
| Freshness + authorship visible | 0-3 | Visible last-updated date (0-1) + author name and credentials (0-2) |

Also check: one clear idea per paragraph, no buried leads, AEO page-type
coverage vs `templates/aeo_page_types/` (14 types) as the content-architecture
evidence for the fix plan.

## Section 3: Authority (20 pts) — can AI trust you?

| Sub-criterion | Points | How to measure |
|---|---|---|
| Cited sources with links | 0-4 | The largest measured citation boost. Priority pages citing named, linked sources: most = 4, some = 2, none = 0 |
| Specific statistics with attribution | 0-3 | Present across priority pages = 3, some = 1-2, none = 0 |
| Expert quotes with name and title | 0-2 | Present = 2, some = 1, none = 0 |
| Original data or research | 0-4 | Published original study/statistics page = 4, in progress = 2, none = 0. The strongest long-term differentiator (see original-research-designer). |
| E-E-A-T | 0-3 | Author pages + credentials + first-hand experience shown: all = 3, partial = 1-2, none = 0 |
| Off-site trust scale | 0-2 | Referring-domain scale and diversity (news, .edu, directories, communities): strong = 2, moderate = 1, thin = 0. Evidence: any DR/refdomain checker output or a documented inspection — never estimated. |
| Entity consistency | 0-2 | Locked entity description consistent across site, LinkedIn, directories + knowledge-graph presence (Wikidata/Wikipedia): consistent = 2, mostly = 1, scattered = 0 |

**Negative check:** keyword stuffing actively reduces AI visibility. Any
stuffed priority page deducts 2 points and is flagged as a defect, not a
neutral.

Cap the section at 20 (sub-criteria total 20; deductions can pull below).

## Section 4: The Rivals (10 pts, inverted) — who's winning instead?

Lower gap severity = more points. Per losing prompt: name the citation winner,
the exact page cited, and classify the winning format (comparison, definitive
guide, original research, listicle, product page, how-to). Expect comparison
content to dominate.

| Sub-criterion | Points | How to measure |
|---|---|---|
| Displacement severity | 0-4 | % of tracked prompts where a competitor is cited and the brand is absent: <20% = 4, 20-40% = 3, 40-60% = 2, 60-80% = 1, 80%+ = 0 |
| Winner-format coverage | 0-3 | Of the losing prompts, % where the brand already has (or has queued) a page in the winning format: most = 3, some = 1-2, none = 0 |
| Trend vs prior scan | 0-3 | Gaps closing since last measurement = 3, flat = 2, widening = 0. First scan: mark "pending". |

The per-prompt winner list feeds `cited-page-teardown` and the content plan
directly.

## Section 5: Presence (10 pts) — does AI hear about you elsewhere?

**Inventory only. Measuring is in scope; fixing off-site is out of scope**
(Loop guardrail — Presence gaps are the built-in expansion conversation).

| Sub-criterion | Points | How to measure |
|---|---|---|
| Listicle/roundup presence | 0-4 | Of the third-party "best of" pages engines cite for tracked prompts, % where the brand appears: most = 4, some = 2, none = 0 |
| Review-site presence + recency | 0-3 | G2/Capterra/TrustRadius listed with reviews in the last 6 months = 3, listed but stale = 1-2, absent = 0 |
| Community + reference coverage | 0-3 | Brand appears in the Reddit threads engines cite (0-1), Wikipedia/Wikidata presence and accuracy (0-1), YouTube coverage of key queries (0-1) |

## Section 6: The Gate (10 pts) — can AI reach you?

Every finding needs evidence (the robots.txt line, the rendered-check output).
No inferred findings.

| Sub-criterion | Points | How to measure |
|---|---|---|
| AI crawler access | 0-4 | robots.txt allows GPTBot, ChatGPT-User, PerplexityBot, ClaudeBot, Google-Extended, Bingbot: all = 4, most = 2-3, retrieval bots blocked = 0 AND the Gate override caps the total score at 40. CCBot noted separately (training-only; blocking is a legitimate choice). |
| Indexation health | 0-2 | Clean sitemap + no noindex on money pages + sane canonicals + no redirect chains = 2, issues = 1, broken = 0 |
| Rendering + speed | 0-2 | Content server-rendered (not locked behind heavy JS) and fast enough to crawl fully = 2, partial = 1, SPA-only shells = 0 |
| Schema detectable in rendered DOM | 0-1 | Verified with a rendered-browser check or Rich Results Test. Reporting "no schema" from a static fetch is a false finding and forbidden. |
| llms.txt | 0-1 | Present and curated at site root = 1 (see ai-crawler-fix) |

---

## The four depths (same rubric, different scope)

| Depth | Scope | Sections |
|---|---|---|
| **Snapshot** | 10 prompts, ChatGPT + Perplexity | Answer Test sampled + top 3 gaps; other sections spot-checked |
| **Gameplan** | ~50 prompts, 4 engines | All six sections graded |
| **Baseline** | 100 prompts, 4 engines | All six sections + full fix queues + 90-day plan |
| **Pulse** | Full portfolio re-run, weekly | Deltas vs Baseline (engine-scan decay mode); quarterly full re-grade |

Continuity is the sales story: Snapshot, Baseline, and Pulse numbers are the
same scale.

## v1 → v2 continuity map

For engagements scored on the retired 9-dimension rubric (0-90), the rough
mapping — do not convert scores numerically, re-score on v2 at the next touch:

| v1 dimension | v2 home |
|---|---|
| 3 AI Search Presence, 9 Citation Share | Answer Test |
| 4 Content Architecture | Structure |
| 1 Domain Foundation, 6 Brand Fingerprint, 8 Authority Signals | Authority (+ Gate for schema) |
| 7 Competitive Position | Rivals |
| 6 directories, 8 off-site pieces | Presence |
| 5 Technical AI Readiness | Gate |
| 2 Organic Discovery | Dropped as a scored section (organic data remains supporting evidence) |

## Anti-patterns (unchanged from v1 — they were right)

- Do not adjust the rubric mid-engagement to make a client look better. The rubric is the contract.
- Do not score without raw evidence. Every point traces to a logged response or documented inspection.
- Do not collapse two sections into one.
- Do not exceed a section's weight.
- Do not skip a section because data is hard to get — mark sub-criteria "pending" and re-score when measurable. Do not estimate.

## Versioning

| Version | Date | Notes |
|---|---|---|
| v1 | 2026-04-23 | 9 dimensions, 0-10 each, 90 total (retired; full text in git history) |
| v2 | 2026-07-24 | Rebuilt on SOP 1's six sections, 0-100, SOP weights + Gate override. Ahrefs-dependent sub-criteria replaced with engine-scan + inspection evidence. |
