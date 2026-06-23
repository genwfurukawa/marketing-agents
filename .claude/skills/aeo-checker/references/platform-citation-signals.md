# Platform Citation Signals
# Used by: aeo-checker, visibility-tracker, visibility-report-writer
# Sources: Princeton GEO study (KDD 2024), SE Ranking domain authority analysis,
#          ZipTie content-answer fit analysis (400K pages)

---

## The Universal Requirements (All Platforms)

Three things are required before any platform can cite you:

1. **Your content must be indexed** by the platform's search backend
2. **AI bots must be allowed** in your robots.txt
3. **Your content must be extractable** — clean structure, self-contained passages

Without all three: citation rate = 0, regardless of content quality.

---

## robots.txt Configuration (Allow All AI Bots)

```
User-agent: GPTBot          # OpenAI ChatGPT search
User-agent: ChatGPT-User    # ChatGPT browsing
User-agent: PerplexityBot   # Perplexity AI search
User-agent: ClaudeBot        # Anthropic Claude
User-agent: anthropic-ai    # Anthropic Claude (alternate)
User-agent: Google-Extended  # Google Gemini + AI Overviews
User-agent: Bingbot          # Microsoft Copilot (via Bing)
Allow: /
```

Safe to block (training only, no citation impact):
```
User-agent: CCBot           # Common Crawl — training datasets only
Disallow: /
```

---

## Platform-Specific Signals

### Google AI Overviews

**Search backend:** Google's own index
**Appears in:** ~45% of Google searches
**Click impact:** Reduces organic clicks by up to 58%

**Key signals:**
- E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)
- Schema markup: Article, FAQPage, HowTo, Product — 30–40% visibility boost
- Authoritative citations within content: +132% visibility
- Authoritative tone (not salesy): +89% visibility
- Only 15% of AI Overview sources overlap with traditional top-10 results
  (pages not on page 1 can still get cited with right structure)
- Knowledge Graph presence helps — accurate Wikipedia entry is a signal

**Content priorities for Google AIO:**
1. Schema markup (single biggest lever)
2. Named, sourced citations within content
3. Author credentials and E-E-A-T signals
4. "What is" and "How to" query patterns trigger AIO most often
5. Topical authority clusters with strong internal linking

---

### ChatGPT (with web search)

**Search backend:** Bing-based index
**Key research:** SE Ranking analysis of 129K domains

**Citation weight breakdown:**
- Domain authority and credibility signals: ~40%
- Content quality (answer fit): ~35%
- Platform trust signals: ~25%

**Freshness is critical:**
- Content updated within 30 days: 3.2x higher citation rate than older content
- Update competitive content monthly

**Content-answer fit (ZipTie, 400K pages):**
- How well your content matches ChatGPT's response format: ~55% of citation likelihood
- Domain authority alone: ~12%
- On-page structure alone: ~14%
- Write the way ChatGPT would answer the question

**High-authority citation benchmarks:**
- Very high referring domain count (350K+): ~8.4 citations per response
- Sites with trust score 91–96 vs 97–100: 8.4 → 6 citations

**Where ChatGPT cites:**
- Wikipedia: 7.8% of all citations
- Reddit: 1.8%
- Forbes: 1.1%
- Brand official sites: cited frequently but third-party carries more weight

**Priorities for ChatGPT:**
1. Domain authority via backlinks (strongest baseline)
2. Monthly content updates
3. Match content structure to ChatGPT's answer format
4. Specific statistics with named sources

---

### Perplexity

**Search backend:** Own index + Google sources
**Behavior:** Always cites with visible links (most transparent platform)
**Index approach:** Multiple reranking passes + quality threshold filtering

**Unique signals:**
- FAQ Schema (JSON-LD): noticeably higher citation rate
- PDF documents: publicly accessible PDFs prioritized
- Publishing velocity: how frequently you publish matters
- Self-contained paragraphs: atomically complete, extractable passages
- Curated domain lists: Amazon, GitHub, major academic sites get inherent boost
- Time-decay algorithm: evaluates new content quickly (fresh publishers can compete)

