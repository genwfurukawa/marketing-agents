---
name: compound
description: "Capture a just-applied correction or durable lesson into the compounding knowledge store at lessons/{category}/{slug}.md. Use after the user corrects, rejects, or rewrites an output; after a gate (voice-validator, cross-model reviewer) catches a preventable error; after a draft takes 3+ revision rounds; or when a non-obvious fix is verified. Triggers on: 'capture this lesson', 'compound this', 'remember this', 'write a lesson', 'that worked', 'add to lessons', and as the closing step of /campaign-retro and the weekly planning review. Classifies the learning, checks for overlap with existing lessons (updates instead of duplicating), writes a frontmatter-tagged file, and regenerates the lessons.md index. Has a headless mode for automated retro flows. Does NOT capture trivial typos or anything already recorded in the repo/CLAUDE.md."
metadata:
  version: 1.0.0
---

# Compound

Capture a correction or durable lesson into the knowledge store while context is fresh, so the next
agent does not re-learn it from scratch. This is the implemented core of the repo's Self-Improvement
Protocol (CLAUDE.md): every correction becomes a constraint that prevents the same mistake twice.

The deliverable is **one file** - a learning at `lessons/{category}/{slug}.md` - plus the regenerated
`lessons.md` index. Nothing else.

## When to capture (and when not)

Capture when any correction trigger fires: the user says "no / wrong / not like that / change this" or
rewrites output; a gate catches a preventable error; a draft takes 3+ rounds; an output misses the ICP;
published content underperforms; or a non-obvious fix to a tool/process is verified.

Do **not** capture: a trivial typo, a one-off with no reusable rule, or something the repo already
records (code structure, git history, an existing CLAUDE.md rule, an existing lesson). If asked to
remember one of those, capture instead what was *non-obvious* about it, or decline and say why.

## Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Interactive** (default) | direct invocation | Confirm the proposed category/slug/rule with the user only if classification is genuinely ambiguous; otherwise write and report. |

## Workflow

### 1. Extract the learning
From the conversation, state in two parts: the **problem** (the concrete symptom - the exact bad
output, error string, or rejected phrasing) and the **rule** (the falsifiable constraint that prevents
it). If you cannot name a reusable rule, there is no lesson - stop and say so.

### 2. Read the conventions
Read `references/conventions.md` (this skill's directory). It holds the frontmatter schema, the
category list, the `problem_type` enum, slug rules, the YAML-safety quoting rule, and the overlap
decision. Do not classify from memory - the categories and enums are specific.

### 3. Classify
Choose `category`, `problem_type`, `applies_to` (the skills/agents/scopes that must obey - read the
conversation for which tool produced the error), `tags` (searchable: error strings, module names,
concepts), a kebab `slug` derived from the rule, and a one-line imperative `title`.

### 4. Overlap check (update beats duplicate)
Grep the store for the same rule before writing:
```bash
grep -rl "<keyword>" lessons/
```
Read any strong matches. If an existing file already covers this problem and rule, **update it**
(sharpen the rule, add the new symptom, add `last_updated: YYYY-MM-DD`) instead of creating a second
file. This is the repo's `audit-before-creating` rule applied to the store. Only create a new file on
low/moderate overlap.

### 5. Write the file
Write `lessons/{category}/{slug}.md` with the frontmatter schema and body structure from
`conventions.md`. Apply the YAML-safety quoting rule (single-quote a title containing a double quote).
No em dashes anywhere.

### 6. Regenerate the index
```bash
python3 .claude/skills/compound/scripts/reindex.py
```
This rewrites the `## Index by category` section of `lessons.md` from the files (stdlib only, no
deps), preserving the protocol prose above the marker. Never hand-edit the index. The script warns if
any file is missing `slug`/`category` frontmatter - fix those before finishing.

### 7. Propagate if the fix changes a tool
If the rule means a skill or agent should now behave differently, say which one and offer to update its
prompt (CLAUDE.md mandates this). Captured-but-not-propagated is half a fix.

## Output

Interactive:
```
Captured: lessons/<category>/<slug>.md  (created | updated existing)
Rule: <one line>
Applies to: <scopes>
Index: reindexed (<N> learnings)
Propagation: <none needed | update <skill/agent> recommended>
```

Headless (for /campaign-retro, the weekly planning review):
```
Compound: lessons/<category>/<slug>.md (created|updated) - <one-line rule>
```

When nothing qualified, say so explicitly: `Compound: no reusable lesson in this exchange` - the visible
no-op is the audit signal that the trigger was considered.

## Common mistakes

| Wrong | Correct |
|-------|---------|
| Hand-editing the `## Index by category` section | Run `scripts/reindex.py` - the index is derived |
| Creating a new file when one already covers the rule | Grep first; update on high overlap |
| A vague rule ("be careful with Notion") | A falsifiable constraint with the exact symptom and fix |
| Title with an unquoted double quote breaking the frontmatter | Single-quote the title (see conventions.md) |
| Capturing and stopping | If the fix changes a skill/agent, propagate it (step 7) |
