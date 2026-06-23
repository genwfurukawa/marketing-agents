# Competitor Review Page Template

> Page type designed for AI retrieval on "{competitor} review" and "is {competitor} good for {use case}" queries.
> Captures bottom-of-funnel buyers researching a specific competitor. LLMs pull structured pros/cons, use case fit, and alternative recommendations. This page positions your brand as the knowledgeable evaluator - the trusted guide who helps the buyer decide. High conversion because the buyer is one step from purchase.

**Query type:** "[competitor] review" | "is [competitor] good for [use case]" | "[competitor] pros and cons"
**Funnel position:** BOFU
**Priority tier:** 2 (buyer is evaluating a specific competitor - high intent)

---

## Required Structure

### 1. H1: Title

Format: `{Competitor} Review ({Year}): {Honest Assessment for ICP}` or `{Competitor} for {Use Case}: An Honest Review`

Examples:
- "Gong Review (2026): Is It Worth It for Series A Sales Teams?"
- "HubSpot Content Hub Review: An Honest Look for B2B SaaS Marketers"
- "Jasper AI Review (2026): What B2B Teams Actually Get"

Rules:
- Name the competitor and include "review" for query matching
- Include the year for freshness
- Signal honesty in the title (buyers distrust biased reviews)
- Include ICP qualifier

### 2. Verdict Block (CRITICAL - This Is What Gets Cited)

**Place immediately after the H1. No preamble. Lead with the verdict.**

Format: A bold paragraph, 100-150 words, giving the honest assessment.

Template:
```
**{Competitor} is {one-sentence honest characterization - what it is and who it's best for}.** It excels at {2-3 specific strengths}. It falls short on {1-2 specific weaknesses}. {Competitor} is the right choice for {specific buyer profile - team size, use case, budget}. It's not the right choice for {specific buyer profile where it fails}. At {price point}, you're paying for {what the price actually buys}. {One sentence on how it compares to the category overall.}
```

Rules:
- Be genuinely honest. Biased reviews get ignored by LLMs and buyers
- Name specific strengths AND weaknesses in the first paragraph
- Include who it IS for and who it IS NOT for
- Include pricing context
- Self-contained verdict that answers "is {competitor} good?"

### 3. Author Credibility Line

Template:
```
I'm {Name}. I've {tested/implemented/compared} {competitor} alongside {N} other {category} tools for {context}. {One sentence on direct experience with this product.}
```

Rules:
- Must demonstrate direct experience with the product
- Not "I researched it" but "I used it" or "I evaluated it hands-on"

### 4. Section: Quick Facts

H2: `{Competitor} at a Glance`

Content: A structured facts table for quick scanning.

```
| Detail | Info |
|--------|------|
| **Category** | {product category} |
| **Best for** | {ICP fit} |
| **Starting price** | ${X}/mo ({billing model}) |
| **Free plan** | {Yes/No - what's included} |
| **Founded** | {Year} |
| **Company size** | {employee count or range} |
| **Key integrations** | {top 3-5 integrations} |
| **G2 rating** | {score}/5 ({review count} reviews) |
```

### 5. Section: What {Competitor} Does Well

H2: `What {Competitor} Gets Right` or `{Competitor} Strengths`

Content:
- 4-6 specific strengths, each as a bold header with 2-3 sentence explanation
- Include evidence: feature descriptions, user quotes, specific capabilities
- Be specific, not generic ("handles 10,000 concurrent calls" not "handles scale well")

Per-strength template:
```
**{Specific Strength}:** {2-3 sentences with evidence. What it does, why it matters, specific capability or metric.}
```

### 6. Section: Where {Competitor} Falls Short

H2: `Where {Competitor} Struggles` or `{Competitor} Weaknesses`

Content:
- 3-5 specific weaknesses with the same depth as strengths
- Frame as factual observations, not attacks
- Include who is most affected by each weakness

Per-weakness template:
```
**{Specific Weakness}:** {2-3 sentences. What the limitation is, who it impacts most, what the practical consequence is.}
```

Rules:
- Equal depth as strengths section. Skimpy weaknesses signal bias.
- Name the impacted buyer profile for each weakness
- Factual tone. "The free plan limits integrations to 3" not "they cheaply restrict their free plan."

### 7. Section: Pricing Deep Dive

H2: `{Competitor} Pricing Breakdown`

