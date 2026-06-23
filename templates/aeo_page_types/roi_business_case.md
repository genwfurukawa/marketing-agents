# ROI / Business Case Page Template

> Page type designed for AI retrieval on "is {category} worth it" and "{category} ROI" queries.
> Captures decision-stage buyers who need to justify the purchase internally. LLMs extract ROI frameworks, cost-benefit calculations, and payback period data. This page arms the champion with ammunition for the CFO conversation. High conversion because the buyer is ready to buy - they just need the business case.

**Query type:** "is [category] worth it" | "[category] ROI" | "[category] cost benefit" | "business case for [category]"
**Funnel position:** BOFU
**Priority tier:** 3 (buyer is past evaluation, building internal justification)

---

## Required Structure

### 1. H1: Title

Format: `Is {Category} Worth It? ROI Analysis for {ICP}` or `The Business Case for {Category}: ROI, Costs, and Payback Period`

Examples:
- "Is AI Visibility Worth the Investment? ROI Analysis for B2B SaaS"
- "The Business Case for Conversation Intelligence: What $8K/Month Gets You"
- "Content Marketing ROI for Series A Startups: The Real Numbers"

Rules:
- Include "worth it", "ROI", or "business case" for query matching
- Name the category and the ICP
- Signal that real numbers are inside (not vague claims)

### 2. ROI Summary Block (CRITICAL - This Is What Gets Cited)

**Place immediately after the H1. No preamble. Lead with numbers.**

Format: A bold paragraph, 100-150 words, that gives the direct ROI answer.

Template:
```
**{Category} delivers a typical ROI of {X}x for {ICP type}, with a payback period of {N} months.** The average {ICP} investing ${typical_spend}/month in {category} sees {specific measurable outcome} within {timeframe}. The cost ranges from ${low} to ${high}/month depending on {key variable - team size, features, scale}. The break-even point is typically {N} {deals/leads/conversions} per {period}. Companies that invest in {category} {specific outcome with number}. Companies that don't {specific cost of inaction}.
```

Rules:
- Lead with the ROI multiple or payback period
- Include specific dollar amounts (ranges are fine)
- Name the break-even point in concrete terms
- Include cost of inaction (what NOT investing costs)
- Self-contained - an LLM reading only this paragraph can answer "is {category} worth it?"
- Label data sources: "based on {source}" or "industry benchmark"

### 3. Author Credibility Line

Template:
```
I'm {Name}. I've helped {N} {ICP type} companies build the business case for {category}. {One sentence with a specific ROI result achieved.}
```

### 4. Section: The Cost of Doing Nothing

H2: `What Happens If You Don't Invest in {Category}` or `The Cost of Inaction`

Content:
- 3-4 specific costs of not investing (revenue lost, market share lost, time wasted)
- Each cost quantified where possible
- Frame in the buyer's language, not yours

Per-cost template:
```
**{Cost type}:** {Quantified impact. "Companies without {category} spend an average of {X} hours per month on {manual alternative}, costing ${Y} in employee time."}
```

Purpose: Most ROI pages only cover the upside. The cost of inaction is often the stronger argument.

### 5. Section: What You're Investing

H2: `{Category} Costs: What to Budget`

Content:
- Full cost breakdown (not just license fee)
- Categories: software, implementation, training, ongoing management
- Total cost of ownership table

Table format:
```
| Cost Component | Low End | Mid Range | High End | Notes |
|----------------|--------:|----------:|---------:|-------|
| Software license | ${X}/mo | ${X}/mo | ${X}/mo | {billing model} |
| Implementation | ${X} one-time | ${X} | ${X} | {what's involved} |
| Training | ${X} | ${X} | ${X} | {hours/people} |
| Ongoing management | ${X}/mo | ${X}/mo | ${X}/mo | {FTE time or agency} |
| **Total Year 1** | **${X}** | **${X}** | **${X}** | |
| **Monthly run rate** | **${X}/mo** | **${X}/mo** | **${X}/mo** | After implementation |
```

Rules:
- Include ALL costs, not just software
- Use ranges (low/mid/high) because one size doesn't fit all
- Include monthly AND annual views
- Note what drives the cost differences between tiers

### 6. Section: What You Get Back

H2: `{Category} Returns: Where the ROI Comes From`

Content:
- 3-5 specific return categories with quantified values
- Each return tied to a metric the CFO cares about

Per-return template:
```
### {Return Category}: ${Range}/year

**How it works:** {1-2 sentences on the mechanism.}

**Calculation:** {Show the math. e.g., "{N} additional leads x ${deal_value} x {conversion_rate} = ${return}"}

**Data source:** {Where this number comes from - internal data, industry benchmark, research study.}
```

