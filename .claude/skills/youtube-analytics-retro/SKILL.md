---
name: youtube-analytics-retro
description: Diagnose a published YouTube video's performance and extract lessons — CTR vs average view duration vs the retention curve, plus traffic source (browse/search/suggested). Reads a YouTube Studio analytics CSV export (no OAuth needed) and the video's packaging.md, tells you WHICH lever failed (the click, the hook, or the body) and what to change next. Use when the user says "why did this video underperform", "youtube retro", "analyze this video's analytics", "diagnose my CTR/retention", or after a video has run ~7-28 days. Closes the loop on youtube-packaging-first.
---

# YouTube Analytics Retro — diagnose the right lever

A video's outcome decomposes into a few numbers, and each points at a different fix.
Treating "the video flopped" as one problem is why channels don't improve. This skill reads
the actual analytics and isolates **which lever failed**:

| Symptom | Lever | Fix lives in |
| --- | --- | --- |
| Low **CTR** (impressions don't convert) | Packaging — title/thumbnail | `youtube-packaging-first` |
| Low **30s retention** (people leave fast) | Hook | `youtube-script-agent` (intro) |
| Steady **mid-video drop** | Pacing / structure / payoff | script + editing |
| Good CTR + retention, low **impressions** | Topic demand or SEO | `youtube-competitor-research`, `youtube-seo-agent` |
| High **browse** %, low **search** % (or vice versa) | Distribution mix | packaging vs SEO emphasis |

## Inputs (no OAuth required for v1)

1. **Studio CSV export** — in YouTube Studio → the video → **Analytics → Advanced mode →
   Export (CSV)**. Also export the **Audience retention** CSV if available. Ask the user to
   drop the file(s) in the workspace, or paste the key numbers if they can't export.
2. **The packaging doc** — `clients/<slug>/production/<slug>/packaging.md` (the promised CTR
   logic + the script's promised hook). The retro judges *promise vs. reality*.
3. **Niche baseline** — optionally re-run `youtube-competitor-research` so "low CTR" is
   judged against this niche, not a generic 4-6% rule of thumb.

## Diagnosis steps

1. **Pull the headline metrics**: impressions, CTR (impressions click-through rate), views,
   average view duration (AVD) + average percentage viewed, and traffic sources.
2. **Locate the retention cliffs** from the retention CSV: timestamp every drop >3-4% in a
   short span. Map each cliff to what's on screen at that moment in `script.md` — a cliff is
   a specific sentence/segment failing, not a vague "people left."
3. **Isolate the failing lever** using the table above. Be specific: "CTR 2.1% vs niche
   outliers' implied 6%+ → packaging is the bottleneck, not the content" beats "needs work."
4. **Promise vs reality**: did the title/thumbnail promise (from packaging.md) match what
   the first 30s delivered? A click-promise the hook doesn't pay off shows as good CTR +
   bad 30s retention — the most common and fixable failure.

## Output + the compounding step

Write `clients/<slug>/production/<slug>/retro.md`:
- **Scorecard** — CTR, AVD, % viewed, impressions, top traffic source, vs baseline.
- **The verdict** — the ONE primary lever that failed, with the metric that proves it.
- **Retention cliff map** — timestamp → on-screen moment → why they likely left.
- **Next-video changes** — 2-3 concrete, testable changes routed to the owning skill
  (e.g. "tighten hook to pay off the thumbnail promise by 0:08" → next script brief).

Then **write a lesson to `lessons.md`** per the repo's self-improvement protocol — a flopped
or winning video is exactly the trigger ("published content underperforms"). If a pattern
repeats (e.g. thumbnails consistently over-promise), update the owning skill/agent prompt,
not just the log.

## Upgrade path (out of scope for v1)

Live pull via the **YouTube Analytics API** (OAuth2) would remove the manual CSV export.
Documented so the path is clear; v1 stays OAuth-free on purpose so it works the day you ask.
