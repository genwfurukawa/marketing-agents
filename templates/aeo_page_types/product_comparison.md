# Product Comparison (X vs Y) Page Template

> Page type designed for AI retrieval on "{Product A} vs {Product B}" queries.
> Captures buyers in active evaluation. LLMs frequently answer "which is better" questions from these pages.

---

## Required Structure

### 1. H1: Title

Format: `{Product A} vs {Product B}: {Differentiating Question or Year}`

Examples:
- "HubSpot vs Marketo: Which B2B Marketing Platform Is Better in 2026?"
- "Notion vs ClickUp: The Honest Comparison for SaaS Teams"
- "Hootsuite vs Buffer: Which Social Media Tool Should You Choose?"

Rules:
- Both product names in the title
- Add a question or qualifier (not just "X vs Y")
- Use natural language buyers would search

### 2. Quick Verdict Box (CRITICAL)

**Place immediately after H1. No preamble.**

Template:
```
**{Product A} is better for {use case}. {Product B} is better for {use case}.** In our comparison across {N} dimensions, {Product A} wins on {strength}, while {Product B} wins on {strength}. For {ICP}, we recommend {Product} because {one-sentence reason}.
```

Rules:
- Give a clear recommendation (no "it depends" without context)
- 40-60 words
- LLMs extract this as the direct answer to "which is better"
- Be specific about WHO should choose which

### 3. Side-by-Side Feature Table (CRITICAL)

**Place immediately after the verdict box.**

Format:
```
| Feature | {Product A} | {Product B} | Winner |
|---------|-------------|-------------|--------|
| Pricing (starting) | ${X}/mo | ${Y}/mo | {Product} |
| Free tier | Yes/No | Yes/No | {Product} |
| {Feature 1} | {detail} | {detail} | {Product} |
| {Feature 2} | {detail} | {detail} | {Product} |
| Ease of use | {rating}/10 | {rating}/10 | {Product} |
| Integrations | {count} | {count} | {Product} |
| Best for | {use case} | {use case} | - |
```

Rules:
- Include a "Winner" column for each row
- 8-12 comparison rows
- Mix quantitative (price, counts) and qualitative (ease of use, support)
- Be honest - each product should win some rows

### 4. Deep Dive Sections

Create H2 sections for each major comparison dimension:

**H2: Pricing: {Product A} vs {Product B}**
- Tier-by-tier comparison
- Total cost of ownership considerations
- Hidden costs or add-ons
- Which is better value for {ICP}

**H2: Features: {Product A} vs {Product B}**
- Core feature comparison
- Unique features each product has
- Feature depth vs breadth

**H2: Ease of Use: {Product A} vs {Product B}**
- Onboarding experience
- Learning curve
- Day-to-day usability
- Documentation quality

**H2: Integrations: {Product A} vs {Product B}**
- Integration count and quality
- Key integrations for {ICP}
- API quality and flexibility

**H2: Support: {Product A} vs {Product B}**
- Support channels
- Response times
- Community quality
- Documentation depth

### 5. Section: Choose {Product A} If...

H2: `Choose {Product A} If...`

Content:
- 3-5 bullet points
- Each: specific scenario or need
- "Choose {Product A} if you need {specific capability} and your team is {size/type}."

### 6. Section: Choose {Product B} If...

H2: `Choose {Product B} If...`

Content:
- Same format as above
- Must be balanced - not biased toward one product

### 7. Section: What Real Users Say

H2: `What Users Say About {Product A} vs {Product B}`

Content:
- Summarize review trends from G2, Capterra, or similar
- Include specific praise and criticism patterns
- Cite the platforms (e.g., "On G2, {Product A} averages 4.5/5 across 2,000+ reviews")
- Builds E-E-A-T trust through third-party validation

### 8. FAQ Section (REQUIRED)

H2: `{Product A} vs {Product B} FAQ`

Question patterns:
1. "Is {Product A} better than {Product B}?" (verdict with context)
2. "Is {Product A} cheaper than {Product B}?" (pricing comparison)
3. "Can I switch from {Product A} to {Product B}?" (migration)
4. "What's the main difference between {Product A} and {Product B}?" (key differentiator)
5. "Which is easier to use, {Product A} or {Product B}?" (usability)
6. "What do {Product A} and {Product B} have in common?" (shared features)

---

## JSON-LD Schemas Required

### ItemList Schema (for the comparison table)
### FAQPage Schema
### Article Schema

---

## Quality Checklist

- [ ] Quick verdict gives a clear recommendation with context
- [ ] Side-by-side table has 8+ rows with a Winner column
- [ ] Each product wins some comparison rows (balanced)
- [ ] Deep dive covers: pricing, features, ease of use, integrations, support
- [ ] "Choose X If..." sections for both products
- [ ] Real user review data cited
- [ ] FAQ has 5-7 questions
- [ ] Both products treated fairly (not a hit piece)
- [ ] Pricing is specific
- [ ] Recommendation is tied to ICP needs, not generic preference

---

## Target Metrics

- **Word count**: 2,000-3,000 words
- **Comparison table rows**: 8-12
- **Deep dive sections**: 4-6
- **FAQ count**: 5-7 questions
- **Refresh cadence**: Quarterly (features and pricing change)