**Priorities for Perplexity:**
1. Allow PerplexityBot in robots.txt
2. FAQPage schema on any page with Q&A content
3. Publicly hosted PDFs (whitepapers, guides, reports)
4. Article schema with publication and modification timestamps
5. Self-contained paragraphs (each paragraph works standalone)
6. Deep topical authority in specific niche

---

### Microsoft Copilot

**Search backend:** Bing's index exclusively
**Distribution:** Edge, Windows, Microsoft 365, Bing Search

**Unique signals:**
- Bing Webmaster Tools submission (many sites only submit to Google)
- IndexNow protocol for faster Bing indexing
- LinkedIn mentions and content get ranking boost
- GitHub presence if relevant
- Page speed threshold: sub-2-second load times

**Priorities for Copilot:**
1. Submit to Bing Webmaster Tools
2. Use IndexNow protocol
3. Page speed under 2 seconds
4. Explicit entity definitions in content
5. LinkedIn articles and company page presence

---

### Claude (Anthropic)

**Search backend:** Brave Search (when web search enabled)
**Citation behavior:** Extremely selective — very low citation rate overall

**Key signals:**
- Brave Search index visibility (verify at search.brave.com)
- ClaudeBot and anthropic-ai allowed in robots.txt
- Factual density: specific numbers, named sources, dated statistics
- Descriptive heading structure
- Cited authoritative sources within content
- Most factually accurate source on the topic

**Priorities for Claude:**
1. Verify content appears in Brave Search results
2. Allow ClaudeBot and anthropic-ai in robots.txt
3. Maximize factual density — specific numbers and named sources
4. Aim to be the most accurate (not just the most comprehensive) source

---

## Princeton GEO Study Summary (KDD 2024)

Tested on Perplexity.ai. 9 optimization methods ranked by visibility impact:

| Method | Visibility Boost | Category |
|--------|:---------------:|----------|
| Cite authoritative sources | +40% | Authority |
| Add statistics with sources | +37% | Authority |
| Add expert quotes | +30% | Authority |
| Authoritative tone | +25% | Authority |
| Improve clarity | +20% | Structure |
| Technical terminology | +18% | Authority |
| Unique vocabulary | +15% | Structure |
| Fluency optimization | +15–30% | Structure |
| Keyword stuffing | **-10%** | ❌ Harmful |

**Best combination:** Fluency + statistics = maximum citation boost
**Low-authority sites benefit more:** Up to 115% visibility increase with
citations + statistics

---

## Citation Rate Benchmarks

Target citation rates by month:

| Month | Target citation rate | Notes |
|-------|:-------------------:|-------|
| Baseline (pre-work) | 0–15% | Typical for unoptimized content |
| Month 1 | 15–30% | After foundation + first AEO pages |
| Month 2 | 30–50% | With query bank + FAQ optimization |
| Month 3+ | 50–70% | Full AEO structure + freshness signals |

**Industry benchmarks (comparison queries specifically):**
- Companies with no AEO work: 0–10% citation rate on comparison queries
- Companies with SEO but no AEO: 10–25%
- Companies with full AEO methodology: 40–70%

---

## Content Types by Citation Likelihood

| Content Type | Citation share | Why AI cites it |
|-------------|:------------:|----------------|
| Comparison articles | ~33% | Structured, balanced, high-intent match |
| Definitive guides | ~15% | Comprehensive, authority signals |
| Original research | ~12% | Unique, citable statistics |
| Best-of/listicles | ~10% | Clear structure, entity-rich |
| Product pages | ~10% | Specific extractable details |
| How-to guides | ~8% | Step-by-step structure |
| Opinion/analysis | ~10% | Expert perspective, quotable |

**Underperformers:**
- Generic blog posts without structure
- Thin product pages with marketing language
- Gated content (AI can't access)
- Content without dates or author attribution
