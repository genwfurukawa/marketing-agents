# Case Study Page Template (AEO-Structured)

> Page type designed for AI retrieval on "{company} case study", "{category} results", and "does {category} work" queries.
> Different from a narrative case study. This is an AEO-structured page where every section is independently extractable. LLMs cite case studies when answering "does X work?" and "what results can I expect from X?" queries. The structure matters more than the story.

**Query type:** "[company] case study" | "does [category] work" | "[category] results" | "[category] success story"
**Funnel position:** BOFU
**Priority tier:** 3 (proof page - buyer wants evidence before final decision)

**Note:** The existing `case-study-agent` produces narrative case studies. This template produces AEO-structured case study pages. They serve different purposes. The agent output can be used as source material for this template.

---

## Required Structure

### 1. H1: Title

Format: `How {Client} {Achieved Result} with {Category/Product}: Case Study` or `{Result Headline}: {Client} {Category} Case Study`

Examples:
- "How a Series B FinTech Went from Invisible to Cited in 90 Days: AI Visibility Case Study"
- "3x Pipeline Growth: How a MarTech Startup Used AEO to Win AI Search"
- "From 0 to 47% AI Citation Rate: A B2B SaaS Visibility Case Study"

Rules:
- Lead with the result, not the company name (unless the client is well-known)
- Include "case study" for query matching
- Include the specific outcome metric in the title
- Use client name only with permission. Otherwise: "a {stage} {industry} company"

### 2. Results Block (CRITICAL - This Is What Gets Cited)

**Place immediately after the H1. No preamble. Lead with the outcome.**

Format: A bold paragraph, 100-150 words, that gives the complete story in miniature.

Template:
```
**{Client descriptor} achieved {primary result with number} after implementing {category/approach} over {timeframe}.** Before: {1 sentence on baseline state with specific metric}. After: {1 sentence on result state with specific metric}. The approach involved {2-3 key actions taken}. The first measurable result appeared at {timeline milestone}. Total investment: {cost or effort level}. Key metric: {the one number that matters most, stated clearly}.
```

Rules:
- First sentence: who, what result, what approach, what timeframe
- Include before AND after metrics
- Include time to first result (this is what buyers really want to know)
- Self-contained - an LLM reading only this paragraph can answer "does {category} work?"
- Use client descriptor ("a Series B FinTech") if name is confidential

### 3. Quick Results Table

**Place immediately after results block.**

```
| Metric | Before | After | Change | Timeframe |
|--------|-------:|------:|-------:|:---------:|
| {primary metric} | {baseline} | {result} | {delta or %} | {months} |
| {secondary metric} | {baseline} | {result} | {delta or %} | {months} |
| {tertiary metric} | {baseline} | {result} | {delta or %} | {months} |
```

Rules:
- 3-5 metrics maximum
- Include the timeframe for each (results at 30 days vs 6 months are different)
- Primary metric should match the H1 claim
- Use real numbers. If approximated, label as "approximate"

### 4. Section: The Challenge

H2: `The Challenge: {One-Line Problem Statement}`