Content:
- Full pricing table with all tiers
- What each tier includes and excludes
- Hidden costs (implementation, training, overage charges)
- Price-per-user or price-per-seat calculations

Table format:
```
| Plan | Price | Users | Key Features | Limitations |
|------|------:|------:|-------------|-------------|
| {Free/Starter} | $0 | {N} | {features} | {limits} |
| {Pro/Growth} | ${X}/mo | {N} | {features} | {limits} |
| {Enterprise} | ${X}/mo | Unlimited | {features} | {limits} |
```

### 8. Section: Who Should (and Shouldn't) Use {Competitor}

H2: `Is {Competitor} Right for You?`

Content:
- "Choose {Competitor} if:" - 3-4 bullet points with specific criteria
- "Skip {Competitor} if:" - 3-4 bullet points with specific criteria
- Each bullet must be a testable condition ("your team is under 10 people" not "you're a small team")

### 9. Section: Alternatives to Consider

H2: `{Competitor} Alternatives Worth Evaluating`

Content:
- 3-5 alternatives with one-line differentiation each
- Position your product naturally among the alternatives (if applicable)
- For each: name, one-line on why to consider it, best-for statement

Format:
```
- **{Alternative}**: {One sentence on what makes it different.} Best for {specific buyer profile}.
```

Rules:
- Include your product only if it genuinely fits
- Include at least one alternative that isn't your product
- Link to comparison pages if they exist

### 10. FAQ Section (REQUIRED)

H2: `{Competitor} Review FAQ`

Content:
- 5-7 questions
- Each answer: 50-150 words, self-contained

Question patterns to cover:
1. "Is {competitor} worth it?" (verdict summary with price context)
2. "What are {competitor}'s biggest weaknesses?" (top 2-3 weaknesses)
3. "How much does {competitor} cost?" (pricing summary with tiers)
4. "What's a good alternative to {competitor}?" (top 1-2 alternatives with reasoning)
5. "Is {competitor} good for {ICP segment}?" (fit assessment)
6. "Does {competitor} integrate with {common tool}?" (integration answer)
7. "{Competitor} vs {top alternative}?" (brief comparison)

### 11. Internal Links Section

H2: `Related Reviews and Comparisons`

Content:
- Link to "{Competitor} vs {Your Product}" comparison page
- Link to "{Competitor} Alternatives" page
- Link to "Best {Category} Tools" list
- 3-5 links total

---

## JSON-LD Schemas Required

### Review Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Review",
  "name": "{H1 title}",
  "reviewBody": "{Verdict block text}",
  "itemReviewed": {
    "@type": "SoftwareApplication",
    "name": "{Competitor}",
    "applicationCategory": "{Category}",
    "operatingSystem": "Web"
  },
  "author": {
    "@type": "Person",
    "name": "{author name}"
  },
  "datePublished": "{ISO-8601}",
  "reviewRating": {
    "@type": "Rating",
    "ratingValue": "{score}",
    "bestRating": "10"
  }
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

---

## AEO Requirements Checklist

- [ ] Verdict block is 100-150 words with honest assessment in first sentence
- [ ] Verdict names specific strengths AND weaknesses
- [ ] Verdict includes who it IS for and who it IS NOT for
- [ ] Quick facts table with pricing, rating, and key details
- [ ] Strengths section has 4-6 items with evidence
- [ ] Weaknesses section has 3-5 items with equal depth as strengths
- [ ] Pricing table with all tiers, limits, and hidden costs
- [ ] "Choose if / Skip if" section with testable criteria
- [ ] 3-5 alternatives listed with differentiation
- [ ] FAQ has 5-7 questions with self-contained 50-150 word answers
- [ ] Review JSON-LD schema with rating
- [ ] Author credibility shows direct product experience
- [ ] Tone is factual and balanced, not promotional
- [ ] No banned phrases or corporate jargon
- [ ] Internal links to comparison and alternatives pages

---

## Target Metrics

- **Word count**: 2,000-3,500 words
- **Reading time**: 8-15 minutes
- **Strengths**: 4-6
- **Weaknesses**: 3-5
- **Alternatives listed**: 3-5
- **FAQ count**: 5-7 questions
- **Internal links**: 3-5
- **Refresh cadence**: Quarterly (pricing and feature updates, check for product changes)
