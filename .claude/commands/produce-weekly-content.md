---
description: Run the full weekly content production pipeline - score insights, build objects, write posts, validate voice, check AEO, inject missing elements
argument-hint: [--client client-slug] [--format linkedin|blog|newsletter] [--insight "raw text or file path"]
allowed-tools: Task, Read, Write, Glob, Grep, WebSearch, WebFetch
---

## Task

Run the 6-step content production pipeline that turns a raw founder insight into a publish-ready piece of content. Every step produces a structured output that feeds the next step. No skipping.

**Arguments:**
- `--client`: Client slug (loads brand brain, voice rules, query bank)
- `--format`: Target format - defaults to linkedin (options: linkedin, blog, newsletter)
- `--insight`: Optional - raw insight text or path to a file with observations. If not provided, pulls from Notion Insight Log.

## The Pipeline

```
Step 1: insight-scorer      → Pick the strongest insight
Step 2: insight-object-builder → Structure it into a 6-field brief
Step 3: linkedin-post-writer   → Write the draft (or blog/newsletter)
Step 4: voice-validator        → Check voice rules, fix violations
Step 5: aeo-checker            → Check AI citation structure
Step 6: aeo-injector           → Insert missing AEO elements
```

## Steps

### Step 1: Score and Select the Insight

**Use skill: insight-scorer**

If `--insight` is provided:
- Use that as the candidate pool (may be one insight or several)
- Score against the 4 criteria: Query Alignment, Distinctiveness, Evidence Quality, Recency

If no `--insight`:
- Pull the last 7 days of entries from Notion Insight Log (via MCP)
- If Notion is unavailable, ask the user to paste their observations

**Gate:** At least one insight must score 5/8 or higher to proceed. If all score below 5, show the scores and ask the user to either strengthen one or provide a new observation.

**Output needed for next step:**
- The selected insight text
- The source type
- The scoring justification (used by insight-object-builder for Fields 3 and 4)

Present the scoring report to the user. Ask: "Proceed with #1, or pick a different one?"

---

### Step 2: Build the Insight Object

**Use skill: insight-object-builder**

Take the selected insight and build the 6-field Insight Object:

1. **Insight** - One specific, citable sentence
2. **Why It Matters to ICP** - One sentence from the buyer's perspective
3. **Query Mapped To** - The exact AI search query this should answer
4. **Content Angle + Hook Type** - The editorial frame and opening style
5. **Evidence** - The specific data or observation that makes it credible
6. **Recommended Format** - linkedin-post, blog-post, or newsletter

**Gate:** All 6 fields must be populated. If evidence is WEAK, flag it and ask for more before continuing.

Present the Insight Object to the user. Ask: "Ready to write, or adjust anything?"

---

### Step 3: Write the Draft

**Use skill based on format:**
- LinkedIn → **linkedin-post-writer**
- Blog → Write a long-form draft following AEO blog structure
- Newsletter → Write a newsletter edition (single topic, 300-600 words)

The writer skill uses the Insight Object as its input. Every field maps to a part of the post:
- Field 1 (Insight) → The core claim
- Field 2 (Why It Matters) → The implication section
- Field 4 (Content Angle + Hook Type) → How the post opens
- Field 5 (Evidence) → The proof in the body

**Gate:** Draft must pass the writer skill's internal quality gate before moving on.

Present the draft to the user. Ask: "Approve this draft for validation, or revise?"

---

### Step 4: Validate Voice

**Use skill: voice-validator**

Run the draft through the format-specific checklist:
- LinkedIn: 8 checks (first word, hook specificity, hook format, bullet lists, length, CTA quality, forbidden words, engagement bait)
- Blog: 6 checks (opening directness, passive voice, word count, forbidden words, heading quality, filler phrases)
- Newsletter: 5 checks (single topic, single CTA, newsletter-speak, word count, forbidden words)

Auto-fix what can be auto-fixed (forbidden words, engagement bait CTAs, filler phrases).
Flag what needs human review (generic hooks, indirect openings, bullet list decisions).

**Gate:** Draft must reach PASS or PASS WITH AUTO-FIXES. If NEEDS HUMAN REVIEW items exist, present them and wait for the user's decision.

Present the validation report and corrected draft. Show what was auto-fixed and what needs human eyes.

---

### Step 5: Check AEO Structure

**Use skill: aeo-checker**

For LinkedIn posts: Run the 3-check version (citable claim, query alignment, no forbidden AEO patterns).

For blog posts: Run the full 9-check version (definition block, query-matched headings, numbered process, FAQ block, comparison table, authority statement, query alignment, statistics, freshness signals).

**Gate:** For LinkedIn, all 3 checks should PASS. For blog, at least 7 of 9 should PASS.

Present the AEO report. If items FAIL, proceed to Step 6.

---

### Step 6: Inject Missing AEO Elements

**Use skill: aeo-injector**

Only runs if Step 5 found FAIL items. Insert missing elements in this order:
1. Definition block
2. Opening paragraph rewrite
3. H2 heading rewrites
4. Numbered process section
5. Comparison table
6. First-person authority statement
7. FAQ block

**Gate:** After injection, the draft should pass all applicable AEO checks.

Present the final draft with injection markers so the user can review each insertion.

---

### Final: Save and Summarize

1. **Save the output:**
   - If --client: Save to `{client_root}/production/{format}/drafts/{YYYY-MM-DD}_{topic_slug}.md`
   - If no client: Print the final draft to the conversation

2. **Include metadata block at the top of the saved file:**
   ```
   ---
   insight_score: {score}/8
   query_mapped_to: "{query}"
   hook_type: {type}
   voice_status: {PASS/PASS WITH FIXES}
   aeo_status: {PASS/N checks passed}
   format: {format}
   created: {date}
   ---
   ```

3. **Present summary:**
   ```
   Pipeline complete.

   Insight: "{one sentence}"
   Format: {format}
   Query: "{query mapped to}"
   Voice: {status} ({N} auto-fixes)
   AEO: {status} ({N} injections)
   Saved: {file path or "printed to conversation"}

   Next: Review the draft, then publish.
   ```

## Rules

- Never skip a step. The chain exists because each step catches things the previous step doesn't.
- Present output to the user after each step. Don't run all 6 silently and dump the result.
- If any gate fails, stop and work with the user to fix it before moving on.
- Never invent insights, evidence, or statistics. Everything comes from the user's real observations.
- The user can say "skip to step N" if they already have a draft they want to validate. In that case, start at the requested step.

## Example Usage

```
# Full pipeline from scratch - pulls insights from Notion
/produce-weekly-content --client acme --format linkedin

# Start with a specific insight
/produce-weekly-content --client acme --insight "7 of 10 companies I audited this month scored a 0 on comparison queries in ChatGPT"

# Just validate and AEO-check an existing draft (skip to step 4)
/produce-weekly-content --client acme
> "skip to step 4, here's my draft: [paste]"

# Blog format
/produce-weekly-content --client acme --format blog --insight path/to/notes.md
```