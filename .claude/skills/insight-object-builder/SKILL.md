---
name: insight-object-builder
description: "Use when turning a selected insight into a structured 6-field
Insight Object that writer skills can consume. Triggers on: 'build an Insight
Object', 'structure this insight', 'prepare this for writing', 'create an
insight object from this observation', or automatically at the end of
insight-scorer when a SELECTED insight is ready. The Insight Object is the
universal input format for all writer skills: linkedin-post-writer,
aeo-page-generator, blog-writer, email-agent, storyboard-builder. Nothing gets
written without one."
metadata:
  version: 2.0.0
---

# Insight Object Builder

You turn a raw, selected insight into the structured 6-field Insight Object
that every writer skill in the visibility ops methodology consumes.

The Insight Object is not content. It is the brief that content is written from.
Its job is to remove every ambiguity before writing begins so that the writer
skills produce on-target output on the first pass.

## Before Starting

**Load the active client's config:**
Resolve the client per the active client convention (explicit client slug
argument, else the CLIENT_CONFIG env var pointing at the client's
config.yaml). Read config.yaml, config/icp-psyche.md, and
config/brand-brain.md (POV library), plus the relevant lessons store
categories per CLAUDE.md. The POV library and query bank are needed for
Fields 3 and 4.

**What you need:**
1. The selected insight text (from insight-scorer output, or user-provided)
2. The source type: `insight-log` | `call-notes` | `audit-delta` |
   `podcast` | `community` | `manual`
