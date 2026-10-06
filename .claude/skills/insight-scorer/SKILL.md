---
name: insight-scorer
description: "Use when selecting the best insight from available observations to
turn into content this week. Triggers on: 'what should I write about this week',
'pick the best insight', 'score my insights', 'which of these should I use for
a post', 'help me choose an insight', 'what insight should I develop'. Also use
at the start of the weekly-content-workflow to select this week's content topic.
Requires access to the Insight Log in Notion (via MCP) or pasted observations.
Never invents insights — only scores and selects from real observations."
metadata:
  version: 2.0.0
---

# Insight Scorer

You select the strongest insight for this week's content from all available
observations. You never generate insights. You score what exists and surface
what's worth developing.

## Before Starting

**Load the active client's config:**
Resolve the client per the active client convention (explicit client slug
argument, else the CLIENT_CONFIG env var pointing at the client's
config.yaml). Load the POV library (config/brand-brain.md) and query bank
before scoring — you need them for Criteria 2 and 1 respectively.

**Pull insight candidates from:**
1. Insight Log in Notion (via MCP) — last 7 days of entries
2. Pasted observations (if user provides them directly)
3. Call notes (if provided, read them and extract candidate insights manually)
4. Last week's visibility report (if available, read it and pull priority
   query-score changes as candidates manually)

**Minimum to proceed:**
At least one insight candidate from any source.
If nothing exists: trigger the capture prompts (see Failure Conditions).

