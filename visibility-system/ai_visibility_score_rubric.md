# AI Visibility Score — 9-Dimension Rubric (v1)

**Authored:** 2026-04-23
**Source:** AEO Blueprint methodology (developed across client engagements in 2026 and operationalized as a reusable scoring asset)
**Status:** Canonical. Use this rubric for every AEO Blueprint engagement.

---

## Why this rubric exists

Every prospect we pitch the Blueprint to needs a defensible, reproducible AI Visibility Score. Without a rubric, scoring is opinion. With one, scoring is engineering. This document defines exactly what each of the 9 dimensions means, how each is measured, what data feeds it, and how the points map to a grade.

The rubric is **inputs-driven**: every score traces back to a tool, a query, or a documented inspection. No vibes. No founder-charm scoring. If we cannot point to the data, we cannot give the score.

---

## Scoring scale

Each dimension scored **0-10** with named sub-criteria.

**Total possible:** 90 points across 9 dimensions.

**Grade map:**

| Total | Grade | Meaning |
|---|---|---|
| 80-90 | A | Industry-leading. Already the cited answer in the category. |
| 65-79 | B | Strong AEO posture. Visible across most AI engines for primary queries. |
| 50-64 | C | Average for AEO-aware companies. Foundation present but content/architecture incomplete. |
| 35-49 | D | Weak. Authority may exist but content + technical layers leave significant capture on the table. |
| 0-34 | F | Effectively invisible to AI search. Foundational work required. |

---

## Dimension 1: Domain Foundation (10 pts)

**What it measures:** The structural credibility AI engines can assess from the domain itself, before any content quality judgment.

**Sub-criteria:**

| Sub-criterion | Points | How to measure |
|---|---|---|
| Domain Rating (Ahrefs) | 0-5 | DR/20, capped. DR 100 = 5 pts. DR 60 = 3 pts. DR 30 = 1.5 pts. |
| Homepage schema completeness | 0-3 | +1 each for: Organization, SoftwareApplication (or Product), AggregateRating. Capped at 3. |
| HTTPS + mobile-friendly + no major Core Web Vitals failures | 0-1 | Pass/partial/fail = 1/0.5/0 |
| Domain age (>3 years) | 0-1 | Pass = 1, fail = 0. Trust signal for AI engines. |

**Data sources:** Ahrefs `site-explorer-domain-rating` + `site-explorer-domain-rating-history`, page source inspection of homepage, Whois for domain age.

---

## Dimension 2: Organic Discovery (10 pts)

**What it measures:** How findable the brand is via traditional organic search, which directly correlates with how often AI engines have crawled and indexed the brand's content.

**Sub-criteria:**

| Sub-criterion | Points | How to measure |
|---|---|---|
| Total organic keywords ranked | 0-3 | <100 = 0, 100-1K = 1, 1K-5K = 2, 5K+ = 3 |
| Top-3 ranking keywords count | 0-3 | <10 = 0, 10-100 = 1, 100-500 = 2, 500+ = 3 |
| Striking-distance keywords (positions 4-20) | 0-2 | <50 = 0, 50-200 = 1, 200+ = 2 (these are immediate-promotion candidates) |
| Branded vs non-branded ratio | 0-2 | >70% non-branded = 2, 50-70% = 1, <50% = 0 (heavy branded reliance = weak organic discovery) |

**Data sources:** Ahrefs `site-explorer-metrics` (org_keywords, org_keywords_1_3), GSC `gsc-keywords` for striking distance + branded/non-branded split.

---

## Dimension 3: AI Search Presence (10 pts)

**What it measures:** Whether the brand actually appears as cited or mentioned in AI engine responses for category-relevant queries.

**Sub-criteria:**

| Sub-criterion | Points | How to measure |
|---|---|---|
| Coverage across 4 primary engines | 0-4 | (Cited query count / total queries) summed across ChatGPT, Claude, Perplexity, GAIO, divided by 4. Each engine contributes 0-1. |
| Average position when cited | 0-3 | Position 0-2 = 3, 3-5 = 2, 6-9 = 1, 10+ = 0 |
| Best engine coverage % | 0-2 | Best single-engine coverage: 50%+ = 2, 25-50% = 1, <25% = 0 |
| Multi-engine consistency | 0-1 | Cited in 3+ engines for same query (any) = 1, else 0 |

