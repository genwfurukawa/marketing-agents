---
name: original-research-designer
description: "Use when designing original research — a survey, data study, or 'State
of X' report — engineered to become a citation magnet in AI answers. Triggers on:
'design original research', 'state of X report', 'create a data study', 'survey for
content', 'original data for AEO', 'citation-magnet research', 'benchmark report'.
Original data earns +37% citation rate; this skill designs the study, methodology,
and packaging, then feeds the statistics page type. Designs the research; does not
fabricate findings."
metadata:
  version: 1.0.0
---

# Original Research Designer

The single highest-leverage AEO asset is original data. Per the Princeton GEO study
(the same research base `aeo-checker` cites), content with specific statistics earns
a **+37% citation rate**, and named original sources earn **+40%**. When *you* are
the source of a stat, every page that cites it points back to you — including AI
answers. This skill designs research engineered to be cited: the question, the
method, and the packaging. It does **not** invent results — it produces the plan you
then execute to gather real data.

## Why Original Research Wins in AI Search

AI engines preferentially cite primary sources for factual/statistical queries
("{category} statistics", "average {metric} for {ICP}", "how many companies {do X}").
If you own a frequently-asked statistic, you become the default citation for a whole
query class — durable, compounding visibility that competitors can't simply copy.

## Before Starting

You need:
1. **The category + ICP** — from `clients/{slug}/config.yaml` / `icp-psyche.md`
2. **A citation-gap signal** — statistic-style queries where the brand is absent (from
   `aeo-engine-scan` / the query bank / `audience-question-miner-agent`). The best
   study answers a question buyers ask that *nobody currently owns with data*.
3. **A realistic data source** — what data can actually be gathered: a customer/
   audience survey, the company's own product/usage data (anonymized, aggregated),
   public dataset analysis, or an expert panel. The method must be honestly doable.

## How It Works

### Step 1 — Pick the ownable question
Choose a research question that is: frequently asked (real query demand), currently
un-owned (no strong primary source cited today), answerable with data you can get,
and tied to the brand's category authority. One sharp question beats a sprawling
survey. Frame it as the stat you want to be cited for: "X% of {ICP} {do Y}."

### Step 2 — Design the method (honest + defensible)
Specify:
- **Instrument** — survey (with the actual questions), product-data analysis (which
  metrics, what aggregation), or dataset analysis (which dataset, what computation)
- **Sample** — who, target n, how recruited; be realistic about achievable n
- **Timeframe** and **how bias is controlled** (so the finding survives scrutiny — AI
  engines and journalists favor methodologically sound sources)
- **The headline metrics** you expect to report (as hypotheses/placeholders, clearly
  marked `TBD — fill with real data`, never as invented numbers)

### Step 3 — Design for citation (packaging)
Plan the outputs so the data is maximally extractable:
- **Key findings as standalone stat bullets** — each a self-contained, quotable
  sentence with the number up front ("63% of {ICP} {finding}.")
- **A `statistics` AEO page** — feed the existing `statistics_research.md` template +
  `Dataset` + `FAQPage` schema via `schema-generator`
- **A methodology section** — named, dated, transparent (this is what earns trust and
  the citation)
- **Derivative assets** — a chart per key stat, LinkedIn posts per finding, a PR/
  outreach angle for journalists and community seeding
- **A canonical URL** that becomes *the* source for the stat

### Step 4 — Distribution-for-citation plan
Original research only compounds if it's discoverable: the on-site statistics page,
community seeding (`community-seeding`) where the stat answers live questions, links
from comparison/what-is pages, and outreach to publications that cover the category.

## Output

Write to `clients/{slug}/research/original-studies/{study-slug}/brief.md`:
1. **The ownable question** + the query class it targets
2. **Method** — instrument (with questions/metrics), sample, timeframe, bias controls
3. **Expected headline metrics** — clearly marked as placeholders to fill with real
   data
4. **Citation packaging plan** — stat-bullet format, statistics-page outline, schema,
   derivative assets
5. **Distribution-for-citation plan** — on-site + community + outreach
6. **Execution checklist** — exactly what to run to collect the real data

## Hand-offs

- Once real data is collected → `aeo-page-generator` (page_type: `statistics`) +
  `schema-generator` (`Dataset`) to publish the page
- Each finding → `linkedin-post-writer`, `community-seeding`, newsletter
- Track whether the stat starts winning citations → `aeo-engine-scan`

## Quality Gate

- [ ] One sharp, ownable, currently-un-owned research question
- [ ] Method is honestly executable with a realistic sample (no fantasy n)
- [ ] Every reported number is a real-data placeholder marked TBD — zero fabricated stats
- [ ] Findings packaged as standalone, number-first quotable bullets
- [ ] Statistics page + Dataset schema planned
- [ ] Distribution-for-citation plan included (a study nobody finds earns nothing)
