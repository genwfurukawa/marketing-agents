# "What Is" Definition Page Template

> Page type designed for AI retrieval on "what is {concept}" queries.
> LLMs extract the definition block directly. This page type has the highest citation rate for informational queries.

---

## Required Structure

### 1. H1: Title

Format: `What Is {Concept}? {Qualifier for B2B SaaS}`

Examples:
- "What Is Answer Engine Optimization? The Complete Guide for B2B SaaS"
- "What Is Customer Data Infrastructure? Why It Matters for Growth Teams"

Rules:
- Include the concept name exactly as buyers would search it
- Add a qualifier that signals depth and relevance to ICP
- Keep under 70 characters for SERP display

### 2. Definition Block (CRITICAL - This Is What Gets Cited)

**Place immediately after the H1. No preamble. No setup.**

Format: A single bold paragraph, 40-60 words, that directly defines the concept.

Template:
```
**{Concept} is {clear definition in plain language}.** {One sentence on why it matters.} {One sentence on who it's for or what problem it solves.}
```

Rules:
- First sentence must be a direct "X is Y" definition
- No jargon in the definition itself
- Self-contained - makes sense without reading anything else on the page
- This paragraph is the #1 extraction target for LLMs

### 3. Author Credibility Line

Format: One paragraph establishing why the author is credible on this topic.

Template:
```
I'm {Name}. I {role/credential relevant to this topic}. {One sentence of specific experience with this concept.}
```

Rules:
- Must include real credentials (not generic)
- Ties the author directly to the concept being defined
- Builds E-E-A-T Experience signal

### 4. Section: Why Does {Concept} Matter?

H2: `Why Does {Concept} Matter for {ICP}?` or `Why Should {ICP Role} Care About {Concept}?`

Content:
- 2-3 paragraphs explaining business impact
- Include at least 1 statistic with source citation
- Use "you" language directed at the ICP
- Frame as old way vs new way where appropriate

### 5. Section: How Does {Concept} Work?

H2: `How Does {Concept} Work?` or `How {Concept} Works in Practice`

Content:
- Numbered steps OR process explanation
- Each step: 1-2 sentences max
- Include a practical example after the steps
- If applicable, include a simple diagram description

### 6. Section: {Concept} vs {Related Concept}

H2: `{Concept} vs {Related Concept}: What's the Difference?`

Content:
- Comparison table with 5-8 dimensions
- One paragraph summary of when to use each
- This section captures comparison queries that include this concept

Table format:
```
| Dimension | {Concept} | {Related Concept} |
|-----------|-----------|-------------------|
| Primary goal | ... | ... |
| Best for | ... | ... |
| Key metric | ... | ... |
```

### 7. Section: Examples

H2: `{Concept} Examples` or `Examples of {Concept} in Practice`

Content:
- 3-5 real-world examples with company names (where possible)
- Each example: company name, what they did, result
- Use bullet points or short paragraphs
- Include both well-known and emerging examples

### 8. Section: Related Tools

H2: `{Concept} Tools and Platforms` or `Best {Concept} Tools`

Content:
- Brief list of 5-8 tools relevant to this concept
- For each: name, one-line description, best for
- This section creates entity co-occurrence signals
- Link to the full "Best Tools" page if one exists

### 9. Section: How to Get Started

H2: `How to Get Started with {Concept}` or `{Concept}: Getting Started Guide`

Content:
- 3-5 actionable steps
- Each step: clear action + expected outcome
- Progressive difficulty (easy first)
- Include specific tools or resources for each step

### 10. FAQ Section (REQUIRED)

H2: `{Concept} FAQ` or `Frequently Asked Questions About {Concept}`

Content:
- 5-7 questions in natural language (how buyers actually ask)
- Each answer: 2-4 sentences, direct, self-contained
- Answers must make sense without reading the rest of the page
- Include the concept name in each answer for extraction

Question patterns to cover:
1. "What is {concept}?" (restate the definition)
2. "Why is {concept} important?" (business value)
3. "How do I implement {concept}?" (practical steps)
4. "What's the difference between {concept} and {related}?" (comparison)
5. "{Concept} vs {alternative approach}?" (positioning)
6. "How much does {concept} cost?" (if applicable)
7. "What are the best {concept} tools?" (tool recommendations)

### 11. Internal Links Section

H2: `Further Reading` or `Related Guides`

Content:
- 3-5 links to related pages on the same site
- Each link: title + one-sentence description
- Builds topical authority cluster signals

---

## JSON-LD Schemas Required

### DefinedTerm Schema
```json
{
  "@context": "https://schema.org",
  "@type": "DefinedTerm",
  "name": "{Concept}",
  "description": "{40-60 word definition from the definition block}",
  "inDefinedTermSet": {
    "@type": "DefinedTermSet",
    "name": "{Category} Glossary"
  }
}
```

### FAQPage Schema
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "{question}",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{answer}"
      }
    }
  ]
}
```

### Article Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{H1 title}",
  "description": "{meta description}",
  "author": {
    "@type": "Person",
    "name": "{author name}",
    "url": "{author page URL}"
  },
  "datePublished": "{ISO-8601}",
  "dateModified": "{ISO-8601}"
}
```

---

## Quality Checklist

- [ ] Definition block is 40-60 words and starts with "{Concept} is..."
- [ ] Definition is self-contained (extractable without context)
- [ ] At least 1 statistic with source citation
- [ ] Comparison table with 5+ dimensions
- [ ] 3-5 real examples with outcomes
- [ ] FAQ has 5-7 natural language questions
- [ ] FAQ answers are self-contained (2-4 sentences each)
- [ ] All three JSON-LD schemas present
- [ ] Author credibility line with real credentials
- [ ] Internal links to 3-5 related pages
- [ ] No banned phrases or corporate jargon
- [ ] Uses "you" language directed at ICP
- [ ] Every H2 is a question or action-oriented

---

## Target Metrics

- **Word count**: 1,500-2,500 words
- **Reading time**: 7-12 minutes
- **FAQ count**: 5-7 questions
- **Statistics**: 2-4 cited data points
- **Internal links**: 3-5
- **Refresh cadence**: Quarterly (update stats and examples)
