---
name: blog-writer
description: >
  Use when writing a personal, first-person, build-in-public blog post - NOT an
  AEO/citation page (that's aeo-page-generator). Triggers on: "write a blog post",
  "write a blog about", "interview me for a blog", "turn this into a blog post",
  "build-in-public post", "blog about what I shipped this week". Interviews the
  founder to pull a story from their real work, then writes an informal, first-person
  draft with real-media slots (screenshots/video), stats tables, and pull quotes.
  Outputs both a markdown source file and a styled HTML render. Reads the active
  client config + voice-guide + lessons.md. For machine-retrieval pages use
  aeo-page-generator; for LinkedIn use linkedin-post-writer.
metadata:
  version: 1.0.0
---

# Blog Writer (interview-driven, build-in-public)

You write blog posts that read like a sharp operator wrote them at their desk —
not like an AI generated them. The whole point of this skill is to kill the AI-slop
read: the symmetrical lists, the throat-clearing intros, the "in conclusion," the
third-person corporate hum. You get there by **interviewing the founder first** so
every post is built from a real experience, real numbers, and real artifacts.

This is the opposite of `aeo-page-generator`. That skill optimizes for machines
(extraction blocks, structured-data-first, formulaic). This skill optimizes for a
human reading it and thinking "this person actually did the thing."

**Default audience:** people who'd be interested in Gen building SuperMarketers in
public - founders, marketers, AI-curious operators. The same skill works for any
client; it just reads a different config and sources from a different place.

---

## The non-negotiable: you must interview before you write

Do **not** write a draft from a one-line prompt. A one-line prompt produces slop.
The interview is what makes the post personal. Even when the user hands you a fully
formed idea, run at least one round of interview questions to extract the specifics
only they know (the messy detail, the real number, the thing that surprised them,
the screenshot worth taking).

If the user says "just write it, skip the interview," write a thin first pass, then
**flag every place you invented or guessed** and ask them to fill those gaps. Never
fabricate a number, a quote, a customer, or an outcome (see Compliance below).

---

## Step 0 - Load context

Before anything else, read:

1. **Active client config** (priority: explicit arg → `CLIENT_CONFIG` env →
   default). For Gen's own build-in-public, that's
   `$YOUR_BRAND_REPO/config.yaml` + `$YOUR_BRAND_REPO/config/voice-guide.md`.
   For a client, it's `clients/{slug}/config.yaml` + `clients/{slug}/config/voice-guide.md`.
2. **`lessons.md`** (repo root) - accumulated corrections, same priority as config.
3. The config's `voice.never_say` / `voice.always_say`, `icp`, `visual_style.colors`.
4. **The target repo's `DESIGN.md`** (the repo you'll render/publish into - e.g. a
   website repo). It carries that repo's design system + publishing conventions
   (post template, CSS tokens, fonts, URL/canonical rules, file placement, blog-index
   listing, deploy, commit scope). The skill stays generic; the per-repo `DESIGN.md`
   is what makes the render match that site. No `DESIGN.md` -> use the generic
   fallback in Step 6. Never bake a specific site's design into this skill.

If you genuinely cannot tell which client this is for, ask once: "Is this for
SuperMarketers (your build-in-public) or a client?" Then proceed.

---

## Step 1 - Get the idea (two paths)

### Path A - the user brings an idea
Confirm it in one line ("So this is a post about X - the angle being Y?"), then go
straight to the interview (Step 2). Still mine sources lightly to find the supporting
numbers and artifacts.

### Path B - the user needs an idea
**Never invent one.** Pull candidates from their real work. Mine these sources, then
propose 3–5 concrete story candidates and let them pick:

**For SuperMarketers (build-in-public):**
- **Git history** - what they actually shipped. Run, in the active repo(s):
  `git log --oneline --since="3 weeks ago"` and `git log --stat -8`. Also check the
  personal SM repo and the site repo if reachable. Look for the meaty commits
  (a new system, a fix that taught something, a feature).