3. Active query bank (from Notion via MCP, or from the client config's seed list)
4. POV library (from the client's config/brand-brain.md)

If the selected insight came from insight-scorer: the source type and
scoring justifications help complete Fields 1, 3, and 4 faster.

---

## The 6 Fields

Every Insight Object has exactly 6 fields. All 6 must be populated before
the object is complete. No writer skill runs with a partial object.

---

### Field 1: Insight

**What it is:** One sentence describing what was observed, found, or learned.

**Rules:**
1. One sentence only. No "and" connecting two observations.
2. Specific: contains at least one of — a number, a company type,
   a named platform, a named behavior
3. Active: something happened or was found — not a belief or opinion
4. Survives the attribution test: if you added "according to [the founder],..."
   at the front, would it be a credible, citable statement?

**Compression process:**
- If the raw insight is already one specific sentence: use it
- If it's multiple sentences: find the most specific single claim
- If it's a vague observation: push back and ask for specifics before continuing

**Quality test:**
Remove the author's name from the sentence.
Could a generic marketing person have observed and said this exact thing?
If YES: it needs more specificity.

**Examples — PASS:**
```
7 of the last 10 companies audited scored a 0 on comparison queries.
Perplexity now cites Acme (RevOps SaaS) for 'best RevOps tools for Series A'
  after one page was restructured with AEO blocks.
Three CEOs in March 2026 didn't know the difference between AEO and GEO,
  and neither did their marketing teams.
```

**Examples — FAIL (push back and ask for more):**
```
Most companies don't show up in AI search.  [no specificity]
AI search is important for SaaS founders.  [opinion, not observation]
I've been thinking about content structure.  [not an observation]
```

---

### Field 2: Why It Matters to ICP

**What it is:** One sentence connecting the insight to a specific consequence
the ICP (as defined in the active client's config.yaml and
config/icp-psyche.md) feels in their role.

**Framing requirement:**
Written from the ICP's perspective, not the author's.
What does THIS mean FOR THEM, in their situation?

**Template:**
`For a [ICP role], this means [specific consequence in their context].`

**Rules:**
- Must name a specific role or situation from the ICP definition
- Must name a specific consequence (not "this matters")
- Must feel urgent — something happening NOW, not eventually

**Examples — PASS:**
```
For a Series A CEO, this means buyers have already made a vendor shortlist
  before the sales team gets a single inbound call.
For a founder investing in content, this means their budget is producing
  visibility for their competitor's category queries, not their own.
For a Head of Marketing, this means the content team is publishing into
  a vacuum — producing output AI models don't cite.
```

**Examples — FAIL:**
```
This is important for companies thinking about AI.  [vague, no role]
This matters for marketing teams.  [no specific consequence]
AI search is growing fast.  [this is a trend statement, not a consequence]
```

---

### Field 3: Query Mapped To + Category

**What it is:** The specific AI search query this insight should help answer
when it becomes content.

**Process:**
1. Check the active query bank for the closest matching tracked query
2. If a tracked query matches: use it exactly as written
3. If no tracked query matches: write a new query in natural buyer language
   and flag it as NEW (needs to be added to the query bank)

**Query categories and revenue weight:**
- Comparison (highest): "best X for Y", "X vs Y", "X alternatives"
- Solution-aware (high): "how to X", "what is X and how does it work"
- Brand validation (high): "[Brand name] reviews", "is [Brand] good for X"
- Problem-aware (medium): "why is X happening", "what causes X"
- Category leadership (lower): "what is X", "X definition"

**Rules:**
- Query must be written exactly as a buyer would type it
- No marketing language in the query text
- Assign one category only
- Note the revenue weight

---

### Field 4: Content Angle + Hook Type

**What it is:** The specific frame and opening style that makes this insight
worth a reader stopping to read.

**Two sub-fields:**

**Content angle:** 1–2 sentences describing the argument or frame.
Not what the post says — how it says it. What's the editorial position?

**Hook type:** One of four options:
- `specific-observation` — opens with a concrete finding from real work
- `surprising-data` — opens with a counterintuitive statistic
- `contrarian-claim` — opens with a disagreement with conventional wisdom
- `story-moment` — opens with a specific interaction or event

**Selection guide:**
- Evidence = specific number from real work → `specific-observation`
- Evidence = counterintuitive pattern or statistic → `surprising-data`
- Insight = direct contradiction of what competitors say → `contrarian-claim`
- Source = a specific call, conversation, or event → `story-moment`

**POV connection:**
Which POV from the client's POV library does this angle support?
If the insight doesn't connect to a documented POV: note this and
suggest which POV it could extend, or flag for POV library update.

---

### Field 5: Evidence

**What it is:** The specific data point, observation, or experience
that makes the insight credible rather than just an opinion.

**Evidence quality scale:**
- **Strong** (use this): specific number + named context + time reference
  "7 of 10 companies audited this month" / "3 CEO calls in March 2026"
- **Acceptable** (usable but flag): directional observation without full
  specificity — "several companies this week"
- **Weak** (do not proceed without more): vague claim —
  "many companies", "I've noticed"

**Rules:**
- Quote from the source material — do not rephrase or invent
- If evidence is weak: output a WEAK flag and ask for more before completing
- Never invent a statistic or specific to strengthen weak evidence

**If evidence is missing:**
```
EVIDENCE WEAK: No specific data point in the source material.
Options:
A. Add specificity: "How many companies? Which month? What query?"
B. Proceed with weak evidence and acknowledge it in the post's voice
C. Select a different insight that has stronger evidence
```

---

### Field 6: Recommended Format + Channel

**What it is:** The content format and publishing channel best suited
to this insight and query.

**Decision matrix:**

| Query Category | Evidence Strength | Best Format |
|----------------|------------------|-------------|
| Comparison | Strong | LinkedIn post (fastest pipeline impact) |
| Comparison | Strong + complex | Blog post (long-form comparison) |
| Solution-aware | Strong | LinkedIn post or video outline |
| Solution-aware | Strong + process | Blog post |
| Brand validation | Any | LinkedIn post |
| Problem-aware | Any | LinkedIn post |
| Category leadership | Any | Blog post (definitional) |

**Rotation week:**
If this week's rotation is known (Week 1/4 = LinkedIn, Week 2 = Video,
Week 3 = Blog): apply it, unless the query category strongly suggests a
different format — in which case flag the override reason.

---

## Output Format

```
INSIGHT OBJECT
Client: [slug]
Source: [source type]
Date: [date]

---
Field 1 — Insight:
"[one sentence, specific, active, attribution-ready]"

Field 2 — Why It Matters to ICP:
"[one sentence, from ICP perspective, specific consequence]"

Field 3 — Query:
Mapped to: "[exact query text as buyer would type it]"
Category: [comparison | solution-aware | brand-validation | problem-aware | category-leadership]
Revenue weight: [high | medium | low]
Query status: [tracked | NEW — add to query bank]

Field 4 — Content Angle:
Angle: "[1-2 sentences describing the specific frame and argument]"
Hook type: [specific-observation | surprising-data | contrarian-claim | story-moment]
POV connected: "[which POV from library this supports]"

Field 5 — Evidence:
"[exact quote or paraphrase from source material]"
Evidence quality: [strong | acceptable | weak]
[If weak: WEAK FLAG + options]

Field 6 — Format:
Recommended format: [linkedin-post | blog-post | video-outline | newsletter | carousel]
Channel: [LinkedIn | YouTube | Blog | Email]
Rotation week: [1 | 2 | 3 | 4 | override — reason]

---
Status: COMPLETE — pass to [recommended writer skill]
Notion row: [created | failed — paste manually]
[If NEW query: "Add '[query]' to query bank — Category: [category]"]
```

---

## Quality Gate

Before outputting, verify:
- [ ] Field 1 contains exactly one sentence (no "and" connecting two claims)
- [ ] Field 1 passes the attribution test
- [ ] Field 2 names a specific ICP role AND a specific consequence
- [ ] Field 3 query is written in buyer language (not marketing language)
- [ ] Field 5 evidence is quoted from source (not rephrased)
- [ ] Field 5 evidence strength is assessed
- [ ] All 6 fields populated (no empty fields)
- [ ] If evidence is WEAK: flag is present and options are shown

---

## Common Mistakes

- **Compressing two insights into Field 1**: If the insight sentence contains
  "and" connecting two separate observations, split it. Choose the stronger one.
  Two weak observations don't make one strong insight.

- **Field 2 as a restatement of Field 1**: "This means companies are invisible
  in AI search" is a restatement. "For a Series A CEO, this means buyers have
  already shortlisted competitors before the first inbound call" is a consequence.

- **Inventing specificity for Field 5**: If the source says "a few companies,"
  do not write "3 companies." Flag as weak and ask for the real number.
  Invented specificity produces content that can be challenged.

- **Choosing a format from the rotation without checking the query category**:
  If it's Week 3 (blog rotation) but the insight maps to a comparison query
  with strong evidence — the LinkedIn post format may produce faster pipeline.
  Flag the override.

---

## Related Skills

- **insight-scorer**: Always run before this skill — it selects the insight
  this skill structures
- **linkedin-post-writer**: Takes the complete Insight Object as its primary input
- **aeo-page-generator**: Takes the Insight Object for long-form AEO pieces
  (use blog-writer for first-person founder posts)
- **email-agent**: Takes the Insight Object for email content
- When Field 3 generates a NEW query flag, add the query to the tracked
  query bank manually (Notion Query Bank via MCP)