**Data sources:** scripts/aeo_audit/aeo_audit.py (Perplexity), Anthropic API direct queries (Claude), Brand Radar `ai-responses` (ChatGPT, Gemini), manual SERP inspection (GAIO).

---

## Dimension 4: Content Architecture (10 pts)

**What it measures:** Whether the brand has built the content scaffolding AI engines need to cite — definitional pages, comparisons, listicles, FAQs — across the 14 AEO page type templates.

**Sub-criteria:**

| Sub-criterion | Points | How to measure |
|---|---|---|
| AEO page type coverage | 0-5 | (Page types present / 14) × 5. The 14 types: What Is, Best Tools, Alternatives, Product Comparison, Integration, Statistics, Glossary, Use Case, Case Study, ROI, Competitor Review, Buyer Guide, FAQ Hub, Problem-Solution. |
| Internal linking depth | 0-2 | Hub-and-spoke architecture present = 2, partial = 1, flat/none = 0 |
| Average article depth | 0-2 | Avg words on top 10 indexed articles: 1500+ = 2, 800-1500 = 1, <800 = 0 |
| Question-format H2 density | 0-1 | 50%+ of H2s on key pages are question-format = 1, else 0 |

**Data sources:** Manual inspection of site (Ahrefs `site-explorer-top-pages` + WebFetch of top 10), templates/aeo_page_types/ for the 14 page types reference.

---

## Dimension 5: Technical AI Readiness (10 pts)

**What it measures:** Whether AI crawlers can actually access, parse, and extract structured information from the site.

**Sub-criteria:**

| Sub-criterion | Points | How to measure |
|---|---|---|
| AI bot access in robots.txt (GPTBot, ClaudeBot, PerplexityBot, CCBot, Google-Extended) | 0-3 | All 5 allowed = 3, 3-4 = 2, 1-2 = 1, all blocked = 0 |
| llms.txt present at root | 0-2 | Present + structured = 2, present minimal = 1, missing = 0 |
| Structured data on key pages (homepage, pricing, key product pages, FAQ pages) | 0-3 | Comprehensive (Organization + Product + FAQPage + BreadcrumbList present where applicable) = 3, partial = 1-2, minimal = 0 |
| Server-rendered (not SPA-only) for crawlable content | 0-1 | Critical pages SSR = 1, SPA shells with no SSR = 0 |
| Sitemap freshness + comprehensiveness | 0-1 | Sitemap exists + lastmod within 90 days + covers all key pages = 1, else 0 |

**Data sources:** ai-crawler-audit-agent output, robots.txt and llms.txt fetch, page source inspection.

---

## Dimension 6: Brand Fingerprint (10 pts)

**What it measures:** Whether the brand's identity is described consistently across the web, so AI engines learn a single canonical entity rather than multiple variants.

**Sub-criteria:**

| Sub-criterion | Points | How to measure |
|---|---|---|
| Locked entity description present + consistent on owned channels (website, LinkedIn, Twitter/X, Crunchbase) | 0-3 | Same description (or core concepts) on all = 3, mostly = 2, scattered = 1, none = 0 |
| Knowledge graph presence (Wikidata + Wikipedia) | 0-3 | Both = 3, Wikidata only = 2, neither = 0 |
| Directory consistency (G2, Capterra, GetApp, Software Advice, Trustpilot) | 0-2 | All 5 with consistent description = 2, 2-4 = 1, 0-1 = 0 |
| Founder/leadership bios use the locked entity description | 0-2 | All bios = 2, some = 1, none = 0 |

**Data sources:** WebFetch of owned channels and directories, Wikidata search, Wikipedia search, manual Google searches for "[brand] founder" and "[brand] CEO".

---

## Dimension 7: Competitive Position (10 pts)

**What it measures:** How the brand stacks up against its locked competitor set across multiple visibility lenses.

**Sub-criteria:**

| Sub-criterion | Points | How to measure |
|---|---|---|
| AI Citation Share gap vs top competitor | 0-3 | We outscore top competitor by 10%+ = 3, within ±10% = 2, behind 10-25% = 1, behind 25%+ = 0 |
| DR vs competitor average | 0-2 | DR ≥ avg = 2, within 10 pts = 1, gap >10 = 0 |
| Refdomain growth rate vs competitor average (12-month) | 0-3 | Outpacing competitor avg by 25%+ = 3, matching = 2, behind = 1, declining = 0 |
| Keyword overlap with primary competitor (high overlap = direct competition for same queries) | 0-2 | Strategic overlap (same target keywords) > 50% = 2, 25-50% = 1, <25% = 0. Note: this measures whether you are competing for the right queries, not winning them. |

