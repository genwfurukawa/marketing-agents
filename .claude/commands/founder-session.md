---
description: Turn a 30-minute founder transcript into 8-12 atomic insights, scored and queued for cross-channel content production (16+ LinkedIn posts, 4 articles, video scripts, carousels).
argument-hint: --transcript /path/to/transcript.txt [--client client-slug] [--queue-days 30] [--video-source /path/to/recording.mp4]
allowed-tools: Task, Bash, Read, Write, Edit, Glob, Grep, WebFetch
---

# Founder Session

You convert a single 30-minute founder transcript into a full 30-day content queue. This is the highest-leverage input in the methodology: one session feeds 16+ LinkedIn posts, 4 long-form articles, 8+ emails, video scripts, and carousels.

This command is the front-end intake for the insight-capture pipeline. Run it on every retainer client monthly. Run it on yourself first.

---

## Why This Command Exists

The system has insight-capture, insight-scorer, insight-object-builder, and produce-weekly-content. What was missing: the intake that turns a raw transcript into the queued atoms those skills consume.

Before this command, founder sessions happened ad-hoc and atoms got lost. After this command, every session lands in `clients/{slug}/research/founder-sessions/{YYYY-MM-DD}/` with traceable atom IDs that flow through to published content.

---

## Inputs

Required:
- `--transcript` - path to a transcript file (txt, md, or Descript .json export)

Optional:
- `--client` - client slug (defaults to the active client: `CLIENT_CONFIG` env var pointing at the client's config.yaml)
- `--queue-days` - days of content to queue out (default 30)
- `--video-source` - if a video recording exists, link it for downstream YouTube clip extraction
- `--pillar` - bias atom selection toward one pillar (default: distribute across the client's pillars per `clients/{client}/config/pillars.md`)

---

## Process

1. **Read the transcript.** Handle txt/md directly. For Descript .json, extract speaker-tagged text.

2. **Read context in parallel:**
   - `clients/{client}/config.yaml`
   - `clients/{client}/config/voice-guide.md`
   - `clients/{client}/config/icp-psyche.md`
   - `clients/{client}/config/pillars.md`
   - `clients/{client}/config/brand-brain.md`
   - `lessons.md`

3. **Invoke `insight-capture-agent`** with the transcript. Output: 8-15 atomic insights (quotes, stories, frameworks, data points, contrarian beliefs).

4. **Invoke `insight-scorer` skill** on each atom. Score on:
   - Pillar alignment (which of the client's pillars + strength)
   - Specificity (named entities, numbers, mechanisms)
   - Contrarian potential (does it challenge conventional thinking?)
   - Citation potential (is it framework-worthy?)
   - ICP relevance

5. **Invoke `insight-object-builder` skill** on the top 8-12 atoms. Output: structured insight objects with topic clusters, supporting evidence, and recommended formats.

6. **Map atoms to content formats.** Use this default ratio per session:
   - 8-12 LinkedIn posts (1.5-2x per atom)
   - 2-4 long-form articles or AEO pages
   - 4-8 emails (3-5 per long-form)
   - 2 YouTube scripts (if `--video-source` present, 1 short + 1 long)
   - 1-2 carousels (most quotable atoms)

7. **Create a content calendar** for `--queue-days` (default 30) with each piece tagged to:
   - Source atom ID
   - Pillar
   - Channel
   - Suggested publish date
   - Status: `queued`

8. **Optional: surface 2-3 POV/framework candidates.** Flag any atom that could become a named-framework post ("The 9-Step Visibility System", "The 30-Minute Founder Session"). These are the highest-citation authority content per the AEO playbook.

9. **Notion sync.**
   - Append all atoms to Insight Log DB
   - Append all queued pieces to Content Calendar DB

10. **Output structure:**

```
clients/{slug}/research/founder-sessions/{YYYY-MM-DD}/
  transcript.txt                  (copied from source)
  atoms.json                      (raw extracted atoms with scores)
  insight_objects.json            (top atoms structured for production)
  content_queue.md                (30-day calendar, human-readable)
  content_queue.csv               (machine-readable for Notion import)
  pov_candidates.md               (framework / contrarian post candidates)
  notes.md                        (anything Gen flagged manually during session)
  video_source.txt                (link to recording if --video-source passed)
```

---

## What Comes Next

After this command runs, the user has three options:

1. **Run `/produce-weekly-content` immediately** to generate Week 1 drafts from the top atoms.
2. **Trickle production** via the Notion task loop (see docs/OPERATING.md) - queue atoms as tasks and produce them week by week.
3. **Review and override** the queue manually before drafts are generated (recommended for the first session).

---

## Critical Rules

1. **Top atoms only.** Never queue more than 12 atoms per session even if more were extracted.

2. **Voice rules apply at extraction.** The insight-capture agent reads `clients/{client}/config/voice-guide.md` - atoms must sound like the founder, not like AI summaries.

3. **POV candidates are precious.** Most sessions produce 0-2 framework-worthy atoms. If you flag 5+, you're being lenient. Lower the bar = lose the authority play.

4. **Never publish from this command directly.** This command queues. Production happens via `/produce-weekly-content` with its own quality gates.

5. **Notion sync is mandatory.** Skipping it loses traceability between session -> atom -> published piece. The pipeline depends on it.

6. **One session per month, minimum.** If a client hasn't had a session in 30 days, the engine starves. Flag it in the next monthly briefing.

7. **Use the video source if available.** Pipe the path to `youtube-publish-agent` or `youtube-script-agent` downstream. A 30-minute video = 4-6 clip candidates + 1-2 long-form scripts.

---

## Related

- Capture: `insight-capture-agent`
- Scoring: `insight-scorer` skill
- Object building: `insight-object-builder` skill
- Production: `/produce-weekly-content`
- Video downstream: `youtube-publish-agent`, `youtube-script-agent`
- Insight log + content calendar: Notion DBs via MCP

---

## First-Run Suggestion

Before running on a client, run on yourself:

```
/founder-session --transcript ~/Desktop/my_voice_memo_2026-05-11.txt
```

Validate the output is high-quality, then offer the same flow to retainer clients as the monthly Founder Voice Session ($1,500 standalone wedge product if not on retainer).
