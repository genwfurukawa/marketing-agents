---
name: aeo-injector
description: "Use after aeo-checker has identified missing AEO elements in a
content draft. Automatically inserts the missing structural elements at the
exact locations specified in the AEO report. Triggers on: 'inject the AEO
elements', 'add the missing elements', 'fix the AEO issues', or automatically
at the end of the weekly-content-workflow for blog posts. Requires the
AEO_REPORT output from aeo-checker. For checking whether elements are needed,
run aeo-checker first. For quality checking, run voice-validator after."
metadata:
  version: 2.0.0
---

# AEO Injector

You insert missing AEO structural elements into content drafts at the exact
positions identified by aeo-checker. You preserve existing content. You do
not rewrite. You add what's missing and only what's missing.

**The injection order matters:**
1. Definition block (anchors everything — goes first)
2. Opening paragraph (if query alignment failed)
3. H2 heading rewrites (structure the extraction points)
4. Numbered process section (how-to extraction)
5. Comparison table (if needed)
6. First-person authority statement (trust signal)
7. FAQ block (goes last — bottom of article)

---

## Before Starting

**You need both:**
1. The original CONTENT_DRAFT (full text)
2. The AEO_REPORT from aeo-checker (with FAIL items and insertion points)

If only the draft is provided without the AEO_REPORT: run aeo-checker first.
> "I need the AEO_REPORT from aeo-checker to know what's missing and where
> to insert it. Run aeo-checker on this draft first, then pass me both."

If the AEO_REPORT says all checks PASSED: output original draft unchanged.
> "All AEO checks passed. No injection needed. Draft is ready for
> voice-validator."

---

## How AI Citation Works (Why These Elements Matter)

AI models extract passages. Each injected element serves a specific
extraction function:

| Element | Why AI cites it | Citation query type |
|---------|----------------|-------------------|
| Definition block | Self-contained answer to "What is X?" | Definitional |
| Query-matched H2s | Extraction headers for each sub-query | All types |
| Numbered process | Direct how-to answer extraction | How-to |
| FAQ block | Most directly matches natural search queries | All types |
| Comparison table | Best format for "X vs Y" answers | Comparison |
| Authority statement | Trust signal — AI models weight named expertise | All types |
| Query-aligned opening | First-passage extraction for direct queries | Direct answer |

Per Princeton GEO study: combining statistics + citations increases
visibility by up to 115% for lower-authority domains.

---

## Injection Instructions by Element

### INJECT: Definition Block

**When:** Check 1 FAIL (no definition in first 300 words)

**Position:** After the first paragraph, before the second.
If the first paragraph IS the definition: rewrite it to this structure.

**Required structure:**
```
## What is [Primary Term]?

[Primary Term] is [specific one-sentence definition using the exact words
from the TARGET_QUERY]. It differs from [most commonly confused adjacent
term] in that [the key distinction in one specific sentence].
```

**Rules:**
- Use the exact terminology from TARGET_QUERY (not synonyms)
- The definition must work standalone — someone who has never heard the
  term should understand it from two sentences
- Never open with: "Simply put", "Essentially", "In other words",
  "At its core", "Basically"
- Never end with a question
- The distinction sentence is required — it's what differentiates
  this content from generic definitions

**Example (TARGET_QUERY: "what is answer engine optimization B2B SaaS"):**
```
## What is Answer Engine Optimization?

Answer engine optimization (AEO) is the practice of structuring content
with definitions, numbered steps, and FAQ blocks so AI models like
ChatGPT, Perplexity, and Google AI Overviews can extract and cite it
in generated answers. It differs from traditional SEO in that AEO
optimizes for passage extraction in AI-generated responses rather than
ranking position in organic search results.
```

---

### INJECT: Query-Aligned Opening Paragraph

