# SEO API Setup Guide

Two external APIs power the SEO research infrastructure: **Keywords Everywhere** (keyword data) and **DataForSEO** (SERP analysis, backlinks, technical audits).

## 1. Keywords Everywhere

**What it does:** Keyword volume, CPC, competition data, related keywords, People Also Search For (PASF), domain keyword rankings.

**Signup:**
1. Go to https://keywordseverywhere.com/api
2. Create an account and purchase credits (pay-as-you-go)
3. Copy your API key from the dashboard

**Cost:** ~$10 for 100,000 credits. Most operations cost 1-2 credits per keyword.

**Add to `.env`:**
```
KE_API_KEY=your_api_key_here
```

## 2. DataForSEO

**What it does:** Live SERP results, backlink profiles, domain intersection (link gap analysis), OnPage crawling (technical SEO), Lighthouse audits.

**Signup:**
1. Go to https://dataforseo.com
2. Create an account (free trial available with $1 credit)
3. Note your login email and password - these ARE the API credentials

**Cost:** Pay-per-task. SERP queries ~$0.002/keyword, backlinks ~$0.02/domain, crawling ~$0.01/page.

**Add to `.env`:**
```
DATAFORSEO_LOGIN=your_email@example.com
DATAFORSEO_PASSWORD=your_password_here
```

## 3. Budget Controls

The cost tracker enforces a per-session spending limit. Set it based on your comfort level.

**Add to `.env`:**
```
SEO_BUDGET_LIMIT_USD=50.00
SEO_CACHE_TTL_HOURS=72
```

| Variable | Default | What it controls |
|----------|---------|-----------------|
| `SEO_BUDGET_LIMIT_USD` | 50.00 | Maximum USD spend per session. Raises `BudgetExceededError` before exceeding. |
| `SEO_CACHE_TTL_HOURS` | 72 | How long to cache API responses. SEO data changes slowly - 72 hours is safe. |

## 4. Full `.env` Block

```
# SEO Research APIs
KE_API_KEY=your_keywords_everywhere_api_key
DATAFORSEO_LOGIN=your_dataforseo_email
DATAFORSEO_PASSWORD=your_dataforseo_password
SEO_BUDGET_LIMIT_USD=50.00
SEO_CACHE_TTL_HOURS=72
```

## 5. Verify Setup

```bash
# Test imports (no API calls)
python3 -c "from scripts.seo import KeywordsEverywhereClient, DataForSEOClient, CostTracker; print('SEO clients loaded')"

# Check KE credits (requires KE_API_KEY)
python3 -c "from scripts.seo import KeywordsEverywhereClient; c = KeywordsEverywhereClient(); print(c.get_credits())"

# Check DFS balance (requires DATAFORSEO_LOGIN + PASSWORD)
python3 -c "from scripts.seo import DataForSEOClient; c = DataForSEOClient(); print(c.get_balance())"
```

## 6. Usage in Agents

All SEO agents automatically load these credentials from `.env`. You can also pass them explicitly:

```python
from scripts.seo import KeywordsEverywhereClient, DataForSEOClient, CostTracker, SEOCache

# Shared infrastructure
cache = SEOCache()
tracker = CostTracker(budget_limit_usd=25.00)

# Clients share cache + cost tracking
ke = KeywordsEverywhereClient(cache=cache, cost_tracker=tracker)
dfs = DataForSEOClient(cache=cache, cost_tracker=tracker)

# Dry-run cost estimation (no API calls)
estimate = tracker.estimate_pipeline([
    {"provider": "ke", "endpoint": "get_keyword_data", "count": 200},
    {"provider": "dfs", "endpoint": "serp_google_organic_batch", "count": 50},
])
print(f"Estimated cost: ${estimate['estimated_total_usd']}")
print(f"Fits budget: {estimate['fits_budget']}")
```
