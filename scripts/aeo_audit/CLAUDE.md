# Perplexity AEO Retrieval Audit Tool

## What This Is
A Python CLI tool that uses Perplexity's Search API to run programmatic AI visibility audits for B2B SaaS clients. Instead of manually prompting LLMs and eyeballing results, this queries Perplexity's retrieval index at scale — the same index serving 200M+ daily queries — and maps which domains, URLs, and content formats are getting surfaced for target keyword clusters.

## Why It Matters
This is the retrieval layer underneath AI-generated answers. When someone asks Perplexity or any LLM-with-search "what's the best [category] tool", these are the ranked sources that get fed into the model. Seeing this data programmatically at scale = real competitive intelligence for AEO.

## Setup
```bash
pip install perplexityai --break-system-packages
export PERPLEXITY_API_KEY="your_key_here"
```

## Usage

### 1. Single Company Audit
```bash
python aeo_audit.py audit --company "Avoma" --domain "avoma.com" --category "conversation intelligence" --competitors "gong.io,chorus.ai,fireflies.ai"
```

### 2. Batch Audit from CSV
```bash
python aeo_audit.py batch --input queries.csv --output results/
```

### 3. Query Cluster Analysis
```bash
python aeo_audit.py cluster --queries "best conversation intelligence tools,AI meeting notes software,sales call recording platform,how to analyze sales calls with AI" --track-domain "avoma.com"
```

## CSV Input Format
```
query,category,client_domain
best conversation intelligence tools,category,avoma.com
AI meeting notes software,category,avoma.com
Avoma vs Gong,comparison,avoma.com
```

## Outputs
- `audit-report-{company}.md` — Full markdown audit report
- `domain-visibility-{company}.csv` — Domain frequency/ranking data
- `raw-results-{company}.json` — Complete API response data for further analysis

## Architecture
- `aeo_audit.py` — Main CLI entry point with 3 commands (audit, batch, cluster)
- `perplexity_client.py` — Async Perplexity API wrapper with retry logic and rate limiting
- `analyzer.py` — Domain extraction, ranking analysis, visibility scoring (legacy)
- `metrics_calculator.py` — Answer-text + citation-based metrics (primary scoring)
- `report_generator.py` — Markdown and CSV report generation
- `query_templates.py` — Pre-built AEO query templates by audit type

## Metrics (metrics_calculator.py)

Primary output. Pulls from `response.choices[0].message.content` (answer text) and `response.citations` (URL array).

**Per-query metrics (PerQueryMetrics):**
- Brand Presence: featured/cited/mentioned/absent + legacy 0-3 score
- Citation Analysis: client URLs, positions in citation array, competitor citations, all cited domains
- Prominence: first char position, position %, first-cited, first-mentioned
- Source Control: own-domain citations vs third-party mentions
- Sentiment: positive/neutral/negative + 10-word characterization (optional, via Claude API)

**Batch metrics (BatchMetrics):**
- answer_rate: % of queries where brand is not absent
- share_of_voice: per-brand mention count / total mentions across all queries
- avg_prominence: mean position % in answer text (lower = better)
- source_control_rate: own-domain citations / total mentions
- sentiment_distribution: {positive: n, neutral: n, negative: n}
- presence_counts: {featured: n, cited: n, mentioned: n, absent: n}

**Output:** `metrics-{company}.json` alongside existing reports.

**Legacy 0-3 scoring** is derived from presence_type: absent=0, mentioned=1, cited=2, featured=3.

## Key Design Decisions
- Uses async for concurrent queries (3-5 at a time with rate limiting)
- Extracts domains from result URLs for frequency analysis
- Tracks position (rank) not just presence — position 1 vs position 8 matters
- Multi-query batching (up to 5 per request) to minimize API calls and cost
- All results cached locally to avoid re-querying during report generation
- Answer text and citations captured from every API response for metrics_calculator
- Sentiment analysis is opt-in (`--sentiment` flag) to control Claude API costs

## Cost
$5 per 1,000 Search API requests. A typical 50-query audit costs ~$0.25.
Sentiment analysis adds ~$0.01/query via Claude Haiku API (opt-in with `--sentiment`).
