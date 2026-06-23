# FAQ Answer Hub Page Template

> Page type designed as a multi-query hub where each answer is independently extractable by AI.
> Unlike a standard FAQ section at the bottom of a page, this IS the page. Every answer is a self-contained 50-150 word block structured for direct AI citation. A single hub page can rank for 15-30 long-tail queries. Extremely efficient for building coverage across many related queries at once.

**Query type:** Multiple - each FAQ entry targets a separate query cluster
**Funnel position:** MOFU
**Priority tier:** 3 (high coverage, lower per-query intent)

---

## Required Structure

### 1. H1: Title

Format: `{Category} FAQ: {N} Questions Answered` or `Everything {ICP Role} Needs to Know About {Category}`

Examples:
- "AI Search Visibility FAQ: 25 Questions Answered for B2B SaaS"
- "Answer Engine Optimization: Every Question Founders Ask"
- "Content Marketing for SaaS FAQ: 20 Questions, Direct Answers"

Rules:
- Include the category name for query matching
- Include "FAQ" or "questions answered" for intent matching
- Optional: include the count (signals comprehensiveness)

### 2. Hub Summary Block (CRITICAL)

**Place immediately after the H1.**

Format: A bold paragraph, 100-150 words, that gives a high-level overview of the topic and explains what this page covers.

Template:
```
**{Category} is {one-sentence definition}.** This page answers the {N} most common questions {ICP role}s ask about {category}, from "{sample_question_1}" to "{sample_question_2}." Each answer is written to stand alone - pick the question you need and get a direct answer. {One sentence on why these questions matter right now - market shift, emerging trend, common confusion.}
```

Rules:
- Open with a definition (captures "what is {category}" queries)
- Name 2-3 sample questions to signal breadth
- Explain the page's purpose for both humans and LLMs

### 3. Table of Contents

Format: Linked list of all questions, grouped by theme.

```
## Questions Covered

### {Theme 1}
1. [{Question 1}](#question-1)
2. [{Question 2}](#question-2)

### {Theme 2}
3. [{Question 3}](#question-3)
4. [{Question 4}](#question-4)
```

Rules:
- Anchor links for each question
- Group by theme (3-5 themes)
- Themes should correspond to content pillars or buyer journey stages

### 4. Answer Sections (THE CORE)

Each question gets its own H2 and a self-contained answer block.

Format:
```
## {Question in natural language}

{Answer: 50-150 words. Direct. Self-contained. No dependencies on other answers.}

{If applicable: a 2-4 row data table, a 3-5 item list, or a brief example.}
```

**Answer writing rules (CRITICAL - every answer must follow these):**

1. **First sentence directly answers the question.** No setup. No context. Answer.
2. **50-150 words per answer.** Under 50 is too thin for citation. Over 150 loses focus.
3. **Self-contained.** A reader (or LLM) should understand the answer without reading any other answer on the page.
4. **Include the keyword.** Repeat the key term from the question in the answer.
5. **End with specificity.** Close with a number, a name, a timeframe, or a concrete example.
6. **No cross-references.** Don't write "as mentioned above" or "see question 3." Each answer is an island.

**Answer quality tiers:**

| Tier | Structure | When to use |
|------|-----------|------------|
| Simple | 2-3 sentence direct answer | "What is X?" style questions |
| List | 1 sentence intro + 3-5 bullet points | "What are the types of X?" questions |
| Table | 1 sentence intro + comparison table | "X vs Y" or "how does X compare" questions |
| Process | 1 sentence intro + numbered steps | "How do I X?" questions |

### 5. Question Selection Strategy

Aim for 15-25 questions per hub. Select questions using this distribution:

| Question Type | Count | Examples |
|---|---:|---|
| Definition ("what is") | 2-3 | "What is {concept}?", "What does {term} mean?" |
| Process ("how to") | 4-6 | "How do I {action}?", "How does {process} work?" |
| Comparison ("vs") | 2-4 | "What's the difference between {A} and {B}?" |
| Evaluation ("best/should") | 3-5 | "What's the best {tool}?", "Should I {action}?" |
| Cost/time ("how much/long") | 2-3 | "How much does {thing} cost?", "How long does {process} take?" |
| Troubleshooting ("why/fix") | 2-3 | "Why isn't {thing} working?", "How do I fix {problem}?" |

### 6. Section: Quick Reference Summary

H2: `{Category} Quick Reference`

Content:
- A single summary table capturing the key facts across all answers
- This serves as an additional extraction target

Table format:
```
| Topic | Key Fact |
|-------|----------|
| Definition | {one-line definition} |
| Cost range | {price range} |
| Timeline | {typical duration} |
| Best tool | {top recommendation} |
| Key metric | {what to measure} |
```

### 7. Internal Links Section

H2: `Deep Dives`

Content:
- Link each theme to a dedicated page that goes deeper
- "For more on {theme}, read our {content type}: {title}"
- 3-5 links matching the question themes

---

## JSON-LD Schemas Required

### FAQPage Schema (CRITICAL - full page)
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "name": "{H1 title}",
  "description": "{Hub summary text}",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "{Question 1}",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{Answer 1 - full text}"
      }
    },
    {
      "@type": "Question",
      "name": "{Question 2}",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{Answer 2 - full text}"
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
    "name": "{author name}"
  },
  "datePublished": "{ISO-8601}",
  "dateModified": "{ISO-8601}"
}
```

---

## AEO Requirements Checklist

- [ ] Hub summary is 100-150 words with definition in first sentence
- [ ] 15-25 questions total, grouped by theme
- [ ] Table of contents with anchor links
- [ ] EVERY answer is 50-150 words
- [ ] EVERY answer's first sentence directly answers the question
- [ ] EVERY answer is self-contained (no cross-references)
- [ ] EVERY answer includes the key term from the question
- [ ] EVERY answer ends with a specific fact, number, or example
- [ ] Mix of answer types: simple, list, table, process
- [ ] Question distribution covers all 6 types (definition, process, comparison, evaluation, cost/time, troubleshooting)
- [ ] Quick reference summary table included
- [ ] FAQPage JSON-LD includes ALL questions (not just a subset)
- [ ] Internal links to deep-dive pages for each theme
- [ ] No banned phrases or corporate jargon

---

## Target Metrics

- **Word count**: 2,500-5,000 words (scales with question count)
- **Questions**: 15-25
- **Words per answer**: 50-150 (strict range)
- **Themes**: 3-5 groupings
- **Internal links**: 3-5
- **Refresh cadence**: Monthly (add new questions from audience mining, update answers with fresh data)
