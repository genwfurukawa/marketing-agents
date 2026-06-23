# Statistics / Research Page Template

> Page type designed for AI retrieval on "{topic} statistics" and "{topic} data {year}" queries.
> Statistics pages get cited constantly because they contain numbers, facts, and datasets that LLMs quote directly.
> These pages also attract backlinks, which further strengthens entity authority.

---

## Required Structure

### 1. H1: Title

Format: `{N} {Topic} Statistics You Need to Know ({Year})` or `{Topic} Statistics and Trends ({Year})`

Examples:
- "47 LinkedIn Marketing Statistics You Need to Know (2026)"
- "AI Search Adoption Statistics and Trends (2026)"
- "B2B Content Marketing Statistics: The Data That Matters (2026)"

Rules:
- Include the year (this page MUST be updated annually)
- Include a count of statistics if possible (signals comprehensiveness)
- Use the exact topic phrase buyers search

### 2. Key Findings Block (CRITICAL)

**Place immediately after H1. No preamble.**

Template:
```
**Key findings from our research on {topic}:**
- {Stat 1 - the most surprising or impactful finding}
- {Stat 2}
- {Stat 3}
- {Stat 4}
- {Stat 5}

*Last updated: {Month Year}. Sources: {N} reports from {source types}.*
```

Rules:
- 5 bullet points, each a complete statistic with context
- Lead with the most citation-worthy stat
- Include the "last updated" date
- LLMs frequently extract this summary block

### 3. Stat Sections by Category

Organize statistics into 4-6 themed sections. Each section follows this format:

H2: `{Topic} {Category} Statistics`

For each statistic within the section:

```
### {Statistic as a headline}

{Number or percentage in bold.} {One sentence of context.} {One sentence on why this matters for {ICP}.}

**Source:** {Publication Name}, {Year}. [{Link text}]({URL})
```

Example:
```
### AI Search Adoption Rate

**87% of B2B buyers now use AI assistants during purchase research.** This represents a 120% increase from 2024, when the figure was under 40%. For B2B SaaS companies, this means your buyers are finding (or not finding) you through AI before they ever visit your website.

**Source:** Gartner B2B Buying Survey, 2025.
```

Rules:
- Every statistic MUST have a source citation
- Each stat gets its own H3 heading (for extraction)
- Include context (not just the number)
- Include "why it matters" for the ICP
- Bold the key number in each stat

### 4. Section: Methodology

H2: `Methodology: How We Compiled These Statistics`

Content:
- Number of sources reviewed
- Types of sources (surveys, reports, platform data)
- Date range of data
- Any limitations or caveats

This section builds E-E-A-T trust. LLMs weight content higher when methodology is transparent.

### 5. Section: Data Sources

H2: `Data Sources`

Content:
- Numbered list of all sources cited
- For each: publication name, report title, year, URL
- Organized by type (industry reports, platform data, surveys, academic research)

### 6. Section: Trends and Predictions

H2: `{Topic} Trends for {Year + 1}`

Content:
- 3-5 trend predictions based on the data
- Each prediction: data-backed reasoning, not speculation
- Frame as "what the data suggests" not "we predict"

### 7. Section: Key Takeaways

H2: `What These {Topic} Statistics Mean for {ICP}`

Content:
- 3-5 actionable takeaways
- Each: statistic reference + what to do about it
- Directed at the ICP with "you" language

### 8. FAQ Section (REQUIRED)

H2: `{Topic} Statistics FAQ`

Question patterns:
1. "What percentage of {audience} use {topic}?" (top stat)
2. "How fast is {topic} growing?" (growth rate)
3. "What are the latest {topic} statistics?" (recency signal)
4. "How effective is {topic} for {use case}?" (ROI stat)
5. "What is the average {metric} for {topic}?" (benchmark)

---

## JSON-LD Schemas Required

### Dataset Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "name": "{Topic} Statistics ({Year})",
  "description": "{Key findings summary}",
  "datePublished": "{ISO-8601}",
  "dateModified": "{ISO-8601}",
  "creator": {
    "@type": "Organization",
    "name": "{Company}"
  },
  "temporalCoverage": "{Year}"
}
```

### FAQPage Schema + Article Schema

---

## Quality Checklist

- [ ] Key findings block has 5 bullet points with specific numbers
- [ ] EVERY statistic has a source citation with publication name and year
- [ ] Statistics organized into 4-6 themed sections
- [ ] Each stat has its own H3 heading
- [ ] "Last updated" date prominently displayed
- [ ] Methodology section explains data sources
- [ ] Data sources listed with full citations
- [ ] Trends section with data-backed predictions
- [ ] Actionable takeaways for ICP
- [ ] FAQ has 5-7 questions
- [ ] No statistics without sources
- [ ] Numbers are bold for scannability

---

## Target Metrics

- **Word count**: 2,500-5,000 words (scales with stat count)
- **Statistics count**: 20-50 individual data points
- **Sources cited**: 10-25 unique sources
- **Sections**: 4-6 themed categories
- **FAQ count**: 5-7 questions
- **Refresh cadence**: Monthly (add new stats, update sources)

---

## Refresh Protocol

This page type requires the most frequent updates of any page type.

1. **Monthly**: Check for new reports and surveys. Add new statistics.
2. **Quarterly**: Update any statistics that have newer versions available.
3. **Annually**: Full rewrite with new year in title. Archive previous year's version.
4. **Always**: Update the "Last updated" date whenever any change is made.