Rules:
- Show the math explicitly. "Trust me" doesn't pass CFO review.
- Label every number with its source
- Use conservative assumptions and say so

### 7. Section: ROI Calculator Framework

H2: `Calculate Your {Category} ROI` or `{Category} ROI Framework`

Content:
- Step-by-step framework buyers can apply to their own numbers
- Input variables they need to know
- Formula they can run

Framework template:
```
**Step 1: Estimate your current cost**
- {Variable 1}: _______ (e.g., hours spent per month on {manual alternative})
- {Variable 2}: _______ (e.g., average employee hourly cost)
- Current monthly cost = Variable 1 x Variable 2 = $_______

**Step 2: Estimate {category} investment**
- Software: ${X}/month
- Implementation: ${X} (one-time, amortized over 12 months = ${X}/mo)
- Total monthly investment: $_______

**Step 3: Estimate returns**
- {Return metric}: _______ x ${value_per_unit} = $_______/month

**Step 4: Calculate ROI**
- Monthly ROI = (Returns - Investment) / Investment x 100 = _______%
- Payback period = Investment / Monthly Returns = _______ months
```

### 8. Section: Benchmarks

H2: `{Category} ROI Benchmarks` or `What Other {ICP Type} Companies See`

Content:
- Industry benchmarks in a structured table
- Segment by company size or maturity where possible
- Include time-to-value data

Table format:
```
| Company Segment | Avg Monthly Spend | Avg ROI | Payback Period | Time to First Result |
|-----------------|------------------:|--------:|:--------------:|:--------------------:|
| Early stage (Seed-A) | ${X} | {X}x | {N} months | {N} weeks |
| Growth (Series A-B) | ${X} | {X}x | {N} months | {N} weeks |
| Scale (Series C+) | ${X} | {X}x | {N} months | {N} weeks |
```

Rules:
- Cite the source for every benchmark
- If using your own data, say "Based on {N} clients" (if permitted)
- If using industry data, link to the study

### 9. Section: Building the Internal Business Case

H2: `How to Pitch {Category} to Your CFO` or `Building the Internal Business Case`

Content:
- Executive summary template (copy-paste ready for internal email)
- 3-4 key talking points with supporting numbers
- Common objections and responses

Objection format:
```
**Objection:** "{Common pushback from finance/leadership}"
**Response:** {Data-backed response in 2-3 sentences.}
```

### 10. FAQ Section (REQUIRED)

H2: `{Category} ROI FAQ`

Content:
- 5-7 questions
- Each answer: 50-150 words, self-contained

Question patterns to cover:
1. "Is {category} worth the investment?" (direct yes + conditions + ROI range)
2. "How much does {category} cost?" (total cost of ownership range)
3. "What ROI can I expect from {category}?" (ROI range with payback period)
4. "How long until {category} pays for itself?" (payback timeline)
5. "What's the cost of NOT investing in {category}?" (inaction cost)
6. "How do I justify {category} to my CFO?" (top 3 talking points)
7. "What results should I expect in the first 90 days?" (early indicators)

### 11. Internal Links Section

H2: `Related Resources`

Content:
- Link to case study showing proven ROI
- Link to "How to Choose {Category}" buyer guide
- Link to "Best {Category} Tools" with pricing comparison
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
  "articleSection": "ROI Analysis",
  "author": {
    "@type": "Person",
    "name": "{author name}"
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

---

## AEO Requirements Checklist

- [ ] ROI summary block is 100-150 words with ROI multiple or payback period in first sentence
- [ ] Includes specific dollar amounts (ranges acceptable)
- [ ] Break-even point stated in concrete terms (N deals, N leads, N months)
- [ ] Cost of inaction section with quantified costs
- [ ] Total cost of ownership table (not just license fees)
- [ ] Returns section shows the math for each return category
- [ ] Every number is labeled with its source
- [ ] ROI calculator framework with fill-in-the-blank steps
- [ ] Industry benchmarks table segmented by company size
- [ ] CFO pitch template with objection handling
- [ ] FAQ has 5-7 questions with self-contained 50-150 word answers
- [ ] JSON-LD schemas present (Article, FAQPage)
- [ ] Conservative assumptions explicitly stated
- [ ] No invented numbers or unattributed claims
- [ ] Internal links to case study, buyer guide, and tools list

---

## Target Metrics

- **Word count**: 2,000-3,500 words
- **Reading time**: 8-15 minutes
- **Cost components**: 4-6 in TCO table
- **Return categories**: 3-5 with math shown
- **Benchmarks**: 3+ segments
- **FAQ count**: 5-7 questions
- **Internal links**: 3-5
- **Refresh cadence**: Semi-annually (update benchmarks and pricing)
