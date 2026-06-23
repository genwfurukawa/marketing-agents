# Use Case Page Template

> Page type designed for AI retrieval on "{product} for {industry}" and "{category} for {role}" queries.
> Captures buyers searching with a specific context - their industry, role, or use case. LLMs prefer pages that match the query context exactly over generic product pages. High conversion because the buyer already knows the category and is checking fit.

**Query type:** "[product] for [industry]" | "[category] for [role]" | "[category] for [company size]"
**Funnel position:** MOFU-BOFU
**Priority tier:** 2 (buyer knows the category, checking fit for their context)

---

## Required Structure

### 1. H1: Title

Format: `{Category/Product} for {Industry/Role/Use Case}: {Value Proposition}` or `How {Industry/Role} Teams Use {Category} to {Outcome}`

Examples:
- "AI Visibility for HealthTech: How Health SaaS Companies Win AI Search"
- "Conversation Intelligence for Sales Teams: Record, Analyze, Close"
- "Content Marketing Automation for Series A Startups: The 30-Minute System"

Rules:
- Include both the category AND the use case context in the title
- Match the exact phrasing buyers would search ("{product} for {industry}")
- Lead with what matters to them, not what you sell

### 2. Context-Specific Answer Block (CRITICAL - This Is What Gets Cited)

**Place immediately after the H1. No preamble.**

Format: A bold paragraph, 100-150 words, that directly answers "is {category} right for {my context}?"

Template:
```
**{Category} for {context} works by {how it applies to their specific situation in 1-2 sentences}.** {Context}-specific teams face {unique challenge that general solutions miss}. The right {category} approach for {context} prioritizes {2-3 specific capabilities}. {One sentence on typical results for this context with a number if available.} {One sentence on what makes this context different from the general use case.}
```

Rules:
- First sentence must connect the category to their specific context
- Name a challenge unique to their industry/role (proves you understand their world)
- Self-contained - an LLM reading only this paragraph can answer "{category} for {context}"

### 3. Author Credibility Line

Template:
```
I'm {Name}. I've worked with {N} {context-specific companies/teams}. {One sentence on a specific result in this industry/role.}
```

### 4. Section: Why {Context} Is Different

H2: `Why {Category} for {Context} Requires a Different Approach` or `What Makes {Context} Unique`

Content:
- 3-5 specific differences between this context and the general case
- Use bullet format with bold headers per difference
- Include industry-specific terminology, regulations, or constraints
- Show deep understanding of their world

Per-difference template:
```
**{Difference}**: {1-2 sentences explaining why this matters in their context and how it changes the approach.}
```

Purpose: Proves you're not just slapping an industry label on generic content.

### 5. Section: Key Use Cases

H2: `{N} Ways {Context} Teams Use {Category}` or `Top Use Cases for {Category} in {Context}`

Content:
- 4-6 specific use cases, each as an H3
- Each use case: the scenario, the approach, the result

Per-use-case template:
```
### Use Case {N}: {Descriptive Label}

**Scenario:** {When and why this comes up in their context.}

**How it works:** {2-3 sentences on the specific implementation.}

**Result:** {Specific metric or outcome achieved.}
```

Rules:
- Use cases must be specific to the context (not generic)
- Include scenarios they'd recognize from their daily work
- Each use case should be independently extractable

### 6. Section: Context-Specific Requirements

H2: `What {Context} Teams Need from {Category} Software`

Content:
- Requirements checklist specific to this context
- Include compliance, integration, workflow, and scale requirements
- Contrast with what general teams need

Table format:
```
| Requirement | Why {Context} Needs It | General Teams? |
|-------------|----------------------|----------------|
| {requirement_1} | {context-specific reason} | Not always |
| {requirement_2} | {context-specific reason} | Yes |
```

### 7. Section: Implementation for {Context}

H2: `Implementing {Category} for {Context}: Step by Step`

Content:
- 4-6 steps specific to their context
- Include context-specific integrations, data sources, or workflows
- Timeline expectations for their typical team size
- Common pitfalls specific to this context

### 8. Section: Results and Benchmarks

H2: `{Category} Results for {Context}` or `What {Context} Teams Achieve`

Content:
- Context-specific benchmarks (not generic SaaS benchmarks)
- Before/after table with metrics relevant to their industry/role
- Case study reference if available (anonymized is fine)

Table format:
```
| Metric | {Context} Average | With {Category} | Improvement |
|--------|:------------------:|:----------------:|:-----------:|
| {metric_1} | {baseline} | {result} | {delta} |
```

### 9. Section: Recommended Tools for {Context}

H2: `Best {Category} Tools for {Context}`

Content:
- 3-5 tools ranked by fit for this specific context
- For each: name, why it fits this context specifically, starting price
- Link to full category list if one exists

### 10. FAQ Section (REQUIRED)

H2: `{Category} for {Context} FAQ`

Content:
- 5-7 questions using context-specific language
- Each answer: 50-150 words, self-contained

Question patterns to cover:
1. "Is {category} good for {context}?" (direct yes + conditions)
2. "How do {context} teams use {category}?" (top 2-3 use cases)
3. "What's the best {category} tool for {context}?" (top recommendation)
4. "How much does {category} cost for {context}?" (pricing for their scale)
5. "How long does it take to implement {category} for {context}?" (timeline)
6. "What {context}-specific features should I look for?" (requirements)
7. "Does {category} work with {context-specific tool/platform}?" (integration)

### 11. Internal Links Section

H2: `More on {Category}`

Content:
- Link to the "What Is {Category}" definition page
- Link to the "Best {Category} Tools" list
- Link to other use case pages (different context)
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
  "about": {
    "@type": "Thing",
    "name": "{Category} for {Context}"
  },
  "audience": {
    "@type": "Audience",
    "audienceType": "{Context role/industry}"
  },
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

- [ ] Context-specific answer block is 100-150 words and connects category to their context in first sentence
- [ ] Names a challenge unique to their industry/role (not generic)
- [ ] 4-6 use cases specific to the context (not repackaged generic examples)
- [ ] Requirements table contrasts context-specific vs general needs
- [ ] Implementation steps are context-specific (mention their tools, workflows, constraints)
- [ ] Benchmarks use context-specific metrics (not generic SaaS averages)
- [ ] Tool recommendations ranked by context fit, not overall quality
- [ ] FAQ has 5-7 questions with self-contained 50-150 word answers
- [ ] JSON-LD Article schema includes audience type
- [ ] Industry/role terminology used correctly throughout
- [ ] Author credibility ties to this specific context
- [ ] Internal links to 3-5 related pages
- [ ] No banned phrases or corporate jargon

---

## Target Metrics

- **Word count**: 1,800-2,800 words
- **Reading time**: 8-14 minutes
- **Use cases**: 4-6
- **FAQ count**: 5-7 questions
- **Context-specific stats**: 2-4
- **Internal links**: 3-5
- **Refresh cadence**: Semi-annually (industry changes move slower than tools)
