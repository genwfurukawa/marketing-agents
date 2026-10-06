---
name: youtube-competitor-research
description: Deep competitor research for a YouTube keyword/topic using the YouTube Data API. Pulls the top-performing videos for a keyword, computes OUTLIER MULTIPLES (views vs each channel's recent median — the real signal of what overperformed), tears down their packaging (title patterns, thumbnail tactics, hook + structure), and outputs a competitive gap map. Use when the user says "research youtube competitors", "what's working on youtube for [keyword]", "find outlier videos for [topic]", or as the first step before validating an idea or packaging a video. Deeper than WebSearch-only competitor research, this uses real view/velocity/outlier data from the API.
---

# YouTube Competitor Research — keyword → outlier teardown → gap map

The job: for a keyword, find the videos that *overperformed* (not just the most-viewed),
reverse-engineer why they won (packaging, hook, structure), and surface the gaps you can
exploit. **Outlier multiple — a video's views ÷ its channel's recent median views — is the
core signal.** A 500k-view video on a 2M-median channel underperformed; a 500k-view video
on a 20k-median channel is a 25x outlier screaming "this idea/packaging works." WebSearch
can't see this. The YouTube Data API can.

## Setup gate (first run)

Needs a free YouTube Data API key. If `scripts/youtube/yt_api.py` errors on the key, STOP
and walk the user through [setup.md](setup.md).

## Inputs

- **Keyword / topic** (required) — what the audience searches. Ask if missing.
- **Client** (for output routing + ICP context) — read `clients/{slug}/config.yaml` and
  `config/icp-psyche.md` so "gap" means *a gap that matters to this ICP*, not any gap.
- **Window** (optional) — `--days N` to bias toward recent/trending; omit for all-time.

## Step 1 — Pull the data (the part only the API can do)

```bash
python3 scripts/youtube/yt_api.py research \
  --query "<keyword>" --max 40 [--days 180] \
  --out clients/<slug>/research/youtube/<keyword-slug>/
```

Writes `competitors.json` + `competitors.csv`, sorted by outlier multiple, with per-video
views, views/day (velocity), engagement rate, channel subs, channel median, and age.
Read the JSON.

**Discard `likely_paid` videos when teaching packaging.** The engine flags any video with
≥10k views and <0.5% engagement ((likes+comments)/views) as `likely_paid` and sinks it below
organic results - a high-view video with dead engagement was served as a YouTube ad, so its
outlier multiple is bought, not earned. It tells you nothing about what packaging or ideas
win organically. Genuine organic videos in a healthy niche run ~2.5-4% engagement. Only
tear down packaging from organic outliers; mention flagged-paid videos only as "a competitor
is running paid on this topic," never as a packaging model to copy.

Run 2-4 adjacent keyword variations (the head term + the way real people phrase it) and
union the results — one query misses the long tail.

## Step 2 — Packaging teardown (why they got the click)

For the top ~10 outliers, analyze packaging — this is where the wins are:

- **Titles** — cluster the patterns. Curiosity gap? Number? Negativity/stakes? Outcome
  promise? "How I…" first-person? Note the exact constructions that recur among outliers
  but NOT among the underperformers. That delta is the formula.
- **Thumbnails** — `WebFetch` the `thumbnail` URL (or use `/browse` per the user's global
  rule — never chrome MCP) and describe each: face/expression, ≤3-word text, color
  contrast, subject, what the thumbnail+title promise *together* (they should not repeat
  each other — they should combine).
- **Length + velocity** — note duration and views/day. Fast velocity on a young video is a
  stronger signal than high lifetime views on an old one.

## Step 3 — Hook + structure teardown (why they kept the view)

For the top 3-5 outliers, get the transcript (`/browse` the watch page or a transcript
source) and extract:
- The **first 15-30s hook** verbatim — what promise/tension opens it.
- The **structural beats** — how they sequence, where they re-hook, the payoff.
- Recurring **format** (listicle, single-narrative, tutorial, reaction, doc-style).

Don't transcribe everything — sample the outliers; that's where the replicable patterns are.

## Step 4 — Gap map (the deliverable)

Write `clients/<slug>/research/youtube/<keyword-slug>/gap-map.md`:

1. **Outlier leaderboard** — top 10 by multiple: title, channel, outlier×, velocity, the
   one-line "why it won."
2. **Winning packaging formula** — the title constructions + thumbnail tactics that
   separate outliers from the pack, stated as reusable rules.
3. **Hook/structure patterns** — the formats that retain, with verbatim hook examples.
4. **Gaps to exploit** — for THIS ICP: angles nobody covered, packaging nobody tried,
   questions the top videos left unanswered, formats absent from the niche. Rank by
   (demand signal × how exploitable). These feed `youtube-idea-validation`.
5. **Saturation read** — is this keyword winnable, or is it a wall of 50x mega-channels?
   Say so plainly; a great gap map sometimes says "don't compete here, go adjacent."

## Hand-off

- `youtube-idea-validation` scores concepts against this gap map's outlier baseline.
- `youtube-packaging-first` builds title/thumbnail concepts from the winning formula.
- Never fabricate view counts or outlier numbers — every figure traces to `competitors.json`.
