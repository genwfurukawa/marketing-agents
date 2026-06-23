---
name: community-seeding
description: "Use when AI answers cite Reddit, Quora, and G2 for your target queries
and you need to show up there — with genuinely helpful, non-promotional answers.
Triggers on: 'seed Reddit for AEO', 'get cited on Reddit/Quora', 'community seeding
plan', 'AI cites Reddit not me', 'find threads to answer', 'G2 reviews for AI search',
'off-site AEO'. Turns entity-authority-agent's seeding PLAN into specific threads +
drafted answers. Hard rule: educational, not promotional — bad seeding gets you
banned and burns trust. Drafts answers for human review; never auto-posts."
metadata:
  version: 1.0.0
---

# Community Seeding

AI answer engines — especially Perplexity and Google AI Overviews — cite community
sources heavily. Reddit, Quora, and G2 are among the most-cited domains for B2B
software queries. `entity-authority-agent` produces a citation-seeding *plan* (which
sources matter); this skill turns it into action: the specific threads to engage and
draft answers that are good enough to earn the citation honestly.

## The Hard Rule

**Educational, not promotional.** AI engines (and community mods) demote and ban
obvious self-promotion. A seeded answer earns its place by being the most genuinely
useful answer in the thread — the brand mention is incidental, disclosed, and
optional. If a draft reads like marketing, it has failed. This is the single most
important constraint; everything below serves it.

This skill **drafts for human review**. It does not post. A human posts from a real
account, with real disclosure where the platform requires it (e.g. Reddit's
self-promotion rules, G2 vendor disclosure).

## Before Starting

You need:
1. **Target queries** — the ones where community sources win citations, from
   `aeo-engine-scan` / the gap matrix. Best inputs are queries where a Reddit/Quora
   thread is the *cited source* and the brand is absent.
2. **The locked entity description + POV** — from `entity-authority-agent` /
   `clients/{slug}/config.yaml`, so any mention is consistent and on-voice.
3. **What's genuinely true** — real product facts, real data, real customer outcomes.
   Never invent capabilities or results to win a thread.

## How It Works

### Step 1 — Find the threads
For each target query, search Reddit/Quora/relevant communities (WebSearch +
WebFetch) for threads where:
- The question matches buyer intent, AND
- The thread ranks / is cited by AI engines or is recent + gaining traction, AND
- A genuinely helpful answer is missing or weak (an opening exists)

Capture per thread: URL, subreddit/community, question, current top answer quality,
age/activity, and the specific angle the brand can add that isn't already covered.
Note community rules (some subs ban vendor participation outright — flag those as
"observe only / earn karma first", don't target them).

### Step 2 — Pick the right surface
- **Reddit** — highest AI-citation weight; also highest self-promo sensitivity. Lead
  with help; mention the brand only if directly relevant and disclosed.
- **Quora** — more tolerant of expert answers with a bio; good for "what is / how to
  / best X" questions.
- **G2 / Capterra** — not threads to answer but reviews/categories to be present and
  accurately represented; recommend the review-generation + category-accuracy actions
  here rather than drafting fake reviews (never draft reviews).

### Step 3 — Draft the answers
For each targeted thread, draft an answer that:
- Leads with the actual answer to the question (3-5 sentences of real substance)
- Uses specifics — numbers, a concrete example, a named tradeoff
- Mentions the brand only if it earns the mention, framed as one option with its
  honest pros/cons (mention a competitor too — balanced answers read as credible and
  survive moderation)
- Discloses affiliation in plain language where the platform expects it
- Matches the founder voice (run the draft past `voice-validator` mentally; no banned
  phrases)

## Output

Write to `clients/{slug}/production/community-seeding/{YYYY-MM-DD}.md`:
1. **Thread targets table** — | query | platform | thread URL | opening | rules note |
2. **Drafted answers** — one per thread, ready for a human to review, personalize,
   and post from a real account
3. **G2/Capterra actions** — accurate category placement, review-request plan (to
   real customers), profile/description consistency — never fabricated reviews
4. **Disclosure + safety notes** — where affiliation must be disclosed; which
   communities to observe-not-post; a reminder to space out activity and build
   genuine account history

## Hand-offs

- Posted answers that earn citations → track via `aeo-engine-scan` /
  `citation-decay-monitor` (did community presence move the needle?)
- Consistent entity mentions → reinforce `knowledge-graph-builder` and
  `entity-authority-agent` descriptions

## Quality Gate

- [ ] Every draft leads with genuine help; brand mention is incidental and optional
- [ ] At least one competitor/alternative acknowledged honestly in comparison answers
- [ ] No invented capabilities, data, or customer results
- [ ] No drafted/fake reviews — G2/Capterra handled as accuracy + real-review requests
- [ ] Disclosure noted where the platform requires it
- [ ] Community rules respected (observe-only subs flagged, not targeted)
- [ ] Drafts are for human posting — this skill never posts
