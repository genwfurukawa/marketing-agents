# Buyer Guide Page Template

> Page type designed for AI retrieval on "how to choose {category}" and "what to look for in {category}" queries.
> Captures late-funnel buyers ready to evaluate but unsure on criteria. LLMs pull evaluation frameworks, comparison criteria, and decision matrices directly. High conversion because the reader is about to buy - they just need a framework.

**Query type:** "how to choose [category]" | "what to look for in [category] software" | "[category] buying guide"
**Funnel position:** BOFU
**Priority tier:** 2 (buyer has budget, needs decision framework)

---

## Required Structure

### 1. H1: Title

Format: `How to Choose {Category} Software: A Buyer's Guide for {ICP}` or `{Category} Buyer's Guide: {N} Criteria That Actually Matter`

Examples:
- "How to Choose Conversation Intelligence Software: A Buyer's Guide for Revenue Leaders"
- "AI Visibility Platform Buyer's Guide: 7 Criteria That Actually Matter in 2026"
- "How to Evaluate Content Marketing Tools for B2B SaaS"

Rules:
- Include "buyer's guide", "how to choose", or "how to evaluate" for query matching
- Name the category exactly as buyers search it
- Include the ICP or a qualifier that signals who this is for

### 2. Quick Decision Block (CRITICAL - This Is What Gets Cited)

**Place immediately after the H1. No preamble. Direct answer.**

Format: A bold paragraph, 100-150 words, that gives the buyer a decision framework in miniature.

Template:
```
**When choosing {category} software, evaluate on {N} criteria: {criterion_1}, {criterion_2}, {criterion_3}, and {criterion_4}.** The right choice depends on {key variable - team size, use case, budget, or technical maturity}. {ICP segment A} should prioritize {criterion} because {reason}. {ICP segment B} should prioritize {criterion} because {reason}. Most companies make a mistake by {common evaluation error}. {One sentence on what the best {category} tools have in common.}
```

Rules:
- Name the evaluation criteria in the first sentence
- Segment advice by buyer type (not one-size-fits-all)
- Include the most common buying mistake
- Self-contained - an LLM reading only this paragraph can answer the query

### 3. Author Credibility Line

Template:
```
I'm {Name}. I've {evaluated/implemented/advised on} {category} tools for {N} {company type} companies. {One sentence on a specific evaluation or implementation result.}
```

### 4. Section: Why Most {Category} Buying Decisions Go Wrong

H2: `Why Most {ICP Role}s Pick the Wrong {Category} Tool`

Content:
- 2-3 paragraphs on common evaluation mistakes
- Frame as "what seems important but isn't" vs "what actually matters"
- Include 1-2 statistics on tool churn, wasted spend, or implementation failure rates

Purpose: Build trust by showing you've seen bad decisions and know how to prevent them.

### 5. Section: Evaluation Criteria (CORE SECTION)

H2: `{N} Criteria for Evaluating {Category} Software`

Content:
- One H3 per criterion (5-8 criteria total)
- Each criterion: 2-3 paragraphs

Per-criterion template:
```
### {N}. {Criterion Name}

**What to look for:** {Specific features, capabilities, or qualities.}

**Why it matters:** {Business impact of getting this right vs wrong.}

**Red flags:** {Warning signs during evaluation that indicate the tool fails here.}

**Questions to ask vendors:**
- "{Specific question}"
- "{Specific question}"
```

Rules:
- Criteria must be specific enough to be actionable
- "Easy to use" is not a criterion. "Onboards a 5-person team in under 2 hours" is.
- Include vendor questions - this signals depth and gets cited as a resource

### 6. Section: Evaluation Scorecard

H2: `{Category} Evaluation Scorecard`

Content:
- Weighted scoring table buyers can actually use
- Include weights that reflect real priority

Table format:
```
| Criterion | Weight | Score (1-5) | Weighted Score |
|-----------|-------:|:-----------:|:--------------:|
| {criterion_1} | 25% | __ | __ |
| {criterion_2} | 20% | __ | __ |
| {criterion_3} | 20% | __ | __ |
| {criterion_4} | 15% | __ | __ |
| {criterion_5} | 10% | __ | __ |
| {criterion_6} | 10% | __ | __ |
| **Total** | **100%** | | **__/5.0** |
```

