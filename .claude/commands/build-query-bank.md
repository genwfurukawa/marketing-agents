---
description: Build a structured query bank for AI visibility auditing - chains ICP analysis, audience mining, and query template generation into 20-30 tagged queries ready for aeo_audit.py batch input
argument-hint: --company "Company Name" --domain company.com --competitors "comp1,comp2,comp3" --problems "problem1,problem2,problem3" [--client client-slug] [--category "category name"] [--icp "ICP description"]
allowed-tools: Task, Read, Write, Glob, Grep, Bash, WebSearch, WebFetch
---

# Build Query Bank

> **Engine note (2026-07-24):** the query bank feeds `scripts/aeo_audit/aeo_audit.py --engines perplexity,chatgpt,claude,gemini` and the `aeo-engine-scan` skill. (The 2026-05 Ahrefs Brand Radar path is retired; historical pulls live in `research/ahrefs/`.)

You build a structured query bank of 20-30 queries for AI visibility auditing. The output is consumed by Ahrefs Brand Radar (primary) or the legacy `aeo_audit.py batch --input query_bank.csv` (legacy).

This command chains three existing tools in sequence:
1. `icp-definition-agent` - validates the buyer profile and surfaces buying triggers
2. `audience-question-miner-agent` - finds real queries buyers are asking right now
3. `query_templates.py` - generates structured audit queries from templates

You synthesize their outputs into a single, tagged query bank. You never replace these tools - you orchestrate them.

## Inputs

### Required
- `--company`: Company display name (e.g., "Avoma")
- `--domain`: Client's primary domain (e.g., "avoma.com")
- `--competitors`: Comma-separated, top 3 competitor names or domains (e.g., "Gong,Chorus,Fireflies")
- `--problems`: Comma-separated, top 3 problems the company solves (e.g., "sales calls not recorded,meeting insights lost,coaching at scale")

### Optional
- `--client`: Client workspace slug. Defaults to lowercase company name.
- `--category`: Product category (e.g., "conversation intelligence"). If not provided, infer from company description.
- `--icp`: ICP description override. If not provided, pull from clients/{client}/config.yaml or client Brand Brain.

### Config Loading
Before any work, load:
1. `clients/{client}/config.yaml` from ops repo root
2. `lessons.md` from ops repo root
3. Client Brand Brain at `clients/{client_slug}/config/brand-brain.md` (if exists)

## Execution Flow

### Phase 1: ICP Validation (via icp-definition-agent)

Run `icp-definition-agent` via Task tool with these inputs:
- Company name and domain
- Competitor names
- Problems solved
- Any existing ICP data from Brand Brain or clients/{client}/config.yaml

Extract from agent output:
- **Buying triggers** with timing signals (these become query seeds)
- **Persona titles** (these shape "for {role}" query variants)
- **Common objections** (these become trust/evaluation queries)
- **Category name and definition** (this sets the category context for all queries)
- **Competitive alternatives** (names to use in comparison queries)

If a client Brand Brain already exists with validated ICP data, skip the full agent run. Read the Brand Brain and extract the fields above directly.

### Phase 2: Audience Question Mining (via audience-question-miner-agent)

Run `audience-question-miner-agent` via Task tool with:
- The category name from Phase 1
- The 3 problems from input
- ICP role titles from Phase 1

Extract from agent output:
- **Top 10 highest-engagement questions** (these become problem and trend queries)
- **AEO page opportunities** (these inform which query categories need more coverage)
- **Exact phrasing from Reddit/Quora** (real buyer language beats templated language)

### Phase 3: Query Generation and Synthesis

Now build the query bank by combining three sources:

**Source A - Template queries** from `scripts/aeo_audit/query_templates.py`:
Run `generate_audit_queries()` mentally using the inputs. This produces the baseline set across brand, awareness, consideration, comparison, and problem intents. Reference the exact function signature:

```python
generate_audit_queries(
    company="{company}",
    domain="{domain}",
    category="{category}",
    competitors=["{comp1}", "{comp2}", "{comp3}"],
    icp="{icp_description}",
)
```

This generates ~25-30 template queries. You will select, deduplicate, and enrich from these.

**Source B - Real buyer questions** from Phase 2:
Take the top 5-8 audience questions and convert them into audit queries. Keep the original phrasing - real language outperforms templated language in AI search testing.

