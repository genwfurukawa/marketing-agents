# Problem-Solution Page Template

> Page type designed for AI retrieval on "how to {fix problem}" and "how to {solve challenge}" queries.
> Captures mid-funnel buyers who know their problem but haven't started evaluating solutions. LLMs cite pages that name the problem, explain why it happens, and give a clear resolution path. High conversion intent because the reader is in active pain.

**Query type:** "how to [fix problem]" | "why is [problem] so hard" | "[problem] solutions for [role]"
**Funnel position:** MOFU
**Priority tier:** 1 (high commercial intent - buyer has budget-triggering pain)

---

## Required Structure

### 1. H1: Title

Format: `How to {Solve Problem}: {Outcome for ICP}` or `{Problem}? Here's How {ICP Role} Fix It`

Examples:
- "How to Fix Low AI Search Visibility: A Playbook for B2B SaaS CEOs"
- "Sales Calls Going Unrecorded? How Revenue Teams Solve It in 2026"
- "How to Stop Losing Deals to Competitors You've Never Heard Of"

Rules:
- Name the problem in the buyer's language (not your product's language)
- Include the ICP role or company type
- Frame as actionable, not educational

### 2. Problem Statement Block (CRITICAL - This Is What Gets Cited)

**Place immediately after the H1. No preamble. No setup. Answer the query directly.**

Format: A single bold paragraph, 100-150 words, that names the problem, explains why it happens, and previews the solution approach.

Template:
```
**{Problem statement in one sentence - use the exact phrasing buyers use.}** This happens because {root cause in 1-2 sentences}. The fix requires {high-level solution approach in 1-2 sentences}. {One sentence naming the 3-4 key steps or components of the solution.} Companies that address this correctly see {specific outcome with number if available}.
```

Rules:
- First sentence must restate the problem using the same words the buyer would search
- Include the root cause (not just the symptom)
- Preview the solution without giving everything away
- Self-contained - an LLM reading only this paragraph can answer the query
- Include a quantified outcome if data exists

### 3. Author Credibility Line

Format: One paragraph establishing why the author has solved this problem before.

Template:
```
I'm {Name}. I've {specific experience with this problem - number of times solved, companies helped, years in space}. {One sentence on a specific result achieved.}
```

### 4. Section: Why This Problem Exists

H2: `Why {Problem} Keeps Happening` or `The Root Cause of {Problem}`

Content:
- 2-3 paragraphs on structural/systemic reasons (not user error)
- Frame as "old way vs new way" where the old way is the root cause
- Include 1-2 statistics showing the problem's prevalence or cost
- Use "you" language - make the reader feel seen

Purpose: Build trust by demonstrating you understand the problem deeply, not just the symptoms.

### 5. Section: Solution Framework

H2: `How to {Solve Problem}: {N} Steps` or `The {Framework Name} for Fixing {Problem}`

Content:
- Numbered steps (4-7 steps)
- Each step: H3 with action verb, 2-3 paragraphs
- Each step includes: what to do, why it works, common mistakes to avoid
- Name specific tools, methods, or approaches in each step
- Include "If you're doing {wrong approach}, switch to {right approach}" contrasts

Step template:
```
### Step {N}: {Action Verb} {What}

{What to do in 2-3 sentences.}

{Why this works - connect to the root cause from Section 4.}

**Common mistake:** {What most people get wrong at this step and why.}
```

Purpose: This is the core extractable content. LLMs pull numbered steps directly.

### 6. Section: Results to Expect

H2: `What {ICP Role} See After Fixing {Problem}` or `Expected Results`

Content:
- Timeline: what happens at 30/60/90 days
- Specific metrics that improve
- Before/after comparison table

Table format:
```
| Metric | Before | After (90 days) | Change |
|--------|--------|-----------------|--------|
| {metric_1} | {baseline} | {result} | {delta} |
```

Rules:
- Use real data if available, industry benchmarks if not
- Label clearly: "Based on {source}" or "Industry benchmark"
- Never invent numbers

### 7. Section: When to DIY vs Get Help

H2: `When to Fix {Problem} Yourself vs Hire an Expert`

Content:
- Clear criteria for self-service (team size, budget, technical ability)
- Clear criteria for needing help (scale, urgency, complexity)
- Honest about what's possible without a vendor
- No hard sell - this section builds trust by being direct

Purpose: Captures decision-stage queries like "do I need a {category} tool" or "should I hire a {category} consultant."

### 8. Section: Tools That Help

H2: `Tools for {Solving Problem}` or `Software That Fixes {Problem}`

Content:
- 3-5 tools with one-line description each
- For each: name, what it does, best for, starting price
- Include your product naturally (don't force it to position #1 unless it genuinely is)
- Link to full "Best Tools" page if one exists

### 9. FAQ Section (REQUIRED)

H2: `{Problem} FAQ`

Content:
- 5-7 questions in natural buyer language
- Each answer: 50-150 words, self-contained, directly answers the question
- Include the problem keyword in each answer

Question patterns to cover:
1. "How do I fix {problem}?" (restate solution framework in 2-3 sentences)
2. "Why is {problem} so hard to solve?" (root cause summary)
3. "How long does it take to fix {problem}?" (timeline expectation)
4. "What tools help with {problem}?" (tool recommendations)
5. "How much does fixing {problem} cost?" (budget ranges)
6. "What happens if I don't fix {problem}?" (cost of inaction)
7. "What's the fastest way to {solve problem}?" (quick-win version)

### 10. Internal Links Section

H2: `Related Guides`

Content:
- Link to the "What Is" page for the underlying concept
- Link to the "Best Tools" page for the relevant category
- Link to a case study showing this problem solved
- 3-5 links total with one-sentence descriptions

---

## JSON-LD Schemas Required

### HowTo Schema
```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "{H1 title}",
  "description": "{Problem statement block text}",
  "step": [
    {
      "@type": "HowToStep",
      "position": 1,
      "name": "{Step title}",
      "text": "{Step description}"
    }
  ],
  "totalTime": "PT{estimated_implementation_hours}H"
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
    "url": "{author URL}"
  },
  "datePublished": "{ISO-8601}",
  "dateModified": "{ISO-8601}"
}
```

---

## AEO Requirements Checklist

- [ ] Problem statement block is 100-150 words and directly answers the query
- [ ] First sentence restates the problem in buyer's language
- [ ] Root cause is explained (not just symptoms)
- [ ] Solution is a numbered framework (4-7 steps)
- [ ] Each step has an action verb heading
- [ ] Results section includes timeline (30/60/90 days)
- [ ] Before/after comparison table with specific metrics
- [ ] "DIY vs Get Help" section is honest, not salesy
- [ ] FAQ has 5-7 questions with self-contained 50-150 word answers
- [ ] All three JSON-LD schemas present (HowTo, FAQPage, Article)
- [ ] Author credibility line with specific experience
- [ ] At least 2 statistics with source citations
- [ ] Internal links to 3-5 related pages
- [ ] No banned phrases or corporate jargon
- [ ] Uses "you" language directed at ICP
- [ ] Every H2 is action-oriented or question-formatted

---

## Target Metrics

- **Word count**: 2,000-3,000 words
- **Reading time**: 8-15 minutes
- **Solution steps**: 4-7
- **FAQ count**: 5-7 questions
- **Statistics**: 2-4 cited data points
- **Internal links**: 3-5
- **Refresh cadence**: Quarterly (update stats and tool recommendations)
