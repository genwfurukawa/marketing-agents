# Glossary / Knowledge Base Page Template

> Page type designed for AI retrieval on term-specific queries and "{category} glossary" searches.
> Glossary pages create hundreds of short definition entries ideal for AI extraction.
> Each term is a standalone retrieval node. Companies dominating AI search often have large glossary libraries.

---

## Required Structure

### 1. H1: Title

Format: `{Category} Glossary: {N} Key Terms Defined` or `The Complete {Category} Glossary`

Examples:
- "AI Search Marketing Glossary: 30 Key Terms Defined"
- "The Complete B2B SaaS Marketing Glossary"
- "Answer Engine Optimization Glossary: Every Term You Need to Know"

Rules:
- Include the category name
- Include a count if possible
- Signal comprehensiveness

### 2. Introduction Block

**Brief - 2-3 sentences max.**

Template:
```
**This glossary covers the {N} essential terms in {category}.** Each definition is written for {ICP role} - no jargon, practical context, and real examples. Use the alphabetical index below to jump to any term.
```

### 3. Alphabetical Jump Links

Format:
```
**Jump to:** [A](#a) | [B](#b) | [C](#c) | [D](#d) | ... | [Z](#z)
```

Rules:
- Only include letters that have entries
- Each letter links to an anchor

### 4. Per-Term Entries (CRITICAL - This Is the Core)

For EACH term, use this exact structure:

```
## {Term Name}

**{Term Name} is {definition in 40-60 words}.** {Also known as: {synonym 1}, {synonym 2}.}

**Example:** {One specific, concrete example of this term in practice.}

**Why it matters:** {One sentence connecting this term to business outcomes for {ICP}.}

**Related terms:** [{Related Term 1}](#related-term-1), [{Related Term 2}](#related-term-2)
```

Rules for each entry:
- **Definition**: 40-60 words. Starts with "{Term} is..." format. Self-contained.
- **Also known as**: Include synonyms and abbreviations. Skip if none exist.
- **Example**: Must be concrete and specific, not abstract.
- **Why it matters**: Connects to business value for the ICP.
- **Related terms**: Cross-link to other glossary entries. Builds internal linking signals.

### 5. Grouping

If the glossary has 20+ terms, group alphabetically with letter headers:

```
## A

### Answer Engine Optimization (AEO)
{entry}

### AI Citation
{entry}

## B

### Brand Entity
{entry}
```

For smaller glossaries (under 20 terms), group thematically:

```
## Core Concepts
### {Term}
### {Term}

## Tools and Platforms
### {Term}
### {Term}

## Metrics and Measurement
### {Term}
### {Term}
```

### 6. Section: How to Use This Glossary

H2: `How to Use This {Category} Glossary`

Content:
- 2-3 sentences on who this glossary is for
- Suggest bookmarking for reference
- Note the update cadence

### 7. Section: Further Reading

H2: `Further Reading`

Content:
- Links to "What Is" pages for key terms
- Links to related guides and tutorials
- Links to statistics pages for data context

### 8. FAQ Section (OPTIONAL but recommended)

H2: `{Category} Glossary FAQ`

Question patterns:
1. "What is {most important term}?" (definition)
2. "What's the difference between {term A} and {term B}?" (common confusion)
3. "What {category} terms should I know?" (overview)

---

## JSON-LD Schema Required

### DefinedTermSet Schema
```json
{
  "@context": "https://schema.org",
  "@type": "DefinedTermSet",
  "name": "{Category} Glossary",
  "description": "{Introduction block text}",
  "hasDefinedTerm": [
    {
      "@type": "DefinedTerm",
      "name": "{Term}",
      "description": "{40-60 word definition}"
    }
  ]
}
```

---

## Quality Checklist

- [ ] Every term definition is 40-60 words and starts with "{Term} is..."
- [ ] Every definition is self-contained (extractable without context)
- [ ] Every term has: definition, example, why it matters, related terms
- [ ] Related terms cross-link to other entries in the glossary
- [ ] Alphabetical jump links present (if 20+ terms)
- [ ] DefinedTermSet schema includes all terms
- [ ] No jargon within definitions (definitions explain jargon, not use it)
- [ ] Each entry has a concrete, specific example
- [ ] "Also known as" included where synonyms exist
- [ ] Further reading links to deeper content

---

## Target Metrics

- **Term count**: 15-50 terms (sweet spot for depth vs utility)
- **Words per definition**: 40-60 words
- **Cross-links per term**: 2-3 related terms
- **Total word count**: 1,500-5,000 words (scales with term count)
- **FAQ count**: 3-5 questions (optional)
- **Refresh cadence**: Quarterly (add new terms, update definitions)

---

## Scaling Strategy

Glossary pages compound over time. Strategy for growth:

1. **Launch**: 15-20 core terms for the category
2. **Month 2-3**: Add 5-10 terms based on search data and AI query patterns
3. **Month 4-6**: Expand each high-traffic term into its own "What Is" page
4. **Ongoing**: Add new terms as the category evolves

Each glossary entry can become a seed for a full "What Is" definition page. The glossary is the index; the definition pages are the depth.