**Source C - Buying trigger queries** from Phase 1:
Convert each buying trigger into 1-2 queries that a buyer in that trigger moment would actually search. Example: trigger "Board asking about AI search strategy" becomes query "how to build an AI search strategy for B2B SaaS".

### Phase 4: Tag, Score, and Deduplicate

Apply these tags to every query:

**Query Category** (7 types):
| Category | Description | Example |
|----------|-------------|---------|
| `brand` | Queries about the company itself | "What is {company}?", "{company} reviews" |
| `problem` | How-to and pain-point queries | "how to solve {problem}", "why is {challenge} hard" |
| `comparison` | Head-to-head and alternatives | "{company} vs {competitor}", "{competitor} alternatives" |
| `category` | Best-of and listicle queries | "best {category} tools", "top {category} software" |
| `trust` | Evaluation, pricing, proof queries | "Is {company} worth it?", "{company} case studies", "{category} ROI" |
| `technical` | Implementation and integration | "how to implement {category}", "{company} integrations" |
| `trend` | Industry direction and future | "{category} trends 2026", "future of {category}" |

**Target Platform:**
| Platform | When to assign |
|----------|---------------|
| `Perplexity` | All queries (baseline - this is what aeo_audit.py tests against) |
| `ChatGPT` | Conversational queries, "what should I use" phrasing |
| `Google AIO` | Queries with commercial intent, "best X for Y" phrasing |

Most queries target all 3 platforms. Assign the primary platform based on where that query style is most commonly asked.

**Buyer Intent Level:**
| Intent | Description | Query signals |
|--------|-------------|---------------|
| `awareness` | Buyer is learning about the problem/category | "what is", "why do companies need", "how does X work" |
| `consideration` | Buyer is evaluating options | "best tools", "top software", "comparison", "how to choose" |
| `decision` | Buyer is making a final choice | "vs", "alternatives", "pricing", "reviews", "worth it", "case studies" |

**Priority Tier:**
| Tier | Criteria | Count target |
|------|----------|-------------|
| `1` | High commercial intent + high competitor presence + direct revenue impact. These are the queries where losing visibility costs deals. | 8-10 queries |
| `2` | Medium intent + category authority builders. Winning these establishes expertise but doesn't directly close deals. | 8-10 queries |
| `3` | Awareness and trend queries. Important for long-term visibility but lower immediate pipeline impact. | 5-8 queries |

**Deduplication rules:**
- If two queries test the same intent with near-identical phrasing, keep the one with more natural language (prefer audience-mined over templated)
- Keep both "{company} vs {competitor}" and "{competitor} vs {company}" - AI platforms return different results for each direction
- Keep both "best {category} tools" and "best {category} software" - these surface different source lists

**Target: 20-30 final queries.** If you have more than 30 after synthesis, cut Tier 3 queries first. If fewer than 20, add more Tier 2 category queries.

## Output Format

### Primary Output: Query Bank Markdown

```markdown
---
type: query-bank
company: {company}
domain: {domain}
competitors: [{competitor_list}]
category: {category}
queries_count: {count}
created: {ISO-8601}
sources: [icp-definition-agent, audience-question-miner-agent, query_templates.py]
---

# Query Bank: {company}

**Category:** {category}
**Domain:** {domain}
**Competitors:** {competitor_1}, {competitor_2}, {competitor_3}
**Date:** {YYYY-MM-DD}
**Queries:** {count}

## Query Bank Summary

| Category | Count | Tier 1 | Tier 2 | Tier 3 |
|----------|------:|-------:|-------:|-------:|
| Brand | {n} | {n} | {n} | {n} |
| Problem | {n} | {n} | {n} | {n} |
| Comparison | {n} | {n} | {n} | {n} |
| Category | {n} | {n} | {n} | {n} |
| Trust | {n} | {n} | {n} | {n} |
| Technical | {n} | {n} | {n} | {n} |
| Trend | {n} | {n} | {n} | {n} |
| **Total** | **{N}** | **{n}** | **{n}** | **{n}** |

## Intent Distribution

| Intent | Count | % |
|--------|------:|--:|
| Awareness | {n} | {%} |
| Consideration | {n} | {%} |
| Decision | {n} | {%} |

---

## Full Query Bank

### Tier 1 - High Priority (Revenue Impact)

| # | Query | Category | Platform | Intent | Source |
|---|-------|----------|----------|--------|--------|
| 1 | {query} | {category} | {platform} | {intent} | {template/audience/trigger} |
| 2 | {query} | {category} | {platform} | {intent} | {source} |

### Tier 2 - Medium Priority (Authority Building)

| # | Query | Category | Platform | Intent | Source |
|---|-------|----------|----------|--------|--------|
| 1 | {query} | {category} | {platform} | {intent} | {source} |

### Tier 3 - Lower Priority (Awareness)

| # | Query | Category | Platform | Intent | Source |
|---|-------|----------|----------|--------|--------|
| 1 | {query} | {category} | {platform} | {intent} | {source} |

---

## Query Sources

### From ICP Buying Triggers
{List each buying trigger and the queries it generated}

### From Audience Questions (Real Buyer Language)
{List each mined question and the query it became, with source URL/subreddit}

### From Query Templates
{List which template categories were used}
```