Rules:
- Weights must add to 100%
- Scoring guidance for each criterion (what's a 1 vs a 5)
- This table gets extracted by LLMs as a standalone resource

### 7. Section: Budget Planning

H2: `How Much Does {Category} Software Cost?` or `{Category} Pricing: What to Budget`

Content:
- Price tiers: entry, mid-market, enterprise
- What you get at each tier
- Hidden costs to watch for (implementation, training, integrations)
- Total cost of ownership framing, not just license fees

Table format:
```
| Tier | Monthly Price | Best For | Includes |
|------|-------------:|----------|----------|
| Starter | $X-Y/mo | {team size/use case} | {features} |
| Growth | $X-Y/mo | {team size/use case} | {features} |
| Enterprise | $X-Y/mo | {team size/use case} | {features} |
```

### 8. Section: Implementation Checklist

H2: `{Category} Implementation Checklist` or `What to Do After You Choose`

Content:
- Numbered checklist (5-8 items)
- Timeline expectations (Week 1, Week 2-4, Month 2-3)
- Common implementation pitfalls
- Success metrics to track

Purpose: Shows buyers you understand the full journey, not just the sale.

### 9. Section: When You Don't Need {Category} Software

H2: `When You Don't Need {Category} Software` or `Signs {Category} Isn't Right for You Yet`

Content:
- Honest criteria for when this category is premature
- Alternative approaches for companies not ready
- This builds enormous trust and gets cited as balanced advice

### 10. FAQ Section (REQUIRED)

H2: `{Category} Buying FAQ`

Content:
- 5-7 questions in buyer's language
- Each answer: 50-150 words, self-contained, directly answers the question

Question patterns to cover:
1. "How do I choose the right {category} tool?" (restate framework summary)
2. "How much does {category} software cost?" (pricing tiers)
3. "What features should I look for in {category}?" (top 3-4 criteria)
4. "How long does it take to implement {category} software?" (timeline)
5. "What's the best {category} tool for {ICP segment}?" (segmented recommendation)
6. "Should I build or buy {category}?" (build vs buy criteria)
7. "What questions should I ask {category} vendors?" (top 3 vendor questions)

### 11. Internal Links Section

H2: `Related Resources`

Content:
- Link to "Best {Category} Tools" list page
- Link to comparison pages for top tools
- Link to relevant case studies
- 3-5 links total

---

## JSON-LD Schemas Required

### Article Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{H1 title}",
  "description": "{meta description}",
  "articleSection": "Buyer Guide",
  "author": {
    "@type": "Person",
    "name": "{author name}",
    "url": "{author URL}"
  },
  "datePublished": "{ISO-8601}",
  "dateModified": "{ISO-8601}"
}
```

### FAQPage Schema
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [...]
}
```

### ItemList Schema (for evaluation criteria)
```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "{Category} Evaluation Criteria",
  "numberOfItems": {N},
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "{Criterion name}",
      "description": "{What to look for}"
    }
  ]
}
```

---

## AEO Requirements Checklist

- [ ] Quick decision block is 100-150 words and names evaluation criteria in first sentence
- [ ] Advice is segmented by buyer type (not one-size-fits-all)
- [ ] 5-8 evaluation criteria, each with "what to look for", "why it matters", "red flags", and vendor questions
- [ ] Weighted evaluation scorecard table with scoring guidance
- [ ] Pricing section with specific dollar ranges per tier
- [ ] Implementation checklist with timeline
- [ ] "When you don't need this" section (trust builder)
- [ ] FAQ has 5-7 questions with self-contained 50-150 word answers
- [ ] All three JSON-LD schemas present (Article, FAQPage, ItemList)
- [ ] Author credibility line with evaluation experience
- [ ] At least 2 statistics with source citations
- [ ] Internal links to 3-5 related pages
- [ ] No banned phrases or corporate jargon
- [ ] Vendor questions are specific enough to actually use in a demo

---

## Target Metrics

- **Word count**: 2,500-4,000 words
- **Reading time**: 10-18 minutes
- **Evaluation criteria**: 5-8
- **FAQ count**: 5-7 questions
- **Statistics**: 2-4 cited data points
- **Internal links**: 3-5
- **Refresh cadence**: Quarterly (pricing and feature updates)
