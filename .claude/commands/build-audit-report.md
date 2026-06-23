---
description: Chain aeo_audit.py, competitor-analysis-agent, and ai-crawler-audit-agent outputs into a unified client-facing audit package with scorecard, gap analysis, and executive summary
argument-hint: --client client-slug --company "Company Name" --domain company.com --competitors "comp1.com,comp2.com" [--audit-dir path/to/audit/output] [--deal-size 50000]
allowed-tools: Task, Read, Write, Glob, Grep, Bash, WebSearch, WebFetch
---

# Build Audit Report

> **Migration notice (2026-05-11):** This command originally synthesized output from `scripts/aeo_audit/aeo_audit.py` (Perplexity-only). Visibility tracking is moving to **Ahrefs Brand Radar** via the `ahrefs-pull` skill. New runs should consume Ahrefs JSON in `research/ahrefs/{YYYY-MM}/`. The legacy Perplexity script remains in `scripts/aeo_audit/` for ad-hoc use.

You produce a unified, client-facing audit package from raw audit data. You wrap existing tools - you never replace them. Your job is synthesis and presentation.

## What This Command Produces

Three deliverables, written to the client workspace:

1. **Visibility Scorecard** - Table comparing client vs competitors across 7 query categories and 3 AI platforms
2. **Gap Analysis Document** - Top 5 visibility gaps, each mapped to a specific AEO page type template with the actual AI answer shown
3. **Executive Summary** - 3 paragraphs: current state, competitive gap, recommended next steps with pipeline estimate

## Prerequisites

Before running this command, the following must already exist:

1. **AEO audit output** from `scripts/aeo_audit/aeo_audit.py` - Look for:
   - `audit-report-{company}.md` (markdown report)
   - `domain-visibility-{company}.csv` (domain ranking data)
   - `raw-results-{company}.json` (full API response data)
2. **Client workspace** at `../clients/{client_slug}/`
3. **clients/{client}/config.yaml** loaded from ops repo root

If audit data doesn't exist yet, tell the user to run the audit first:
```
python scripts/aeo_audit/aeo_audit.py audit --company "{company}" --domain "{domain}" --competitors "{competitors}"
```

## Input Resolution

Parse inputs in this priority order:

### Required
- `--company`: Company display name (e.g., "Avoma")
- `--domain`: Client's primary domain (e.g., "avoma.com")
- `--competitors`: Comma-separated competitor domains (e.g., "gong.io,chorus.ai")

### Optional
- `--client`: Client workspace slug. Defaults to lowercase company name.
- `--audit-dir`: Path to existing audit output. Defaults to `scripts/aeo_audit/results/`
- `--deal-size`: Client's stated average deal size in USD. Used for pipeline estimate in executive summary. Defaults to $50,000.

### Config Loading
Before any work, load:
1. `clients/{client}/config.yaml` from ops repo root
2. `lessons.md` from ops repo root
3. Client Brand Brain at `../clients/{client_slug}/03_insight_layer/brand_brain.md` (if exists)

## Execution Flow

### Phase 1: Collect Raw Data (read-only)

Read all existing audit artifacts. Do NOT re-run audits.

**Step 1.1** - Read AEO audit output:
- Parse `raw-results-{company}.json` for query-by-query results
- Parse `domain-visibility-{company}.csv` for domain rankings
- Parse `audit-report-{company}.md` for the existing analysis
- Extract: visibility_rate, avg_position, visibility_score, gaps, intent_coverage, competitor_stats

**Step 1.2** - Run competitor-analysis-agent via Task tool:
- Input: Company name, competitor list, client domain
- Depth: Standard
- Extract: positioning gap map, content gaps, messaging comparison

**Step 1.3** - Run ai-crawler-audit-agent via Task tool:
- Input: Client website URL
- Extract: crawler access score (0-100), structured data findings, priority fix list

Run Steps 1.2 and 1.3 in PARALLEL.

### Phase 2: Build Visibility Scorecard

Construct a comparison table using data from Phase 1.

**7 Query Categories** (map from AEO audit intent_coverage):
1. Brand queries ("what is {company}", "{company} reviews")
2. Category queries ("best {category} tools", "top {category} software")
3. Problem queries ("how to solve {pain_point}")
4. Comparison queries ("{company} vs {competitor}")
5. Alternative queries ("{competitor} alternatives")
6. Integration queries ("{company} integrations with {tool}")
7. Industry queries ("{category} for {industry}")

**3 Platforms** (from AEO audit raw results, tag by source):
- Perplexity (primary - from aeo_audit.py API data)
- ChatGPT (if available from prospect-scorecard or manual queries)
- Google AI Overviews (if available)

Note: If only Perplexity data exists, label the scorecard as "Perplexity Retrieval Index" and note that ChatGPT and Google AI Overviews require separate audit runs.

**Scorecard Table Format:**

