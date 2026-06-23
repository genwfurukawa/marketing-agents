---
name: youtube-idea-validation
description: Score a YouTube video idea BEFORE scripting it — go/no-go on whether it's worth making. Grades a concept on Demand, Breadth, Outlier potential, Personal angle, and Production feasibility (0-2 each, threshold 7/10), grounded in youtube-competitor-research data. Use when the user says "is this video idea worth making", "validate this youtube idea", "score these video concepts", or before /produce-video or youtube-packaging-first. Stops you spending production effort on ideas nobody searches for or that can't outperform the niche.
---

# YouTube Idea Validation — score before you script

The #1 lever in YouTube is idea selection, not production. A perfectly produced video on a
dead idea fails; a roughly produced video on a great idea wins. This skill is the gate:
score the idea against real demand and outlier data, give a go/no-go, and only pass winners
downstream. Sibling of `insight-scorer` — same 0-2 rubric discipline.

## Inputs

- **The idea(s)** — one or more video concepts (a title or a one-line premise). Ask if none.
- **Competitor data** (strongly recommended) — the `youtube-competitor-research` output for
  the relevant keyword (`competitors.json` + `gap-map.md`). If it doesn't exist, run that
  skill first; scoring without it is guesswork and you must say so.
- **Client context** — `clients/{slug}/config.yaml` + `config/icp-psyche.md`, so "breadth"
  and "personal angle" are judged against THIS creator and audience.

## The rubric (0-2 each, max 10, threshold 7 to greenlight)

Score conservatively. When uncertain, score lower — same rule as the other scorers.

1. **Demand (0-2)** — is anyone looking for this / does it ride a real interest?
   - 2: clear search or topical demand (outliers exist for the keyword, or it's a rising trend).
   - 1: niche but real audience.
   - 0: no evidence anyone wants this.

2. **Breadth (0-2)** — how big is the addressable audience beyond the hardcore niche?
   - 2: broad appeal, clickable to a cold browse audience.
   - 1: appeals to the core niche only.
   - 0: inside-baseball, tiny ceiling.

3. **Outlier potential (0-2)** — can this BEAT the niche baseline, not just match it?
   - 2: an angle/packaging that the gap-map shows is unexploited AND demonstrably works.
   - 1: solid but in a saturated lane against big channels.
   - 0: a wall of 20x+ mega-channel incumbents with no opening.

4. **Personal angle / credibility (0-2)** — can THIS creator make it uniquely well?
   - 2: direct experience, proprietary data, or a real contrarian POV they can defend.
   - 1: competent but commodity take.
   - 0: off-brand or no credibility to claim it.

5. **Production feasibility (0-2)** — can it be made well with the available stack?
   - 2: fits the format/tools (e.g. avatar-video / hyperframes) at reasonable cost.
   - 1: makeable but heavy.
   - 0: needs footage/resources you don't have.

## Output

For each idea write a compact verdict:

```
IDEA: <title/premise>
SCORE: 8/10  →  GREENLIGHT   (or HOLD / KILL)
  Demand 2 · Breadth 2 · Outlier 1 · Angle 2 · Feasibility 1
WHY: <2-3 sentences grounded in specific competitor/outlier evidence>
SHARPEN: <the one change that would raise the lowest dimension — e.g. a tighter angle,
         a more searchable framing, a format swap>
```

Rules:
- **GREENLIGHT ≥7**, **HOLD 5-6** (fixable — name the fix), **KILL ≤4**.
- Cite real numbers from `competitors.json` ("the top 3 outliers here are all 8x+ and none
  cover X") — never assert demand you can't evidence.
- If asked to rank a batch, sort by score and lead with the single best bet + why.
- A greenlit idea hands to `youtube-packaging-first` (or `/produce-video`). A HOLD goes
  back with the specific sharpen. Don't pass borderline ideas — the gate only works if it bites.
