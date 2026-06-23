# Alternatives Page Template

> Page type designed for AI retrieval on "{product} alternatives" queries.
> Captures bottom-of-funnel buyers actively evaluating options. High commercial intent.

---

## Required Structure

### 1. H1: Title

Format: `Best {Incumbent} Alternatives ({Year})` or `{N} {Incumbent} Alternatives for {Use Case}`

Examples:
- "Best HubSpot Alternatives (2026)"
- "7 Hootsuite Alternatives for B2B Social Media"
- "Best Salesforce Alternatives for Growing SaaS Teams"

Rules:
- Always name the incumbent product in the title
- Include year for freshness
- Optional: include count or use case qualifier

### 2. Quick Answer Block

**Place immediately after H1. No preamble.**

Template:
```
**The best {Incumbent} alternatives are {Alt A} (best for {reason}), {Alt B} (best for {reason}), and {Alt C} (best for {reason}).** We compared {N} alternatives across pricing, features, and ease of migration for {ICP description}.
```

Rules:
- Name top 3 alternatives in the first sentence
- Include why someone would look for alternatives (not just "it's expensive")
- This paragraph gets extracted by LLMs

### 3. Section: Why Look for {Incumbent} Alternatives?

H2: `Why Are Teams Switching from {Incumbent}?`

Content:
- 3-5 specific, honest reasons (not generic bashing)
- Each reason: 1-2 sentences with evidence
- Frame as legitimate business needs, not complaints

Example reasons:
- Pricing scaled beyond budget at {tier}
- Missing {specific feature} for {use case}
- Complexity for teams under {size}
- Integration gaps with {tools}
- Contract flexibility needs

### 4. Feature Comparison Matrix (CRITICAL)

**This table is the primary extraction target.**

Format:
```
| Feature | {Incumbent} | {Alt A} | {Alt B} | {Alt C} | {Alt D} |
|---------|-------------|---------|---------|---------|---------|
| {Feature 1} | Yes | Yes | No | Yes | Yes |
| {Feature 2} | Yes | Yes | Yes | No | Yes |
| Pricing from | ${X}/mo | ${Y}/mo | ${Z}/mo | ${W}/mo | ${V}/mo |
| Free tier | No | Yes | Yes | No | Yes |
| Best for | Enterprise | SMB | Mid-market | Enterprise | Startups |
```

Rules:
- Include the incumbent in the comparison (not just alternatives)
- Use checkmarks/Yes/No for feature presence
- Include pricing row
- Include "Best for" row
- 8-12 feature rows for depth

### 5. Per-Alternative Breakdowns

For each alternative, use this H2 structure:

H2: `{N}. {Alternative Name} - Best {Incumbent} Alternative for {Use Case}`

Each breakdown includes:

**Why switch from {Incumbent}**:
- 1-2 sentences on what this alternative does better

**Key differences from {Incumbent}**:
- 3-4 bullet points: specific feature/capability differences

**Pricing comparison**:
- Side-by-side with incumbent pricing
- Highlight cost savings where applicable

**Migration difficulty**: Easy / Moderate / Complex
- One sentence on what migration involves

**Best for**:
- "Best for teams that {specific need} and currently {pain point with incumbent}."

### 6. Section: How to Migrate from {Incumbent}

H2: `How to Switch from {Incumbent}: Migration Guide`

Content:
- Numbered steps for the migration process
- Data export considerations
- Timeline expectations
- Common pitfalls to avoid

### 7. Section: When to Stay with {Incumbent}

H2: `When {Incumbent} Is Still the Best Choice`

Content:
- 2-3 scenarios where the incumbent wins
- Builds credibility through honesty
- Prevents bias perception

### 8. FAQ Section (REQUIRED)

H2: `{Incumbent} Alternatives FAQ`

Question patterns:
1. "What is the best alternative to {Incumbent}?" (top pick + reasoning)
2. "Is {Alt A} better than {Incumbent}?" (comparison answer)
3. "What is the cheapest {Incumbent} alternative?" (price-focused)
4. "Can I migrate from {Incumbent} to {Alt}?" (migration feasibility)
5. "What {Incumbent} alternative is best for {use case}?" (use-case match)
6. "Is {Incumbent} worth the price?" (value assessment)

---

## JSON-LD Schemas Required

### ItemList Schema
```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Best {Incumbent} Alternatives ({Year})",
  "numberOfItems": {count},
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "{Alternative Name}",
      "description": "Best for {use case}"
    }
  ]
}
```

### FAQPage Schema + Article Schema (same as other templates)

---

## Quality Checklist

- [ ] Quick answer names top 3 alternatives with reasoning
- [ ] "Why switch" section has specific, honest reasons (not generic complaints)
- [ ] Feature matrix includes the incumbent alongside alternatives
- [ ] Feature matrix has 8+ rows
- [ ] Each alternative has: key differences, pricing comparison, migration difficulty
- [ ] Migration guide section included
- [ ] "When to stay" section included (credibility builder)
- [ ] FAQ has 5-7 questions
- [ ] Pricing is specific where possible
- [ ] No bias language or affiliate-style copy
- [ ] Honest about both strengths and weaknesses

---

## Target Metrics

- **Word count**: 2,000-3,500 words
- **Alternatives covered**: 5-8
- **Feature matrix rows**: 8-12
- **FAQ count**: 5-7 questions
- **Refresh cadence**: Monthly (pricing and features change)