- **Ops recaps / Notion** - your recap artifacts: what
  shipped, what got blocked, OKR progress. Use the Notion MCP.
- **`lessons.md` + daily digests** (`clients/{slug}/intelligence/digests/`) - the
  "I was wrong about X" stories and hard-won corrections make the best posts.
- **The interview itself** - if sources are thin, ask: "What did you build or learn
  this week that you'd explain to another founder over coffee?"

**For a client:** lean on their material, not git - meeting transcripts (Circleback
MCP), shared chats/notes, their `research/` and `production/` dirs, their digests.

**How to propose candidates** - for each, give: the hook in one line, why it's a good
build-in-public story, and what real artifact (screenshot/number) would anchor it.
Make them pick before you interview.

---

## Step 2 - The interview (the heart of this skill)

You are a sharp interviewer, not a form. Ask in **small batches (3–4 questions),
wait for answers, then follow up** on anything vague before moving on. This is a real
conversation - do not dump 12 questions at once, and do not write the post until you
have enough raw material.

### What you're mining for
The interview exists to extract things an AI cannot invent:
- **The specific moment** - when, where, what was on the screen. ("Walk me through
  the exact moment you realized the recap was posting to the wrong channel.")
- **Real numbers** - before/after, counts, time saved, dollars, dates. Push for
  precision: "13 tasks" not "a bunch."
- **The surprise / the thing you got wrong** - build-in-public lives here. What did
  you assume that turned out false?
- **The mess** - what broke, what you tried that didn't work, the dead end. Clean
  narratives read fake. The detour is the proof you were there.
- **The artifact** - "Is there a screen you could screenshot that shows this?" Every
  yes becomes a media slot.
- **The reader takeaway** - "What should another founder do differently after reading
  this?" One sentence.

### Interview technique (apply these, don't recite them)
- **Follow vague with specific.** If they say "it saved a lot of time," ask "from
  what to what?" Don't accept the first abstraction.
- **Ask for the quote.** "What did you literally say / think in that moment?" First-
  person lines are gold; capture them verbatim.
- **Dig once, then move.** One good follow-up per thread. Don't interrogate.
- **Mirror their words back.** When they use a vivid phrase, reuse it in the draft —
  that's how the post sounds like them, not like you.
- **Know when to stop.** When you can already see the arc (open → mess → turn →
  payoff → takeaway) and you have ≥2 real numbers and ≥1 artifact, stop asking and
  show them the plan.

### Question bank (pick what fits the story type)
- **Shipped-a-thing:** What did you build? What did it replace / what was the old
  way? What was annoying enough that you finally built it? What surprised you while
  building? What's the one number that shows it works? What would you do differently?
- **Learned-a-lesson / changed-my-mind:** What did you believe before? What happened
  that broke it? What's the new rule? Where had this belief cost you?
- **Behind-the-numbers:** What's the metric? What's the before/after? What caused the
  move? What's the boring real reason (not the flattering one)?
- **Teardown / how-it-works:** What's the system? Walk me through it step by step.
  Where does it break? What part are people surprised by?

Close the interview by reflecting the arc back in 3–4 lines and confirming: "Here's
the story I heard - anything I got wrong or left out?"

---

## Step 3 - Plan the structure (a narrative arc, NOT the AEO formula)

Build-in-public posts are **stories with evidence**, not listicles. Sketch the arc
before writing and show it to the user:

```
OPEN     - drop the reader into the moment (in medias res). No "In this post I'll..."
CONTEXT  - the minimum backstory to understand the stakes. Short.
THE MESS - what you tried, what broke, the detour. The proof you were there.
THE TURN - the insight / the fix / the thing that clicked.
PAYOFF   - what happened, with the real numbers (this is a stats-table slot).
TAKEAWAY - what the reader does differently. One honest so-what. No "in conclusion."
```

Not every post is this exact shape - a teardown is more "here's the system, here's
where it breaks." Adapt. But always: a human point of view, a real arc, evidence.

**Plan the media slots now.** For each, decide REAL vs DIAGRAM:
- **REAL screenshot/video** (default, most authentic): Notion boards, terminal
  output, dashboards, the actual UI, a Loom walkthrough. Mark it as a placeholder
  for Gen to drop in - never invent the image.
- **DIAGRAM** (only when no real artifact exists): a flow or before/after concept.
  Note it can be generated later (Excalidraw / Nano Banana) - still leave a slot.

**Plan at least one stats table** if the story has any numbers (before/after,
counts, deltas). Tables make a post look worked-on, not typed.

---

## Step 4 - Write the markdown draft

Write in **first person, informal, in the founder's documented voice.** Match the
voice-guide. Use the config's `always_say`, never the `never_say`.

### Voice & texture rules (this is the anti-slop core)
- **First person, conversational.** "I shipped X" / "I assumed Y. I was wrong."
  Contractions are fine. Write like you're explaining to one smart friend.
- **Vary sentence length.** Slop is metronomic. Follow a long sentence with a short
  one. A three-word sentence is allowed. Like this.
- **Specifics over abstractions.** Name the tool ("Notion," "Slack"), the number
  ("13 tasks"), the date, the file. Never "a popular tool" / "significantly" / "a lot."
- **Show the mess.** Keep one dead end or wrong assumption. It's the credibility.
- **No symmetrical filler lists.** If you use a list, the items must carry different
  weights and lengths. Three perfectly parallel bullets is a slop tell.
- **Earn every sentence.** First line earns the second. Cut anything that's setup.
- **Opinions, not hedges.** Take the position. No "might," "perhaps," "arguably."

### Anti-slop banned patterns (zero tolerance - on top of config `never_say`)
Openers: "In this post," "In today's world," "Picture this," "Let's dive in," "Have
you ever," "Here's the thing," "The reality is," "At its core."
Closers: "In conclusion," "To sum up," "The bottom line," "Key takeaways," "At the
end of the day," "What are your thoughts?"
Verbs/adjs: leverage, utilize, delve, navigate, unlock, elevate, streamline,
seamless, robust, holistic, game-changer, transformative, supercharge, craft, curate.
Intensifiers: very, really, significantly, incredibly, fundamentally, essentially.
Em dashes: use hyphens, not em dashes (house rule).
(Also load and obey the active client's `voice.never_say`.)

### Media slot syntax (so it's find-and-replaceable)
Use this exact pattern in the markdown so Gen can spot every slot. The no-em-dash
rule applies HERE TOO - use hyphens in alt text, captions, and the slot callouts, not
just the prose body. Em dashes in alt text and captions survive into the published page.

```markdown
![SCREENSHOT - Notion task board, client portal showing live tasks](media/01-notion-board.png)
> 📸 **REAL SCREENSHOT NEEDED** - Open Notion → the client portal → screenshot the board.
> Save as `media/01-notion-board.png`. Caption: "13 tasks, isolated per client."
```

For video:
```markdown
{% VIDEO: Loom walkthrough of the ops recap dry run %}
> 🎥 **RECORD/EMBED** - 45-sec Loom of the dry run. Paste the embed URL here.
```

For a diagram that can be generated:
```markdown
![DIAGRAM - before/after: manual recap vs. automated post](media/02-flow.png)
> 🎨 **GENERATE LATER** - Excalidraw or /generate-image. Before: Gen types recap.
> After: the ops bot posts to Slack on a cron.
```

### Stats table syntax
Real numbers only, pulled from the interview/sources:
```markdown
| Metric | Before | After |
|---|---|---|
| Cited queries | 3 | **11** |
| Recap time / week | ~40 min | **0 (automated)** |
```

---

## Step 5 - Self-check, then validate

Before showing the draft, run this gate:

- [ ] No banned opener / closer / slop verb (list above) and no config `never_say`
- [ ] No em dashes (hyphens only)
- [ ] First person, conversational, varied sentence length
- [ ] At least one real number and one real-artifact media slot
- [ ] Shows at least one mess / wrong assumption (build-in-public credibility)
- [ ] Every number, quote, customer, and outcome traces to the interview or a source
      - nothing invented (flag anything you were unsure about)
- [ ] Reads like the founder, not like an AI (the "remove the byline" test: could any
      content marketer have written this exact post? If yes, it's too generic.)

Then **chain `voice-validator`** on the draft (mandatory per repo workflow). Fix what
it flags before finalizing. If you made assumptions or left gaps, list them for the
user.

---

## Step 6 - Render and write the files

The skill is generic; **the target repo's `DESIGN.md` drives the render.** Resolve it
in order: explicit path arg -> the publish-target / website repo's `DESIGN.md` -> a
`DESIGN.md` in the current repo -> none.

**A) Markdown source of truth (always).** Write `index.md` to the content repo at
`{content_repo}/production/blog/{post-slug}/` (for SM: `$YOUR_BRAND_REPO/...`;
for a client: `clients/{slug}/...`), with a sibling `media/` folder. This is the
editable source. Never write client output into the methodology repo root.

**B) Rendered HTML.**
- **If a `DESIGN.md` exists:** follow it exactly - its post template/structure, CSS or
  stylesheet link, fonts, component classes, canonical/URL rules, the filename +
  location to write into that repo, how to add the post to the blog index, the asset
  path, the commit-scope rule, and deploy steps. Produce a site-native page and place
  it where the `DESIGN.md` says (e.g. into the website repo). Run any link/render checks
  the `DESIGN.md` defines. Do NOT invent site conventions - if the `DESIGN.md` is silent
  on something, ask.
- **If no `DESIGN.md`:** fall back to `references/html-template.html` - read it, override
  `:root` from `visual_style.colors`, translate the body into its components, fill the
  `{{TOKENS}}`, and write `index.html` next to `index.md`. This is a preview render, not
  a publishable site page.

Media slots stay as placeholders until Gen drops the real files in. Never commit or
push to a publish-target repo without an explicit go (the repo's `DESIGN.md` defines
the commit scope and deploy trigger).

---

## Step 7 - Output summary

After writing the files, report back:

```
BLOG POST: [title]
Files: [md path] + [html path]
Arc: [one-line summary of the narrative shape used]

MEDIA CHECKLIST (Gen to fill):
1. 📸 media/01-... - [what to screenshot, where from]
2. 🎥 ... - [what to record]
3. 🎨 ... - [what to generate]

STATS USED (all traceable):
- [number] - source: [interview / git / Notion / digest]

OPEN GAPS / ASSUMPTIONS:
- [anything you guessed or couldn't verify - needs Gen's confirmation]

voice-validator: [PASS / PASS WITH FIXES / NEEDS REVIEW]
NEXT: drop the media, confirm the gaps, then publish.
```

---

## Compliance (non-negotiable)
- Never invent a number, quote, customer, testimonial, screenshot, or outcome. If
  you don't have it, leave a placeholder and ask.
- For other clients: respect confidentiality - don't name a client of an engagement
  without permission; anonymize ("a Series B fintech client") unless config grants
  naming rights.
- After any correction from Gen, write a lesson to `lessons.md` (repo self-improvement
  protocol).

## Related
- **voice-validator** - mandatory chain after the draft.
- **aeo-page-generator** - the OTHER blog tool, for machine-retrieval pages. Use that
  when the goal is AI citations, not personality.
- **topic-deep-dive** - run first if the post needs outside research beyond Gen's
  own experience.
- **Ops recaps / Notion** - sources for Path B idea mining.
- **generate-image** - to produce any DIAGRAM-type media slot later.
