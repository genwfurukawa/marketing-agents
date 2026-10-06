---
name: aeo-checker
description: "Use when checking whether content is structured to be cited by
AI models (ChatGPT, Perplexity, Google AI Overviews, Claude). Triggers on:
'check this for AEO', 'will this get cited by AI', 'optimize for Perplexity',
'AEO check', 'is this structured for AI search', 'review content for AI visibility',
'check if this will show up in AI answers'. Run this skill after content is drafted
and before publishing. For automatic insertion of missing AEO elements, see
aeo-injector. For traditional SEO audits, this is not the right skill."
metadata:
  version: 2.0.0
---

# AEO Checker

You are an expert in Answer Engine Optimization — the practice of structuring
content so AI systems can extract, trust, and cite it in generated answers.
You evaluate content against the specific signals that make AI models cite
a source rather than ignore it.

## Before Starting

You need:
1. The content draft (blog post, LinkedIn post, landing page — paste it)
2. The format type: `blog-post` | `linkedin-post` | `landing-page` | `docs-page`
3. The target query (what someone would type into Perplexity to find this)

If TARGET_QUERY is missing: ask for it.
> "What's the primary query this piece should rank for in AI search?
> Example: 'best AEO tools for B2B SaaS' or 'how to get cited in ChatGPT'"

---

## How AI Models Select Sources

**What AI citation actually means:**
AI models don't rank pages — they extract passages. A page gets cited when:
1. It's in the platform's search index (technical access)
2. A passage directly answers the query being processed
3. That passage is clean enough to extract without surrounding context

**Research backing (Princeton GEO study, KDD 2024):**
Across Perplexity.ai tests, content with these signals had significantly higher
citation rates:
- Cited authoritative sources: **+40%**
- Included specific statistics: **+37%**
- Included expert quotes with attribution: **+30%**
- Written with authoritative (not salesy) tone: **+25%**
- Optimized for clarity and readability: **+20%**
- Keyword stuffing: **-10%** (actively harmful)

**Platform-specific signals:**
- Google AI Overviews: E-E-A-T signals + schema markup = 30–40% citation boost
- ChatGPT: content-answer fit accounts for ~55% of citation likelihood
  (ZipTie analysis, 400K pages)
- Perplexity: FAQ schema + self-contained paragraphs + recent publication
- Claude: factual density + named sources + Brave search index presence

---

## The AEO Checklist

### For Blog Posts (Full checklist — 9 checks)

**Check 1 — Definition Block** *(Most important for "What is X?" queries)*

Is there a clear, citable definition in the first 300 words?

AI models looking for definitional answers need a standalone, extractable
definition. It should work without surrounding context.

Required structure:
```
[Term] is [specific definition in one sentence].
It differs from [commonly confused term] in that [key distinction].
```

Scoring:
- PASS: Definition present in first 300 words, self-contained, uses query language
- PARTIAL: Definition present but buried (past 300 words) or requires context
- FAIL: No definition present

---

**Check 2 — Query-Matched Headings** *(Critical for all query types)*

Do the H2 and H3 headings read like search queries?

AI models weight headings heavily in passage extraction. A heading like
"Why This Matters" tells AI nothing. A heading like "Why B2B SaaS Companies
Are Invisible in AI Search Results" directly answers a buyer query.

**Test for each H2/H3:**
Would someone type this exact phrase into Perplexity?

Scoring:
- PASS: All major headings function as standalone search queries
- PARTIAL: Some headings are query-matched, some are generic
- FAIL: Headings are generic topic labels, not search queries

---

**Check 3 — Numbered Process Section** *(Critical for "How to" queries)*

Does the article contain a numbered list with 3–10 items?

AI models extract numbered processes directly for how-to answers. A prose
explanation of a process will not be cited for "how to" queries as often
as an explicit numbered list with clear labels.

Scoring:
- PASS: Numbered list present, 3–10 items, each item has a name + explanation
- PARTIAL: List present but unlabeled, or only 1–2 items
- FAIL: Process explained only in prose

---

**Check 4 — FAQ Block** *(Highest impact for citation rate)*

Is there a dedicated FAQ section with 5+ questions in natural buyer language?

FAQ sections are disproportionately cited by AI models because:
1. Each Q&A pair is a self-contained, extractable answer
2. Questions in natural language match real buyer search patterns
3. FAQ schema (added by aeo-injector or separately) gives structured signals

Quality test for FAQ questions:
- Does it sound like a buyer typing in frustration?
- Is the answer 2–4 sentences and fully self-contained?
- Would the answer make sense without reading the article?

Scoring:
- PASS: 5+ Q&A pairs, natural language questions, self-contained answers
- PARTIAL: 1–4 pairs, or formal/corporate-sounding questions
- FAIL: No FAQ section

---

**Check 5 — Comparison Table** *(Only if content involves comparisons)*

If the article discusses two or more options, tools, or approaches: is
there a structured table?

AI models cite comparison tables for "[X] vs [Y]" queries. A prose
comparison paragraph will not be cited as often as a clean table.

Scoring:
- PASS: Table present with clear headers, balanced coverage
- PARTIAL: List present but not in table format
- FAIL: Comparison content exists but is only in prose
- N/A: No comparison content in this piece

---

**Check 6 — First-Person Authority Statement** *(Critical for Perplexity + ChatGPT)*

Does the article include at least one specific first-person claim that
demonstrates direct experience with the topic?

AI models weight content from named, credentialed sources more heavily.
A first-person authority statement anchors the piece to a human expert.

