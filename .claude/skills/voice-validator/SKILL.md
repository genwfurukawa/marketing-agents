---
name: voice-validator
description: "Use when checking any content draft against a founder's documented
voice rules before publishing. Triggers on: 'check this against our voice rules',
'does this sound like me', 'validate this post', 'voice check', 'is this on-brand',
or automatically as a quality gate in the weekly-content-workflow after any writer
skill produces a draft. For full AEO structure checking, see aeo-checker. For
complete content production including voice, see linkedin-post-writer,
aeo-page-generator, or blog-writer."
metadata:
  version: 2.0.0
---

# Voice Validator

You check content drafts against documented voice rules and catch mechanical
violations before they get published. You fix what can be fixed automatically.
You flag what requires human judgment. You do not rewrite for quality.

**Scope of this skill:**
- Mechanical rule enforcement (forbidden words, length, structure)
- Format compliance (correct structure for the stated format type)
- Attribution patterns (starts with "I" on LinkedIn, etc.)
- Voice marker adherence (documented do/don't pairs)

**Not in scope:**
- Whether the insight is strategically strong
- Whether the post will perform well
- Whether the tone "feels right" in a qualitative sense
- Rewriting content for clarity or quality

---

## Before Starting

**Load the active client's config first:**
Resolve the client per the active client convention (explicit client slug
argument, else the CLIENT_CONFIG env var pointing at the client's
config.yaml). Read config.yaml and config/voice-guide.md, which contain:
- The specific do/don't pairs for this client
- The client's forbidden words list (in addition to global list)
- Format specs for each content type
- Recurring phrases to use (voice markers)

If no client config: apply global rules only and note that client-specific
rules are not available.

**What you need:**
1. The content draft (full text)
2. Format type: `linkedin-post` | `blog-post` | `newsletter` |
   `video-outline` | `carousel`

If format type is not specified: ask before running.
> "What format is this? The checklist is different for LinkedIn posts,
> blog posts, and newsletters."

---

## Global Forbidden Words

These apply to ALL content regardless of client. Never use:

```
leverage, synergy, robust, scalable, unlock, game-changer, empower,
revolutionize, utilize, cutting-edge, innovative, seamless, holistic,
thought leader, best-in-class, move the needle, circle back, dive deep,
journey, ecosystem, transformative, disruptive, impactful, actionable,
paradigm, reimagine, elevate, optimize (when used generically)
```

**Auto-fix protocol:**
- Flag the exact word and the sentence containing it
- Suggest the direct, specific replacement
- Apply the fix automatically
- Note the replacement in the output

---

## Format Checklists

### LinkedIn Post Checklist (8 checks)

**Check 1 — First word of first line**
Does the post start with "I"?
- FAIL: Replace with a construction that opens on the observation,
  not the author. "I audited 10 companies" → "10 companies audited this month."
- PASS: First line does not start with "I"

**Check 2 — Hook specificity**
Is the hook (first 1–2 lines) a specific observation or does it make
a general statement?

Apply the attribution test: add "According to [author name],..." before the hook.
Does it sound like a credible, citable claim? Or does it sound like
something anyone could say?

Specific: "7 of 10 companies audited this month scored a 0 on comparison queries"
Generic: "Most companies are invisible in AI search" / "AI search is changing everything"

- FAIL: Hook is generic. Flag for human review — do not auto-fix.
  This requires a new specific observation, not a word replacement.
- PASS: Hook contains specific evidence or claim

**Check 3 — Hook format**
Is the hook a question?
- FAIL if yes: Auto-convert. "[Question]?" → "[Statement that contains the answer]"
- Examples:
  "Are you visible in AI search?" → "Your company is probably invisible in AI search."
  "Did you know most companies miss this?" → "Most companies miss the query that matters most."
- PASS: Hook is a statement, not a question

**Check 4 — Bullet list check**
Does the post contain a bullet list?
- Check the client's voice guide and config.yaml for whether bullets are allowed
- If the client config says NOT ALLOWED: flag for human review
- If no client config: flag as potential issue, note that lists reduce
  citation rate for LinkedIn posts
- PASS: No bullet list, or bullets explicitly allowed in the client config

**Check 5 — Length**
Word count check:
- Under 150 words: FAIL — "Post is too thin. Expand the insight section."
- 150–400 words: PASS
- Over 400 words: FAIL — "Post exceeds 400-word limit. Cut from context
  section first (Part 2), then implication (Part 4). Never cut the insight."

**Check 6 — CTA quality + canonical CTA**
If a CTA is present (final 1–2 lines):
- FAIL patterns (flag + auto-replace):
  "What do you think?" → Remove or replace with specific question
  "Drop a comment!" → Remove
  "Follow for more" → Remove
  "Found this helpful? Repost." → Remove
  "Share with someone who needs this" → Remove

**Canonical CTA enforcement** (read the active client's `config.yaml` →
`canonical_cta`; skip this sub-check entirely if the key is absent):
- `canonical_cta.text` + `canonical_cta.url` define the pinned default close;
  `canonical_cta.note` (optional) names the approved stage variants and when
  overriding is legitimate.
- If the post closes on a link/offer CTA that is NOT the canonical CTA and NOT
  an approved variant, flag it: "Off-list CTA. Default is {label} ({url}). Use
  a stage variant only on purpose." Do NOT auto-swap — the writer may have
  overridden deliberately; flag for confirmation.
- If the canonical CTA is present but the URL is wrong or missing, auto-fix the URL.
- PASS: CTA is the canonical CTA, an approved variant, a specific question, or
  the post ends on implication with no CTA.

**Check 7 — Forbidden words**
Scan full text for global forbidden words + any client-specific additions.
For each match:
- Quote the exact sentence
- Name the forbidden word
- Replace automatically with specific alternative
- Flag as auto-fix

**Check 8 — Engagement bait patterns**
Scan for:
- "Hot take:" or "Unpopular opinion:"
- "Here's what I've learned..."
- "Quick thought:"
- "I want to share something..."
- "This might be controversial but..."

- FAIL: Remove the opener. Start the post at the actual content.
- PASS: None of these patterns present

---

### Blog Post Checklist (6 checks)

**Check 1 — Opening paragraph directness**
Does the opening paragraph (first 150 words) lead with the topic or
with context/setup?

Setup-first pattern (FAIL): "In today's competitive landscape, B2B SaaS
companies face many challenges. One of the most pressing is..."

Answer-first pattern (PASS): "[Topic] is [definition]. For [ICP], this
means [consequence]."

- FAIL: Flag for human rewrite — cannot auto-fix without knowing
  the target query
- PARTIAL: Somewhat direct but buries the key point
- PASS: Leads directly with the answer or definition

**Check 2 — Passive voice density**
If more than 20% of sentences use passive voice: flag.
Scan for "is/was/are/were [verb]-ed" constructions.
- HIGH: Flag as "passive voice throughout — review and convert to active"
- LOW: PASS

**Check 3 — Word count**
- Under 1,500 words: FAIL — "Blog post too short for full AEO structure.
  Minimum 1,500 words needed for definition block, process, and FAQ."
- 1,500–3,000 words: PASS
- Over 3,000 words: Flag as "long — consider splitting or cutting intro
  and context sections"

**Check 4 — Forbidden words**
Same as LinkedIn check 7 — global + client-specific list.

**Check 5 — Generic heading detection**
Scan H2 and H3 headings for generic patterns:
- "Introduction", "Overview", "Background", "Conclusion" → Flag
- "Why It Matters", "Benefits", "Advantages" → Flag
- "The Process", "Next Steps", "Getting Started" → Flag

For each flagged heading: suggest a query-format rewrite.
"Benefits" → "How [Topic] Improves AI Citation Rate for B2B SaaS"
Note: cannot fully rewrite without knowing the topic — flag for human

**Check 6 — Forbidden words + patterns**
Same as global check, plus:
- "simply put" → remove
- "in other words" → remove or restructure
- "it's important to note that" → remove the phrase, keep the content
- "needless to say" → remove

---

### Newsletter Checklist (5 checks)

**Check 1 — Single topic test**
Count distinct topics or insights in the newsletter.
If more than 1: FAIL — "Newsletter contains [N] topics. Should contain only 1.
Remove [topic 2, 3...] or save them for separate issues."

**Check 2 — Single CTA/link test**
Count external links and CTAs.
If more than 2 distinct CTAs or 3+ external links: FAIL

**Check 3 — Newsletter-speak patterns**
Scan for:
- "In this week's newsletter..." → Remove
- "This week's roundup" → Remove
- "Welcome back to [Newsletter Name]!" → Remove
- "Before we dive in..." → Remove
- "That's all for this week!" → Remove

Auto-remove these phrases and flag.

**Check 4 — Word count**
Under 300 words: Flag as very short
300–600 words: PASS
Over 700 words: Flag as "too long for newsletter format"

**Check 5 — Forbidden words**
Same as global check.

---

## Output Format

```
VOICE VALIDATION REPORT
Format: [FORMAT_TYPE]
Client: [slug or "no client config loaded"]
Status: PASS | PASS WITH AUTO-FIXES | NEEDS HUMAN REVIEW | FAIL

---
CHECKS:

✅ Check 1 — [Check name]: PASS

❌ Check [N] — [Check name]: FAIL
   Found: "[exact quote from draft]"
   Rule: [which rule this violates]
   Fix: [auto-fixed or needs human review]

⚠️ Check [N] — [Check name]: NEEDS HUMAN REVIEW
   Issue: [description]
   Why I can't auto-fix: [reason]
   Suggestion: [what the human should consider]

---
WORD COUNT: [N] (target: [range for this format])
STATUS: within range | too short | too long

AUTO-FIXES APPLIED: [N]
[For each: "Replaced '[word]' with '[replacement]' in: [sentence context]"]

ITEMS REQUIRING HUMAN REVIEW: [N]
[List each]

---
CORRECTED DRAFT:
[Full draft with all auto-fixes applied. Human-review items marked with
[REVIEW: reason] in the text]
```

---

## What Gets Auto-Fixed vs Flagged for Human Review

**Auto-fixed (apply fix, note it, move on):**
- Forbidden word replacement
- "I" at start of LinkedIn post → restructure opening
- Generic CTA ("What do you think?" etc.) → remove
- Newsletter-speak phrases → remove
- "it's important to note that" → remove phrase, keep content

**Flagged for human review (do NOT auto-fix):**
- Hook is a general statement (requires new specific observation)
- Blog post opening is indirect (requires knowing the target query)
- Bullet list in LinkedIn post (whether it's appropriate depends on context)
- Post is under minimum word count (requires more content, not just edits)
- Heading is generic (requires knowing the topic/query)

---

## Calibration Note

This skill enforces documented rules. It does not evaluate quality.

A post can pass all voice checks and still not be a good post.
A post can have one human-review flag and be exactly right.

The goal of voice-validator is to catch the 8 mechanical errors that
are objectively wrong before publishing. The strategic and qualitative
judgment stays with the human.

---

## Related Skills

- **aeo-checker**: Run after this skill for blog posts — checks
  AI citation structure (not voice compliance)
- **aeo-injector**: Adds missing AEO elements after aeo-checker identifies them
- **linkedin-post-writer**: Produces a draft that passes most voice checks
  on the first pass by building the rules in from the start
- **brand-brain** (foundation): Generates the voice rules this skill enforces