### Secondary Output: CSV for aeo_audit.py batch

Generate a CSV file that plugs directly into `python aeo_audit.py batch --input query_bank.csv`:

```csv
query,category,client_domain
{query_1},{category_tag},{domain}
{query_2},{category_tag},{domain}
```

The `category` column maps to the `intent` field in aeo_audit.py's analyzer. Use these values to match the existing codebase:
- `brand` -> `brand`
- `problem` -> `problem`
- `comparison` -> `comparison`
- `category` -> `consideration`
- `trust` -> `brand` (closest match in existing taxonomy)
- `technical` -> `problem` (closest match)
- `trend` -> `awareness`

### Tertiary Output: JSON for programmatic use

```json
{
  "company": "{company}",
  "domain": "{domain}",
  "category": "{category}",
  "competitors": ["{comp1}", "{comp2}", "{comp3}"],
  "created": "{ISO-8601}",
  "query_count": {N},
  "queries": [
    {
      "query": "{query text}",
      "category": "{brand|problem|comparison|category|trust|technical|trend}",
      "platform": "{Perplexity|ChatGPT|Google AIO}",
      "intent": "{awareness|consideration|decision}",
      "tier": {1|2|3},
      "source": "{template|audience|trigger}",
      "source_detail": "{specific template name, Reddit URL, or trigger description}"
    }
  ]
}
```

## Output Routing

Write all outputs to the client workspace:

```
clients/{client_slug}/research/audits/
  {YYYY-MM-DD}_query_bank.md          (full tagged bank)
  {YYYY-MM-DD}_query_bank.csv         (aeo_audit.py batch input)
  {YYYY-MM-DD}_query_bank.json        (programmatic use)
```

For a standalone client repo (`~/clients/{slug}/`), write to the repo's `research/audits/` directory.

## Presentation Checkpoint

After generating the query bank, present this summary:

```
Query bank built for {company}:

Total queries: {count}
  Tier 1 (revenue): {n}
  Tier 2 (authority): {n}
  Tier 3 (awareness): {n}

Category breakdown: {brand: n, problem: n, comparison: n, category: n, trust: n, technical: n, trend: n}

Sources used:
  Template queries: {n}
  Audience-mined: {n}
  Buying triggers: {n}

Files written:
  {path_to_markdown}
  {path_to_csv}
  {path_to_json}

Next step: Run the audit with:
  python scripts/aeo_audit/aeo_audit.py batch --input {path_to_csv} --domain {domain} --company "{company}" --client {client_slug}
```

Wait for user approval before proceeding to audit execution.

## Rules

1. **20-30 queries, no more, no less.** Under 20 misses coverage. Over 30 wastes API credits and dilutes scoring. Cut Tier 3 first if trimming.
2. **Real language wins.** When an audience-mined question and a template query test the same intent, keep the audience version. Real buyer phrasing surfaces different (often better) results in AI search.
3. **Every query must be tagged.** No query enters the bank without all 4 tags: category, platform, intent, tier. Untagged queries break downstream analysis.
4. **CSV must be aeo_audit.py-compatible.** The CSV uses the column names `query`, `category`, `client_domain` - exactly matching the `run_batch()` function in `aeo_audit.py` (line 225). The `category` values must map to the intent taxonomy the analyzer expects.
5. **Don't invent queries from nothing.** Every query traces to one of three sources: template function, audience mining, or ICP buying trigger. If you can't cite the source, cut the query.
6. **Comparison queries go both directions.** Always include both "{company} vs {competitor}" AND "{competitor} vs {company}". AI platforms treat these as different queries with different results.
7. **Show the next step.** Always end with the exact `aeo_audit.py batch` command the user should run. The query bank is not the deliverable - the audit is. This command builds the input.