```markdown
# AI Search Visibility Scorecard

**Company:** {company}
**Date:** {YYYY-MM-DD}
**Queries Analyzed:** {count}
**Data Source:** Perplexity Search API

## Overall Scores

| Company | Visibility Score | Grade | Citation Rate | Avg Position |
|---------|-----------------|-------|---------------|--------------|
| {client} | {score}/100 | {A-F} | {X}% | {X.X} |
| {competitor_1} | {score}/100 | {A-F} | {X}% | {X.X} |
| {competitor_2} | {score}/100 | {A-F} | {X}% | {X.X} |
| {competitor_3} | {score}/100 | {A-F} | {X}% | {X.X} |

## Score by Query Category

| Category | {client} | {comp_1} | {comp_2} | {comp_3} | Client Gap |
|----------|----------|----------|----------|----------|------------|
| Brand | {0-3} | {0-3} | {0-3} | {0-3} | {+/- vs leader} |
| Category | {0-3} | {0-3} | {0-3} | {0-3} | {+/- vs leader} |
| Problem | {0-3} | {0-3} | {0-3} | {0-3} | {+/- vs leader} |
| Comparison | {0-3} | {0-3} | {0-3} | {0-3} | {+/- vs leader} |
| Alternative | {0-3} | {0-3} | {0-3} | {0-3} | {+/- vs leader} |
| Integration | {0-3} | {0-3} | {0-3} | {0-3} | {+/- vs leader} |
| Industry | {0-3} | {0-3} | {0-3} | {0-3} | {+/- vs leader} |

## Competitive Displacement Score

For each query where a competitor appears and the client doesn't, calculate displacement:

| Query | Client Present? | Displaced By | Competitor Position | Revenue at Risk |
|-------|----------------|--------------|--------------------:|----------------:|
| {query} | No | {competitor} | #{position} | ${deal_size * displacement_factor} |

**Displacement Factor:** Position 1-3 = 0.15x deal size, Position 4-7 = 0.08x, Position 8+ = 0.03x

## Technical Readiness

| Dimension | Score | Status |
|-----------|------:|--------|
| AI Crawler Access | {X}/30 | {status} |
| Sitemap Health | {X}/10 | {status} |
| Structured Data | {X}/30 | {status} |
| Page Structure | {X}/30 | {status} |
| **Infrastructure Total** | **{X}/100** | **{rating}** |
```

**Scoring methodology for category scores (0-3 scale):**
- 3 = Client appears in top 3 results for majority of queries in this category
- 2 = Client appears in top 10 for some queries
- 1 = Client mentioned but not in primary results
- 0 = Client absent from all queries in this category

### Phase 3: Build Gap Analysis Document

Take the top 5 visibility gaps from the AEO audit (queries where competitors appear but client is absent, sorted by competitor count descending).

For each gap, produce:

```markdown
# Visibility Gap Analysis

## Gap #{n}: {query}

**Severity:** {Critical / High / Medium}
**Query Intent:** {intent_stage}
**Competitors Present:** {list of competitor domains appearing}
**Client Status:** Not cited in any AI response

### What AI Currently Answers

> {Paste the actual AI-generated answer from raw-results JSON, or summarize the top 3 results. Show what the buyer sees when they search this query.}

**Sources Cited:**
1. {domain_1} - Position 1 - "{snippet}"
2. {domain_2} - Position 2 - "{snippet}"
3. {domain_3} - Position 3 - "{snippet}"

### Recommended Content Type

**Template:** `templates/aeo_page_types/{recommended_template}.md`
**Page Type:** {What Is / Best Tools / Alternatives / Comparison / Integration / Statistics / Glossary}

**Why this page type:** {1-2 sentences connecting the query intent to the template's target pattern}

### Content Brief (Starter)

- **Target H1:** {suggested title}
- **Target query cluster:** {3-5 related queries this page would also capture}
- **Key entities to include:** {companies, products, concepts that must appear}
- **Differentiation angle:** {what the client can say that competitors can't - pull from competitor-analysis-agent positioning gap map}
- **Schema markup:** {recommended JSON-LD type from aeo-page-brief-agent patterns}
```

**Gap-to-template mapping rules:**
- "what is" / definition queries -> `what_is_definition.md`
- "best tools" / "top software" -> `best_tools_list.md`
- "{product} alternatives" -> `alternatives.md`
- "{product A} vs {product B}" -> `product_comparison.md`
- "integrates with" / "{product} + {product}" -> `integration.md`
- "{topic} statistics" / "{topic} data" -> `statistics_research.md`
- Term-specific / glossary queries -> `glossary.md`
- Problem/solution queries -> `what_is_definition.md` (closest match - note that problem-solution template is not yet built)
- Category/buyer guide queries -> `best_tools_list.md` (closest match)
- ROI/business case queries -> `statistics_research.md` (closest match)

### Phase 4: Build Executive Summary

Write exactly 3 paragraphs. No headers inside the summary. Direct, specific, written for a CEO who will read this in 2 minutes.