**Data sources:** Per-engine citation scans (Dimension 3 outputs), Ahrefs `site-explorer-domain-rating` for all competitors, Ahrefs `site-explorer-refdomains-history`, Ahrefs `site-explorer-organic-competitors`.

---

## Dimension 8: Authority Signals (10 pts)

**What it measures:** The off-site validation that AI engines weight when deciding which sources to trust.

**Sub-criteria:**

| Sub-criterion | Points | How to measure |
|---|---|---|
| Refdomain count | 0-3 | <500 = 0, 500-2K = 1, 2K-10K = 2, 10K+ = 3 |
| Refdomain growth velocity (12-month % change) | 0-3 | +50%+ = 3, +20-50% = 2, 0-20% = 1, declining = 0 |
| Citation source diversity (top 100 refdomains span how many categories: news, .edu, .gov, Reddit, G2/dir, GitHub, podcasts) | 0-2 | 6+ categories = 2, 3-5 = 1, <3 = 0 |
| Top-tier citation count (Wikipedia, .gov, top-100 trade publication, major news outlet) | 0-2 | 5+ = 2, 1-4 = 1, 0 = 0 |

**Data sources:** Ahrefs `site-explorer-refdomains-history`, `site-explorer-referring-domains`, `site-explorer-anchors`.

---

## Dimension 9: Citation Share (10 pts)

**What it measures:** Of all the AI responses for category-relevant queries, what share of citations the brand actually owns. This is the closest analog to "market share" in AI search.

**Sub-criteria:**

| Sub-criterion | Points | How to measure |
|---|---|---|
| Total citation share across all 4 engines (cited results / total cited results in tracked queries) | 0-4 | 25%+ = 4, 15-25% = 3, 10-15% = 2, 5-10% = 1, <5% = 0 |
| Cited page diversity (homepage vs deep pages) | 0-2 | Both homepage AND ≥3 deep pages cited = 2, homepage only = 1, none = 0 |
| Citation context (positive, neutral, negative) | 0-2 | Mostly positive = 2, neutral = 1, negative = 0 |
| Brand vs unbranded query citation ratio | 0-2 | Cited in unbranded category queries (not just brand queries) = 2, mixed = 1, brand-only = 0 |

**Data sources:** Per-engine citation scans (Dimension 3 outputs), manual SERP review for sentiment, query tagging in query bank.

---

## Use this rubric in three ways

### 1. Score a client at engagement start (the Blueprint deliverable)
Run all 9 dimensions, total points, assign grade, identify the lowest-scoring dimensions as the priority repair list.

### 2. Score competitors for the gap matrix
Run a partial rubric (Dimensions 1, 2, 7, 8 — the dimensions where competitor data is observable) on each locked competitor. Use the comparison to support the strategic memo.

### 3. Re-score quarterly
Same rubric, same data sources, same methodology. Compute month-over-month and quarter-over-quarter deltas. Flag any dimension with negative movement as an alert.

---

## Anti-patterns (do not do this)

- **Do not adjust the rubric mid-engagement to make a client look better.** The rubric is the contract. If a client scores poorly, that is the audit's value, not a problem.
- **Do not score Citation Share without raw evidence.** Every point in Dimension 9 must trace to a logged AI engine response. No estimating.
- **Do not collapse two dimensions into one.** They measure different things even if they correlate.
- **Do not score above 10 in any dimension.** If sub-criteria total exceeds 10, the rubric needs revision (not the score).
- **Do not skip a dimension because data is hard to get.** If you cannot measure Brand Radar SOV today, mark Dimension 3 sub-criterion as "pending" and re-score after 1-2 weeks. Do not estimate.

---

## Rubric versioning

Bump version on any sub-criterion change. Old engagements stay scored against the rubric version active at engagement start.

| Version | Date | Notes |
|---|---|---|
| v1 | 2026-04-23 | Initial authorship during Talkadot self-audit. 9 dimensions, 0-10 each, 90 total. |

---

## Implementation reference

The Talkadot 2026-04-23 audit is the first execution of this rubric. See `clients/talkadot/research/audits/2026-04-23/01_visibility_score.md` for the worked example with all 9 dimensions scored against real data.
