# Perplexity AEO Retrieval Audit Tool

## What This Actually Gets You

This tool queries Perplexity's Search API — the retrieval layer behind 200M+ daily AI search queries — and maps which domains, URLs, and content formats are getting surfaced and ranked for any set of target queries.

**This is not prompting an LLM and reading the output.** This is seeing the actual retrieval index: the ranked sources that get fed INTO LLM answers. That's the difference.

## Setup

```bash
# 1. Install
pip install perplexityai

# 2. Set your API key (get it at perplexity.ai/settings > API tab)
export PERPLEXITY_API_KEY="pplx-..."

# 3. Run your first audit
python aeo_audit.py audit \
  --company "Avoma" \
  --domain "avoma.com" \
  --category "conversation intelligence" \
  --competitors "gong.io,chorus.ai,fireflies.ai" \
  --output ./results
```

**Cost:** ~$0.25 per full audit (50 queries). $5 per 1,000 API requests, no token charges.

## Three Commands

### 1. `audit` — Full Company Visibility Audit
Generates 30-50 queries across intent stages (awareness, consideration, comparison, brand), runs them all, and produces a scored report with competitive analysis.

```bash
python aeo_audit.py audit \
  --company "Arrows" \
  --domain "arrows.to" \
  --category "customer onboarding software" \
  --competitors "rocketlane.com,clientsuccess.com,gainsight.com" \
  --icp "B2B SaaS" \
  --output ./results
```

**Outputs:**
- `audit-report-arrows.md` — Full markdown report with visibility grade, competitive comparison, gaps, and recommendations
- `domain-visibility-arrows.csv` — Every domain that appeared, how often, and at what position
- `raw-results-arrows.json` — Complete API data for further analysis

### 2. `cluster` — Query Cluster Analysis
Quick and dirty: throw in a set of queries, see which domains dominate.

```bash
python aeo_audit.py cluster \
  --queries "best AEO tools,AI search optimization,how to optimize for ChatGPT,answer engine optimization guide" \
  --track-domain "acme.com"
```

### 3. `batch` — CSV Batch Mode
Load queries from a CSV for maximum control.

```bash
python aeo_audit.py batch \
  --input sample-queries.csv \
  --domain "avoma.com" \
  --company "Avoma" \
  --output ./results
```

## What You Can Build With This

### For Client Audits (the $5K+ deliverable)
Run the `audit` command per client. You get a data-backed visibility report showing exactly where they appear (and don't appear) in AI search retrieval, which competitors are winning, and which queries are the highest-priority content opportunities. Pair this with the existing prospect-audit skill for the narrative + Loom, and now you have hard retrieval data backing up your recommendations.

### For Ongoing Monitoring (the retainer upsell)
Run the same query set monthly. Track visibility rate and position changes over time. "Last month you appeared in 15% of retrieval results for your category. After 60 days of our content system, you're at 42%." That's a retention story.

### For Content Prioritization
The gaps list tells you exactly which queries a client needs to create content for — ranked by competitive urgency (queries where competitors appear but client doesn't). No more guessing what to write about.

### For AEO Methodology Validation
Run audits before and after AEO content optimization. Measure whether restructured content actually improves retrieval visibility. This is the data layer that proves the methodology works.

### For Lead Gen / Cold Outreach
Run quick audits on prospects BEFORE outreach. "Hey [Founder], I ran your company through our AI retrieval analysis — you appear in 0 out of 30 buyer queries for your category. Here's the data." That's a gift that opens doors.

### For the AI Buyer Journey Simulator (your lead magnet tool)
This is the engine underneath it. The Simulator takes a prospect's domain + category, runs queries across the buyer journey stages, and shows where they appear vs competitors. This tool does the backend work.

## Claude Code Integration

Drop this entire folder into your client ops repo. The CLAUDE.md file means Claude Code can:
- Run audits on command ("run an AEO retrieval audit for Arrows.to")
- Generate reports automatically
- Extend the query templates per industry/vertical
- Build on top of the raw JSON output

## Architecture

```
aeo_audit.py          ← CLI entry point (audit, cluster, batch)
perplexity_client.py  ← Async API wrapper (retry, rate limiting, batching)
query_templates.py    ← AEO query generation by intent stage
analyzer.py           ← Domain extraction, visibility scoring, gap analysis
report_generator.py   ← Markdown reports, CSV exports, JSON dumps
sample-queries.csv    ← Example batch input
CLAUDE.md             ← Claude Code instructions
```