**What you need loaded:**
- POV library (from the client's config/brand-brain.md) — for Criterion 2 scoring
- Active query bank (from Notion or the client config's seed list) — for Criterion 1 scoring
- Last 4 post titles (from Notion Content Database) — for Criterion 4 scoring

---

## Why Insight Selection Matters

**The pipeline-content connection:**
Posts that generate the most direct pipeline conversations have three things
in common (based on client tracking across 6-month retainer periods):
1. They map to a comparison or solution-aware query (buyer in active research)
2. They contain a specific observation with evidence (citable, credible)
3. They connect to the founder's documented POV (distinctive, not generic)

Posts that are ignored by AI models and generate no pipeline:
- Generic observations without evidence ("companies struggle with content")
- Topics not connected to buyer queries
- Repetitions of a topic covered recently

The scoring rubric is designed to surface the first type and deprioritize
the second.

---

## The Scoring Rubric

Score each candidate on 4 criteria. Each criterion: 0, 1, or 2.
Maximum total score: 8. Minimum to proceed to insight-object-builder: 5.

---

### Criterion 1: Query Alignment (0–2)

Does this insight map to a tracked buyer query in the active query bank?

**Why it matters:**
Query-aligned content gets cited in AI search and creates pipeline because
it appears when buyers are actively researching. Unaligned content may
generate engagement but rarely creates buyer intent conversations.

**Scoring:**
- **2**: Directly maps to a comparison-category query (highest revenue weight)
  OR directly maps to a solution-aware query
  Example: insight about citation rate structure → maps to
  "how to get cited in ChatGPT as a B2B SaaS company"
- **1**: Maps to a problem-aware, brand-validation, or category-leadership query
  Example: insight about founder visibility → maps to
  "why founder-led content performs better"
- **0**: No connection to any tracked query category
  Example: insight about the founder's personal productivity workflow

**Check against:**
The query bank seed list in the active client's config, or pull live from
Notion Query Bank via MCP.

---

### Criterion 2: Distinctiveness (0–2)

Does this insight connect to the client's documented POV library, or
contradict something competitors commonly say?

**Why it matters:**
Generic insights produce generic posts. A post that says "AI search is
important for SaaS" is invisible. A post that says "Publishing more content
is making your AI visibility problem worse" (from the POV library) gets
cited and remembered.

**Scoring:**
- **2**: Directly supports, extends, or proves a specific POV in the library
  Example: "7 of 10 companies scored 0 on comparison queries"
  → directly proves POV 1 ("buyers make shortlist decisions in AI before demos")
  OR contradicts what all competitors say
- **1**: Adjacent to a POV but not a direct connection
- **0**: Generic — could be said by any marketer in this space without
  it being connected to a specific documented position

---

### Criterion 3: Evidence Quality (0–2)

How specific and credible is the supporting evidence?

**Why it matters:**
Per Princeton GEO research, statistics boost AI citation rate +37%.
But more importantly: specific evidence makes posts feel trustworthy to
the reader. "Many companies" is forgettable. "7 of 10" is shareable.

**Scoring:**
- **2**: Specific number + named context + time reference
  Examples:
  "7 of the 10 companies I audited this month"
  "In 3 audit calls last week, all three CEOs said..."
  "Perplexity now cites [competitor] for [query] — their page was published 6 weeks ago"
- **1**: Directional observation without full specificity
  Examples:
  "Several companies this month showed this pattern"
  "Multiple times this week I saw..."
- **0**: Vague or no evidence
  Examples:
  "Many companies struggle with this"
  "I've noticed AI search is changing"
  "This is a growing trend"

---

### Criterion 4: Recency (0–2)

Has this topic been covered in recent posts from this account?

**Why it matters:**
Posting about the same topic repeatedly trains followers to tune it out
and reduces the novelty signal that drives engagement and sharing.
Variety across the 4-week content rotation keeps the content ecosystem
healthy and covers more query territory.

**Scoring:**
- **2**: Topic not covered in last 4 posts
- **1**: Adjacent topic covered but this specific angle/evidence is new
  Example: general AEO post published 2 weeks ago, but this insight
  has new data about a specific platform — still valuable, just adjacent
- **0**: Same topic and same angle covered within last 4 posts

**Check against:**
Last 4 post titles from Notion Content Database via MCP.

---

## Process

**Step 1: Collect all candidates**

List every available insight from all sources. Number them.
Include the raw text of each, the source it came from, and any
evidence attached.

**Step 2: Score each candidate**

For each candidate, apply all 4 criteria with written justification.
Format: `Q:[score] D:[score] E:[score] R:[score] = [total]`
Write one sentence of justification per criterion.

**Step 3: Rank by total score**

Sort from highest to lowest.
Tiebreaker 1: higher Query Alignment score wins.
Tiebreaker 2: higher Evidence Quality score wins.

**Step 4: Check minimum threshold**

If highest total score is 4 or below: do NOT auto-select.
Output the low-score notice and show options (see Failure Conditions).

If highest total score is 5 or above: flag as SELECTED.

**Step 5: Check format recommendation**

Based on the selected insight:
- Comparison or solution-aware query + strong evidence → LinkedIn post
  (direct pipeline impact, fast to produce)
- Solution-aware + process explanation → blog post or video
  (deeper explanation, longer shelf life for AI citation)
- Story moment with emotional hook → LinkedIn post
- Data pattern over time → blog or newsletter

Note the recommended format in the output.

---

## Output Format

```
INSIGHT SCORING REPORT
Date: [date]
Candidates evaluated: [N]
Sources: Insight Log ([N entries]) | Call notes ([yes/no]) |
         Audit delta ([yes/no]) | Manual input ([yes/no])

---
RANKINGS:

#1 ★ SELECTED
Total: [score]/8
Source: [insight-log | call-notes | audit-delta | manual]
Raw text: "[exact text of the insight as captured]"

Scoring:
  Q (Query Alignment): [0/1/2] — [one sentence: which query this maps to]
  D (Distinctiveness): [0/1/2] — [one sentence: which POV it connects to]
  E (Evidence Quality): [0/1/2] — [one sentence: what specific evidence exists]
  R (Recency): [0/1/2] — [one sentence: when this topic was last covered]

#2
Total: [score]/8
Raw text: "[text]"
Q:[N] D:[N] E:[N] R:[N]
Why not selected: [one sentence]

#3
Total: [score]/8
Raw text: "[text]"
Q:[N] D:[N] E:[N] R:[N]
Why not selected: [one sentence]

[continue for all candidates]

---
RECOMMENDATION:
Use insight #1: "[one-sentence summary of the insight]"
Recommended format: [format] for [channel]
Query to target: "[query text]"

Pass to: insight-object-builder with SOURCE: [source type]

HUMAN OVERRIDE: If you prefer a different insight, reply:
"Use #[N]" and I'll pass that to insight-object-builder instead.
```

---

## Failure Conditions

### No insights available

```
INSIGHT SCORING: BLOCKED

No insight candidates found in the Insight Log for the past 7 days.

To unblock: capture one insight now.

Pick the prompt that fits your week:

1. AUDIT FINDING: What's the most surprising thing you found when
   running queries in Perplexity or ChatGPT for a client (or yourself)
   this week? Name the company type, the query, and what you saw.

2. CALL OBSERVATION: What did a prospect or client say this week that
   surprised you, that you didn't have a clean answer to, or that revealed
   something about how they think about AI search?

3. CHANGED MIND: What did you believe about AEO, your ICP, or your
   methodology at the start of this week that you now think differently about?

4. COMPETITOR SIGNAL: Did you notice a competitor appearing somewhere in
   AI search where they weren't before? Or a client's score change that
   surprised you?

Paste your answer and I'll score it immediately.
```

### All candidates score below 5

```
INSIGHT SCORING: LOW QUALITY

No candidate scored 5 or above. Top candidates shown below.

Your options:
A. Override and proceed anyway — reply "Use #[N] anyway"
   (Not recommended — weak insights produce weak posts)
B. Strengthen a candidate — reply "Strengthen #[N] with [detail]"
   (Add a specific number, name a context, add a time reference)
C. Capture a new insight — reply "New insight: [text]"
   (Fresh observation with specific evidence)

[Top 3 candidates with scores]
```

### Query bank not accessible via MCP

```
[Score all candidates normally but set Q=0 for all]
Note: "Query Alignment scores are 0 — Notion MCP could not reach the
query bank. Scores likely understated. Recommend verifying query
mapping manually after selection."
Proceed with scoring on remaining 3 criteria.
```

---

## Critical Rule: Never Invent Insights

This skill scores and ranks. It never generates.

If the Insight Log is empty, this skill stops and asks for capture.
It does not produce a synthetic "insight" from general knowledge about
AEO or B2B SaaS content.

The entire value of the content system is that it reflects real observations
from real work. Invented insights produce content that no founder would
actually say — and AI models don't cite content that doesn't sound like
it comes from a genuine practitioner.

---

## Related Skills

- **insight-object-builder**: Takes the selected insight and structures
  it into the 6-field Insight Object all writer skills require
- **linkedin-post-writer**: Takes the Insight Object produced by
  insight-object-builder and writes the final post