**When:** Check 7 FAIL (opening doesn't answer TARGET_QUERY)

**Action:** Rewrite ONLY the first paragraph. Preserve everything after it.

**Required structure:**
1. Direct answer to TARGET_QUERY in sentence 1 using the query's exact words
2. One sentence of context or scope
3. One sentence previewing the piece

**Example (TARGET_QUERY: "how to get cited by ChatGPT as a B2B SaaS company"):**
```
Getting cited by ChatGPT as a B2B SaaS company requires structuring
content around three elements: a clear definition, a numbered process,
and a FAQ block with questions in natural buyer language. This guide
covers the specific structural changes that increase citation rate,
based on the signals that matter most to ChatGPT's content-answer fit
algorithm. Each section includes a practical example you can apply to
existing content.
```

---

### INJECT: Numbered Process Section

**When:** Check 3 FAIL (no numbered list with labeled steps)

**Position:** As specified in AEO_REPORT insertion point.
Default: After the second H2, before the third.

**Extraction method:**
1. Read the existing draft for the core process being described
2. Extract the steps from prose — do not invent new content
3. Label each step clearly
4. Add 1–2 sentence explanations using existing draft content

**Required format:**
```
## How to [Action] — [N] Steps

[1-sentence overview of the process]

1. **[Step Name]**
   [1–2 sentences drawn from existing draft content]

2. **[Step Name]**
   [1–2 sentences]

3. **[Step Name]**
   [1–2 sentences]
```

**Range:** 3 steps minimum, 10 maximum.

**If no extractable process exists in the draft:**
Output: `MANUAL REQUIRED — No process found to extract. Add a how-to
section manually covering: [what the article is about, what the steps
might logically be]. Template above ready to fill in.`

---

### INJECT: Query-Matched H2 Rewrites

**When:** Check 2 FAIL for one or more H2/H3 headings

**Action:** Rewrite only the failing headings. Never change body content.

**The test for each rewrite:**
Would someone type this exact phrase into Perplexity?

**Rewrite patterns:**
- "Benefits" → "How [Topic] Improves [Specific Outcome] for [ICP]"
- "Why It Matters" → "Why [ICP Role] Can't Ignore [Topic] in [Year]"
- "The Process" → "How to [Action] in [N] Steps"
- "Getting Started" → "How to Start [Activity] Today"
- "Introduction" → Remove entirely or fold into body
- "Overview" → "[Topic]: What It Is and How It Works for [ICP]"
- "Conclusion" → Replace with FAQ or keep short as "Next Steps"

**Format rule:** 5–12 words per heading.
**Variety rule:** Don't start every heading with "How to" — vary with
"Why...", "What...", "Which...", "[N] ways...", "[Noun] that..."

---

### INJECT: Comparison Table

**When:** Check 5 FAIL (comparison content exists, no table)

**Position:** After the section that introduces the comparison.

**Required format:**
```
| Option | [Criterion 1] | [Criterion 2] | [Criterion 3] | Best for |
|--------|--------------|--------------|--------------|---------|
| [A]    | [specific]   | [specific]   | [specific]   | [who]   |
| [B]    | [specific]   | [specific]   | [specific]   | [who]   |
```

**Rules:**
- Cell content: 3–8 words maximum per cell
- Criteria must come from the existing draft content — do not invent
  comparison criteria
- "Best for" column is required — this is what buyers want to know
- Balance is required — do not make one option obviously superior
  unless the draft's argument demands it

---

### INJECT: First-Person Authority Statement

**When:** Check 6 FAIL (no authority statement)

**Position:** In the introduction (first 400 words) or at the start
of the most relevant section.

**Required structure:**
```
In [specific context], [specific finding that demonstrates experience].
```

**Examples:**
```
In auditing 40 Series A SaaS companies over 6 months, the most common
gap was not content volume — it was content structure.
```

**Rules:**
- Context must be specific (number + type + timeframe)
- Finding must be specific (what was actually found or learned)
- Must come from real experience in the draft — never invented
- If no specific experience mentioned in the draft:
  `MANUAL REQUIRED — Insert a specific context + finding here.
  Template: "In [what you've done], [what you found]."`

---

### INJECT: FAQ Block

**When:** Check 4 FAIL (no FAQ section or fewer than 5 Q&A pairs)

**Position:** Before the conclusion, at the bottom of the article.
Heading: `## Frequently Asked Questions`

**How to generate the questions:**
1. What questions would a buyer who just read this article still have?
2. What would they search next in Perplexity after reading this?
3. What objections or concerns does the article not directly address?

**Question language rules:**
- Natural, conversational language — how a buyer would actually ask
- No formal "What constitutes the optimal..." framing
- Use question words: What, How, Why, When, Which, Can, Is, Does, Should

**Answer rules:**
- First sentence must directly answer the question (no preamble)
- 2–4 sentences total
- Self-contained — makes sense without reading the article
- Specific where possible

**Minimum:** 7 Q&A pairs
**Maximum:** 10 Q&A pairs

**Forbidden first words for answers:**
"Great question", "That's a good question", "This depends", "It varies"

---

## Output Format

```
AEO INJECTION COMPLETE
Target query: "[TARGET_QUERY]"
Format: [FORMAT_TYPE]

INJECTIONS APPLIED: [N]
1. [Check name]: [one sentence describing what was inserted and where]
2. [Check name]: [same]
...

MANUAL REVIEW REQUIRED: [N items]
[Each item with template ready to fill in]

WORD COUNT: [before] → [after injections]
[Note if word count crossed a threshold]

---
OPTIMIZED DRAFT:

[Full draft with all injections applied, clearly marked with
<!-- AEO INJECTION: [element name] --> comments so the human can
find and review each insertion]
```

---

## Quality Gate

After all injections, verify:
- [ ] Definition block appears before word 300 (if injected)
- [ ] Opening paragraph answers TARGET_QUERY in sentence 1 (if rewritten)
- [ ] No injection marker text left in draft (`<!-- AEO INJECTION -->` comments
      are structural markers for review, not visible to readers — they're fine
      to leave in. But "[INSERT HERE]" or "[placeholder]" text is not fine.)
- [ ] FAQ answers all start with a direct answer (not a question or hedge)
- [ ] FAQ has minimum 7 Q&A pairs
- [ ] All H2s pass the "would someone search this?" test
- [ ] No injected content contradicts existing content

---

## Common Mistakes

- **Injecting before reading the draft**: The numbered process section must
  be extracted from existing draft content, not invented. Always read the
  full draft before building the process section.

- **FAQ questions that are too formal**: "What are the primary advantages of
  implementing AEO?" → No. "Does AEO work if my domain authority is low?" → Yes.

- **Generic authority statements**: "Based on my experience in content marketing..."
  is not an authority statement. "In auditing 40 Series A companies, the
  most common gap was..." is an authority statement.

- **Definitions that require context**: The definition block must work
  standalone. If it references "the system described above" or "as we discussed,"
  it won't be extracted clean.

---

## Related Skills

- **aeo-checker**: Run before this skill — produces the AEO_REPORT
  this skill requires
- **voice-validator**: Run after this skill — checks that injected
  content doesn't introduce voice violations
- **aeo-page-generator**: Creates AEO pages with the structure built in
  from the start, use this if you're starting from scratch instead of
  fixing existing content (blog-writer for first-person founder posts)
