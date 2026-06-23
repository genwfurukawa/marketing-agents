---
name: youtube-packaging-first
description: End-to-end YouTube video workflow that designs the TITLE + THUMBNAIL FIRST, then writes the script to deliver on that packaging — the inverse of the usual script-then-thumbnail order, matching how top channels actually work. Chains youtube-competitor-research → youtube-idea-validation → packaging lab (title + thumbnail concepts) → packaging gate → script (youtube-script-agent) → production (avatar-video / produce-video) → SEO + publish (youtube-seo-agent, youtube-publish-agent). Use when the user says "make a youtube video the right way", "package this video", "title and thumbnail first", or wants the full idea-to-publish pipeline. Orchestrates existing agents — does not reinvent them.
---

# YouTube Packaging-First — title + thumbnail lead, script follows

The old way: write the video, then slap on a title and thumbnail. The way that wins:
**decide the title and thumbnail FIRST**, validate they'd earn a click, then build the
video to pay off that promise. The thumbnail is the product's cover; nobody watches a video
they don't click. This skill enforces that order and chains the existing tools so nothing
gets reinvented.

## The pipeline (each stage gates the next)

```
Research → Validate → Package → [GATE] → Script → Produce → Optimize → Publish
```

### Stage 1 — Research (foundation)

Run the **`youtube-competitor-research`** skill for the target keyword. You need its
`gap-map.md` + `competitors.json` (real outlier data) before packaging — packaging that
ignores what already wins in the niche is a guess.

### Stage 2 — Validate the idea

Run **`youtube-idea-validation`** on the concept(s). Only a **GREENLIGHT (≥7)** proceeds.
A HOLD goes back for the named sharpen first. Don't package a weak idea into a pretty
thumbnail — that's polishing the wrong thing.

### Stage 3 — Packaging lab (the core of this skill)

Design packaging as a unit. Produce **3 title + thumbnail PAIRS**:

- **Titles** — apply the winning constructions from the gap-map (curiosity gap, stakes,
  number, outcome promise, first-person). Each ≤ ~60 chars, front-loaded. Vary the angle
  across the three, don't just reword one.
- **Thumbnails** — dispatch the **`youtube-thumbnail-agent`** for CTR-driven concepts: one
  clear subject, ≤3 words of text, high contrast, an expression/visual that creates
  tension. The thumbnail and title must **combine, not repeat** — the title says one half,
  the thumbnail shows the other; together they open a loop.
- For each pair, write the **one-sentence promise** the viewer believes when they click.
  That promise becomes the script's contract.

Optionally generate the thumbnail images via the `generate-image` skill / Nano Banana in
the client's brand style so the pair is real, not described.

### Stage 4 — Packaging GATE (human or self-check)

Pressure-test each pair before any script exists:
- Would the target ICP click this over the actual outliers in `competitors.json`?
- Is the promise TRUE and deliverable, or clickbait that will tank retention/trust?
- Does it survive at thumbnail size (squint test — text legible, subject readable)?

Pick the winning pair (or present the top pair + rationale for the user to choose). **Do not
proceed to script until packaging is locked.** This is the whole point of the skill.

### Stage 5 — Script to the packaging

Dispatch **`youtube-script-agent`** with the locked title + thumbnail + promise as the
brief. The script's job is to (a) pay off the exact promise in the hook within ~15-30s and
(b) sustain it. The packaging is now a constraint, not an afterthought — feed it explicitly.
Pull the client voice (`config/voice-guide.md`) per repo rules.

### Stage 6 — Produce

Hand the script to production: **`avatar-video`** (talking-head w/ cloned voice + avatar),
the local **`ai-video`**, or **`/produce-video`** for a footage-based cut. Motion graphics
via `hyperframes`. Out of scope to rebuild — just route to the right one based on format.

### Stage 7 — Optimize + publish

- **`youtube-seo-agent`** — description, tags, chapters, search/suggested optimization.
  (SEO comes AFTER packaging — discovery is secondary to the click, not a substitute.)
- **`youtube-publish-agent`** — full publish package from the final transcript: chapters,
  pinned comment, end-screen plan, captions.

## Output

A handoff doc `clients/<slug>/production/<slug>/packaging.md`: the locked title + thumbnail
pair, the promise, the validation score, and the gap-map evidence behind the choice — so
the script, the editor, and the future retro all share one source of truth.

## Why this order (state it if asked)

CTR and retention are the two numbers YouTube ranks on. Packaging-first optimizes CTR
*before* sinking effort into production, and forces the script to defend retention by
contract. Reversing the order — the common mistake — means discovering after editing that
the video isn't clickable. The loop closes with `youtube-analytics-retro`, which checks
whether the packaging's promised CTR and the script's promised retention actually held.