```markdown
# Executive Summary: {company} AI Search Visibility

**Prepared for:** {company} leadership
**Date:** {YYYY-MM-DD}
**Prepared by:** {brand}

{Paragraph 1 - Current State}
{Company} currently scores {score}/100 on AI search visibility across {X} queries tested against {platform}. Your brand appears in {visibility_rate}% of buyer-intent queries in your category, with an average citation position of {avg_position}. {X} of {total} queries return results that include at least one competitor but not {company}. Your technical infrastructure scores {crawler_score}/100 for AI crawler accessibility - {interpretation of what that means practically}.

{Paragraph 2 - Competitive Gap}
{Top competitor} leads your category with a visibility score of {score}/100, appearing in {rate}% of the queries where you are absent. The highest-impact gaps are in {category_1} and {category_2} queries - the exact searches your buyers run before building a vendor shortlist. {Specific example: "When a buyer searches '{example_query}', {competitor} appears at position {X} while {company} is not cited."} This pattern repeats across {X} of the {Y} queries we tested. Each invisible query is a conversation you're not part of.

{Paragraph 3 - Recommended Next Steps + Pipeline Estimate}
Closing these {top_gap_count} gaps requires {X} new AEO-structured pages targeting the query categories where competitors currently displace you. Based on your stated deal size of ${deal_size} and the {displacement_count} queries where competitors appear instead of you, the estimated pipeline exposure is ${pipeline_estimate} per quarter. We recommend starting with {gap_1_content_type} and {gap_2_content_type} pages - these two content types address {X}% of your visibility gaps. Expected timeline to measurable improvement: 60-90 days from publication, based on AI search reindexing cycles.
```

**Pipeline estimate formula:**
```
quarterly_pipeline = displacement_count * deal_size * 0.05 * 3
```
Where 0.05 = conservative 5% conversion rate from AI search impression to pipeline, and 3 = quarterly multiplier.

Always label this as "directional estimate" - never present as a guarantee.

## Output Routing

Write all 3 deliverables to the client workspace:

```
../clients/{client_slug}/04_content_engine/audits/
  {YYYY-MM-DD}_visibility_scorecard.md
  {YYYY-MM-DD}_gap_analysis.md
  {YYYY-MM-DD}_executive_summary.md
```

Also generate a combined single-file version for easy sharing:

```
../clients/{client_slug}/04_content_engine/audits/
  {YYYY-MM-DD}_full_audit_report.md
```

The combined file concatenates all 3 deliverables with page breaks (`---`) between sections, plus a table of contents at the top.

### Metadata Frontmatter

Every output file starts with:

```yaml
---
type: audit-report
component: scorecard | gap-analysis | executive-summary | full-report
company: {company}
domain: {domain}
competitors: [{competitor_list}]
queries_analyzed: {count}
visibility_score: {score}
grade: {A-F}
created: {ISO-8601}
audit_source: scripts/aeo_audit/
---
```

## Quality Checks

Before writing final output, verify:

1. [ ] All competitor scores are calculated from real data, not estimated
2. [ ] Gap analysis references actual AI answers from raw-results JSON
3. [ ] Each gap maps to a real template in `templates/aeo_page_types/`
4. [ ] Executive summary contains specific numbers, not vague claims
5. [ ] Pipeline estimate is labeled as "directional" and shows the formula
6. [ ] No banned phrases from clients/{client}/config.yaml voice.never_say
7. [ ] No AI slop verbs or adjectives from output style rules
8. [ ] Technical infrastructure score comes from ai-crawler-audit-agent, not invented
9. [ ] Displacement scores use the defined formula, not arbitrary numbers
10. [ ] Combined report has working table of contents with anchor links

## Presentation Checkpoint

After generating all deliverables, present a summary to the user:

```
Audit report generated for {company}:

Visibility Score: {score}/100 ({grade})
Top Competitor: {name} at {score}/100
Gaps Found: {count} ({critical_count} critical)
Pipeline Exposure: ${estimate}/quarter (directional)
Pages Recommended: {count} across {template_count} content types

Files written:
- {path_to_scorecard}
- {path_to_gap_analysis}
- {path_to_executive_summary}
- {path_to_combined}

Review the scorecard first. Approve before sending to client.
```

Wait for user approval before marking complete. Never auto-send to client.

## Rules

1. **Wrap, don't replace.** This command reads output from aeo_audit.py and agents. It never re-runs the audit itself.
2. **Real data only.** Every number in the scorecard must trace back to actual query results. If data is missing for a platform or category, show "N/A" - never estimate.
3. **One pipeline formula.** Use the displacement formula defined above. Don't invent alternative calculations.
4. **Template mapping must be exact.** Only map gaps to templates that exist in `templates/aeo_page_types/`. If no template fits, say "No existing template - requires new page type."
5. **Voice rules apply.** The executive summary is client-facing content. Run it against clients/{client}/config.yaml voice.never_say and lessons.md before finalizing.
6. **Show the actual AI answer.** The gap analysis is powerful because it shows the CEO what buyers see today. Pull real snippets from the raw JSON - don't paraphrase.