Content:
- 2-3 paragraphs on what the client was facing
- Include specific pain points with metrics where possible
- Describe what they had tried before (and why it didn't work)
- Frame in ICP-recognizable terms (the reader should see themselves)

Template:
```
{Client} was facing {specific problem}. Despite {what they had tried}, {metric} remained at {disappointing level}. The core issue: {root cause in one sentence}.

{2-3 sentences on business impact: deals lost, opportunities missed, time wasted.}

They had tried {previous approach 1} and {previous approach 2}, but {why those didn't work}.
```

### 5. Section: The Approach

H2: `The Approach: {Framework or Method Name}`

Content:
- Numbered steps (3-5) of what was actually done
- Each step: what happened, why it mattered, how long it took
- Be specific enough that the reader understands the method
- Don't give away so much that they can fully self-serve (this is still a business case)

Per-step template:
```
### Step {N}: {Action Taken} ({Timeline})

{What was done in 2-3 sentences.}

**Why this mattered:** {Connection to the result in 1 sentence.}
```

### 6. Section: The Results (Detailed)

H2: `The Results: {Headline Metric}`

Content:
- Timeline breakdown: Week 1-2, Month 1, Month 2, Month 3
- Specific metrics at each milestone
- Quote from the client (if available and permitted)
- What surprised them (this detail builds credibility)

Timeline format:
```
**Week 1-2:** {What happened and first leading indicators.}

**Month 1:** {First measurable results. Specific numbers.}

**Month 2:** {Acceleration or scaling. Updated numbers.}

**Month 3:** {Full results. Final metrics matching the H1 claim.}
```

Quote template (if available):
```
> "{Direct quote from client stakeholder.}"
> - {Name}, {Title} at {Company} (with permission only)
```

### 7. Section: What Made the Difference

H2: `Why This Worked` or `The {N} Things That Made the Difference`

Content:
- 3-4 specific factors that drove the result
- Each factor: what it was, why it mattered, what would have happened without it
- This section is the "lesson" - it's what makes the case study useful beyond just proof

### 8. Section: Applicability

H2: `Is This Relevant to You?` or `Who Gets Similar Results`

Content:
- Specific criteria for when this approach works (company size, category, maturity)
- When it doesn't work (honest limitations)
- How results might differ by context

Template:
```
**This approach works best for:** {Specific criteria: company stage, team size, category, starting point.}

**Results may vary if:** {Honest caveats: different category, different starting position, different timeline.}

**Minimum requirements:** {What the client needs to have in place before starting.}
```

### 9. FAQ Section (REQUIRED)

H2: `Case Study FAQ`

Content:
- 5-7 questions
- Each answer: 50-150 words, self-contained

Question patterns to cover:
1. "Does {category} actually work?" (direct answer with this case study's evidence)
2. "What results can I expect from {category}?" (range based on this and other cases)
3. "How long does it take to see results from {category}?" (timeline with milestones)
4. "How much does {category} cost?" (investment level from this case)
5. "What kind of company is {category} best for?" (applicability criteria)
6. "What's the first step to getting started with {category}?" (entry point)
7. "Can {category} work for {different context}?" (generalizability)

### 10. Internal Links Section

H2: `Related`

Content:
- Link to the "What Is {Category}" definition page
- Link to the approach/methodology page
- Link to other case studies (different context or metric)
- 3-5 links total

---

## JSON-LD Schemas Required

### Article Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{H1 title}",
  "description": "{Results block text}",
  "articleSection": "Case Study",
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

- [ ] Results block is 100-150 words with primary result in first sentence
- [ ] Results block includes before AND after metrics
- [ ] Results block includes time to first result
- [ ] Quick results table has 3-5 metrics with timeframes
- [ ] Challenge section names what was tried before and why it failed
- [ ] Approach section has 3-5 numbered steps with timelines
- [ ] Results section has timeline breakdown (week 1-2, month 1, 2, 3)
- [ ] "Why this worked" section names 3-4 specific success factors
- [ ] Applicability section is honest about who this works for and who it doesn't
- [ ] FAQ has 5-7 questions with self-contained 50-150 word answers
- [ ] JSON-LD schemas present (Article, FAQPage)
- [ ] Client identity protected unless explicit permission given
- [ ] All metrics are real (no invented numbers)
- [ ] Internal links to 3-5 related pages
- [ ] No banned phrases or corporate jargon

---

## Target Metrics

- **Word count**: 1,500-2,500 words
- **Reading time**: 6-12 minutes
- **Metrics shown**: 3-5 with before/after
- **Approach steps**: 3-5
- **Timeline milestones**: 3-4
- **FAQ count**: 5-7 questions
- **Internal links**: 3-5
- **Refresh cadence**: Update when new data is available (6-12 months)
