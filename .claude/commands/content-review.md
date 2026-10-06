---
description: Run 4 parallel quality reviewers on content drafts - voice, AEO, brand consistency, and conversion
argument-hint: [--client client-slug] [--draft path/to/draft.md | --dir path/to/drafts/]
allowed-tools: Task, Read, Write, Glob, Grep
---

# Content Review - Parallel Specialist Reviews

You run 4 independent reviewers in parallel on one or more content drafts.

Each reviewer evaluates from a different lens. No reviewer overlaps with another.

## The 4 Reviewers

| Reviewer | Tool | Focus | Does NOT Check |
|----------|------|-------|----------------|
| **Voice Validator** | `voice-validator` skill | Tone, word choice, format rules, forbidden words | Brand alignment, AEO, conversion |
| **AEO Checker** | `aeo-checker` skill | AI citation structure, definition blocks, FAQ schema | Voice, brand, conversion |
| **Brand Consistency** | `brand-consistency-reviewer` agent | Brand Brain alignment, positioning, ICP, style | Voice mechanics, AEO, conversion |
| **Conversion** | `conversion-reviewer` agent | Pipeline impact, CTA quality, pain points, evidence | Voice, brand, AEO |

## Input

Accepts either:
- `--draft path/to/draft.md` - Review a single draft
- `--dir path/to/drafts/` - Review all drafts in a directory (e.g. `clients/{slug}/production/drafts/`)
- If neither provided, ask the user for the draft content or path

For directory mode:
- Resolve the client via the active client convention: explicit `--client` slug, else the `CLIENT_CONFIG` env var pointing at the client's config.yaml
- Load all `.md` files from the directory

## Execution

### Step 1: Load Configuration

Before invoking reviewers, load these files (pass relevant sections to each reviewer):

1. `clients/{client}/config.yaml` - voice.never_say, voice.always_say, positioning, icp, offers
2. `lessons.md` - all accumulated corrections
3. `clients/{client}/config/voice-guide.md` - voice constraints
4. Client Brand Brain (if client specified): `clients/{slug}/config/brand-brain.md`

### Step 2: Detect Format

Read the draft frontmatter or content to determine format:
- `format: linkedin-post` -> LinkedIn review rules
- `format: blog` or `format: aeo-page` -> Blog review rules
- `format: email` or `format: newsletter` -> Email review rules
- `format: youtube-script` -> Video review rules
- If no frontmatter, infer from content length and structure

### Step 3: Run 4 Reviewers in Parallel

For EACH draft, launch all 4 reviewers simultaneously via the Task tool:

**Task 1: Voice Validation**
```
Invoke the voice-validator skill on this draft.
Format: {detected_format}
Client: {client_slug}
Draft content: {draft_content}
```

**Task 2: AEO Check**
```
Invoke the aeo-checker skill on this draft.
Format: {detected_format}
Draft content: {draft_content}
```

**Task 3: Brand Consistency Review**
```
Invoke the brand-consistency-reviewer agent.
Client: {client_slug}
Brand Brain path: {brand_brain_path}
Config sections: {positioning, icp, voice from clients/{client}/config.yaml}
Draft content: {draft_content}
```

**Task 4: Conversion Review**
```
Invoke the conversion-reviewer agent.
Client: {client_slug}
ICP config: {icp section from clients/{client}/config.yaml}
Offers: {offers section from clients/{client}/config.yaml}
Draft content: {draft_content}
```

### Step 4: Compile Results

After all 4 reviewers complete, compile a unified review report.

### Step 5: Auto-Fix

If the AEO checker found missing elements, invoke `aeo-injector` skill to auto-fix.

For voice-validator auto-fixable issues (banned words, engagement bait CTAs), apply fixes.

Mark auto-fixed items in the report.

### Step 6: Present Results

Show the compiled report and ask: "Approve these fixes and move to QA, or revise specific items?"

## Output Format

### Unified Review Report

```markdown
# Content Review: {draft_filename}

## Summary

| Reviewer | Result | Issues |
|----------|--------|--------|
| Voice Validator | {PASS/FAIL} | {count} issues ({count} auto-fixed) |
| AEO Checker | {PASS/FAIL} | {count} issues ({count} auto-fixed) |
| Brand Consistency | {PASS/FAIL} | {count} issues |
| Conversion | {PASS/FAIL} (Score: {N}/10) | {count} issues |

**Overall: {PASS | FAIL | PASS WITH FIXES}**

## Auto-Fixed Items
{List of changes made automatically by aeo-injector and voice-validator}

## Issues Requiring Human Review

### Critical
{Issues that block publishing - must be fixed}

### Major
{Issues that should be fixed - significantly impact quality}

### Minor
{Suggestions for improvement - optional}

## Reviewer Details

### Voice Validator
{Full voice-validator output}

### AEO Checker
{Full aeo-checker output}

### Brand Consistency
{Full brand-consistency-reviewer output}

### Conversion
{Full conversion-reviewer output}
```

### Batch Directory Output

When reviewing a directory, save the compiled report to:
`{dir}/reviews/review_compiled.md`

Also save individual reviewer reports:
- `{dir}/reviews/voice_review.md`
- `{dir}/reviews/aeo_review.md`
- `{dir}/reviews/brand_review.md`
- `{dir}/reviews/conversion_review.md`

## Pass/Fail Logic

- **PASS**: All 4 reviewers pass, conversion score 7+
- **PASS WITH FIXES**: Auto-fixes applied, no remaining critical/major issues, conversion score 5+
- **FAIL**: Any reviewer has critical issues, OR conversion score below 5

A FAIL blocks `/content-qa`. The user must address the issues and re-run review.

## Standalone Usage

This command also works on any single draft:

```
# Review a single draft
/content-review --draft ../clients/acme/content/linkedin/drafts/2026-04-14_ai-citations.md

# Review with client context
/content-review --client acme --draft path/to/draft.md
```

## Rules

1. Always run all 4 reviewers - never skip one
2. Run reviewers in parallel, not sequential
3. Auto-fix what can be auto-fixed before presenting to user
4. Rank remaining issues by severity (critical > major > minor)
5. Never modify the original draft - create a reviewed copy if auto-fixes applied
6. Load clients/{client}/config.yaml and lessons.md before invoking any reviewer
7. If Brand Brain doesn't exist for the client, run 3 reviewers (skip brand consistency) and note the gap