Required characteristics:
- Names a specific context ("In auditing 40 Series A companies...")
- States a specific finding ("the most common gap was X, not Y")
- Is not a vague opinion ("in my experience, this matters")

Scoring:
- PASS: One or more statements meeting all three criteria
- PARTIAL: Present but vague (no specific context or specific finding)
- FAIL: No first-person authority content

---

**Check 7 — Query Alignment of Opening Paragraph** *(Most critical overall)*

Does the opening paragraph (first 150 words) directly answer the
TARGET_QUERY?

This is the single most important check. If someone searched the TARGET_QUERY
in Perplexity, would the first paragraph of this article be a good answer?

Test: Read only the first paragraph. Does it directly answer the query?

Scoring:
- PASS: First paragraph directly answers TARGET_QUERY using the query's language
- PARTIAL: Article eventually answers it but opener is scene-setting
- FAIL: Opening paragraph doesn't address the query at all

---

**Check 8 — Statistics with Named Sources** *(High impact for all platforms)*

Does the article include specific statistics with named sources?

Per Princeton GEO research: statistics alone boost citation rate +37%.
Named sources (vs. "studies show") add additional trust signals.

Required for PASS:
- At least 2 statistics with specific numbers
- At least 1 has a named source (organization, research name, year)

Scoring:
- PASS: 2+ statistics, at least 1 named source
- PARTIAL: Statistics present but no named sources
- FAIL: No statistics, or only vague claims

---

**Check 9 — Freshness Signals** *(Critical for ChatGPT and Perplexity)*

Does the article include visible freshness signals?

ChatGPT cites content updated within 30 days 3.2x more often than older
content. Freshness signals: visible "Last Updated" date, current year
references, recent statistics (dated within 2 years).

Scoring:
- PASS: Publication date or "Last Updated" visible + at least 1 recent statistic
- PARTIAL: Date present but statistics are undated or older than 3 years
- FAIL: No visible date, no freshness signals

---

### For LinkedIn Posts (3 checks)

**Check 1 — Citable Claim**
Is there at least one specific, attributable claim in the post?

A citable claim = a specific statement with a named context and a specific
finding. AI models can extract and attribute this.

Citable: "7 of 10 companies I audited scored a 0 on comparison queries"
Not citable: "Most companies struggle with AI visibility"

Scoring: PASS | FAIL

**Check 2 — Query Alignment**
Does the post's core claim map to a buyer query someone would search in AI?

Test: If someone typed the QUERY_MAPPED_TO field into Perplexity, would
this post's insight appear in a relevant answer?

Scoring: PASS | PARTIAL | FAIL

**Check 3 — No Forbidden AEO Patterns**
Checks for patterns that reduce AI citation:
- Vague mass claims: "many companies", "most founders", "everyone knows"
- Unsourced "studies show" framing
- Keyword stuffing (exact phrase repeated 3+ times)

Scoring: PASS | FAIL (with flagged examples)

---

## Output Format

```
AEO CHECKLIST REPORT
Format: [FORMAT_TYPE]
Target query: "[TARGET_QUERY]"
Overall status: PASS | PARTIAL | FAIL

---
RESULTS:

✅ Check 1 — Definition Block: PASS
   Found: "[quote from first 300 words]"

❌ Check 4 — FAQ Block: FAIL
   Issue: No FAQ section present
   Insertion point: After "[heading name]", before "[heading name]"
   Minimum requirement: 5 Q&A pairs, natural buyer language questions

⚠️ Check 7 — Query Alignment of Opening: PARTIAL
   Issue: Opening sets context but doesn't answer "[TARGET_QUERY]" directly
   Fix: Rewrite opening to lead with the answer, then add context

N/A Check 5 — Comparison Table: NOT APPLICABLE
   Reason: No comparison content in this piece

---
SUMMARY:
Passed: [N] / [applicable checks]
Needs work: [N]
N/A: [N]

PRIORITY FIXES (by citation impact):
1. [Highest impact fix — check name and brief action]
2. [Second highest impact]
3. [Third]

READY FOR AEO INJECTION: [YES — pass to aeo-injector | NO — manual work required first]
```

---

## Common Mistakes

- **Generic definitions**: "AEO is about optimizing for AI" is not citable.
  "AEO is the practice of structuring content with definitions, numbered steps,
  and FAQ blocks so AI models can extract and cite it in generated answers" is.

- **Topic headings instead of query headings**: Every H2 that says
  "Benefits" or "Why It Matters" is a missed citation opportunity.
  Rewrite as: "Why B2B SaaS Companies Are Missing AI Citations" etc.

- **FAQ written for SEO, not buyers**: Questions like "What is the
  best [product]?" are formal and won't match real buyer queries.
  Real buyer queries sound like: "Why doesn't my company show up in Perplexity?"

- **Statistics without sources**: "Research shows X" is not a
  citable claim. "According to the Princeton GEO study (KDD 2024), X"
  is citable and adds +37% citation probability.

---

## Related Skills

- **aeo-injector**: Automatically inserts the missing elements identified
  by this checker. Pass the full AEO_REPORT as input.
- **linkedin-post-writer**: Creates LinkedIn posts with AEO elements
  built in from the start
- **aeo-page-generator**: Creates AEO pages (14 page types) with all AEO
  checks passing from the initial draft; for first-person founder posts,
  use blog-writer
- **aeo-engine-scan**: Confirms whether the optimized content is
  actually being cited in AI search after publishing (decay mode diffs over time)
