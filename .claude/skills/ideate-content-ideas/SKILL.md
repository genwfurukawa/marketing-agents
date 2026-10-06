---
name: ideate-content-ideas
description: >
  Mine any repo you're building in Claude Code - this ops repo, a client repo, or a
  totally unrelated side project - for build-in-public content ideas: what shipped,
  what broke, what got fixed, what system is worth explaining, what a lesson cost you.
  Produces a scored backlog of ideas that PROVE the "autonomous marketing with AI"
  thesis with real evidence, not generic engineering-log posts. Global skill - works
  in any repo. Triggers on: "mine this repo for content ideas", "what should I post
  about", "find content ideas from what I built", "give me content ideas", "content
  idea backlog", "what's worth writing about here", "turn this repo into content".
  Feeds blog-writer, linkedin-post-writer, youtube-script-agent, and topic-deep-dive -
  this skill finds and scores the idea, those skills produce the piece. Different from
  blog-writer's Path B (a quick 3-5 candidate list for one post already in motion) -
  this is the deeper, persistent, cross-channel backlog with a thesis filter and a
  scoring gate, meant to run periodically against any repo.
metadata:
  version: 1.0.0
---

# Ideate Content Ideas (repo-mining, build-in-public)

You mine a codebase for content, not a topic list. The premise: the best proof that
"autonomous marketing with AI" works is SuperMarketers' own operation - the gates, the
loops, the scoring rubrics, the 3am alert that fired because a cron job outlived its
usefulness. That material already exists in git history, lessons files, PLAN docs, and
config. Most of it is never turned into content because nobody sits down and mines it.
That's this skill's one job.

**Default audience and destination:** Gen's own SuperMarketers build-in-public channels
(founders, marketers, AI-curious operators, per `$YOUR_BRAND_REPO/config.yaml`
icp). The repo you MINE and the repo you WRITE THE BACKLOG TO are usually different -
see Step 0.

---

## What this is not

- Not a brainstorm generator. Every idea traces to a real file, commit, or number in
  the target repo. If you can't point to the evidence, it's not an idea, it's a guess -
  drop it.
- Not "here's a feature we built." A changelog entry is not content. The bar is: does
  this teach a transferable lesson, or prove a step toward marketing that runs without
  a human in the loop? See Step 2.
- Not a replacement for blog-writer's interview. This skill produces the ANGLE and the
  evidence; blog-writer (or linkedin-post-writer / youtube-script-agent) still does the
  real writing, and blog-writer still interviews Gen for the specifics a repo can't
  contain (what it felt like, what he almost didn't ship).

---

## Step 0 - Load context and pick two repos

You're working with two repos that are often not the same:

1. **Target repo** (what you mine) - the repo Claude Code is currently running in,
   unless the user names a different path. This can be `marketing-agents`,
   `$YOUR_BRAND_REPO/`, a client repo, or an unrelated side project.
2. **Destination repo** (where the backlog gets written) - resolve with the same
   priority order as the rest of this repo's active-client convention:
   1. Explicit destination argument from the user
   2. `CLIENT_CONFIG` env var, if set, pointing at `clients/{slug}/`
   3. Default: `$YOUR_BRAND_REPO/` (Gen's own channels - this is the
      common case, since the whole point is dogfooding SM's own build)

Before mining, read from the **destination** repo:
- `config.yaml` -> `content.pillars` (for SM: `aeo`, `ai_marketing`, `claude_code`,
  `b2b_saas` - each with a `pov` line, use it) and `voice.never_say` / `always_say`
- `config/voice-guide.md`
- **A deep ICP doc, if one exists** (`config/icp-psyche.md` or equivalent - check for
  it explicitly, don't stop at `config.yaml`). `config.yaml`'s `icp` block and pillar
  names are a coarse label; a deep ICP doc encodes what actually moves the reader (fear
  validation, gap visibility, proof of results - see Step 2). Score against the deep
  doc's framework when one exists, never against pillar names alone (lesson:
  `lessons/client-context/score-content-against-deep-icp-doc.md` in the ops repo).
- `lessons.md` (if the destination is this ops repo or links to it) - the Always-apply
  block holds regardless of channel

If the target repo is a client's and not Gen's own, confirm before mining: client repo
contents may be confidential (see Compliance).

---

## Step 1 - Mine the target repo (multi-source sweep)

Run every pass that applies to the target repo; skip what doesn't exist rather than
forcing it. For each finding worth keeping, capture three things: **the fact** (what
happened), **the evidence** (exact file path / commit SHA / line so it's checkable),
and **the so-what** (why a reader who doesn't work here would care).

1. **Git history - what shipped, what broke, what got reverted.**
   ```
   git log --oneline --since="4 weeks ago"
   git log --stat -15
   git log --grep="fix\|revert\|hotfix" --oneline --since="8 weeks ago"
   ```
   Meaty commits (new systems, painful fixes, reverts) beat routine ones. A revert or a
   "fix:" commit is usually a better story than a clean "feat:" - it has a mistake in
   it, and mistakes are what make build-in-public credible.

2. **Corrections store** - `lessons/{category}/*.md` if this is the ops repo (or a
   CHANGELOG, retro doc, or postmortem file in another repo). Each lesson is already
   packaged as problem -> rule; that's most of a post's outline for free.

3. **Architecture and systems worth explaining** - read `CLAUDE.md` / `README.md` /
   `docs/` for anything that reads like a constitution or a named system (gates, loops,
   schedulers, cross-model verification, scoring rubrics). A system with a name and a
   rule is inherently a better post than a feature description, because it's a pattern
   the reader can steal.

4. **Plans and decisions** - `PLAN-*.md`, `docs/design/*.md`, any ADR-style doc. The
   value here is the "why," not the "what" - what alternative was rejected and why.

5. **Numbers** - config files, dashboards, scorecards, anything with a measurable
   before/after (tasks automated, minutes saved, citation rate, cost per run). A post
   with one real number beats five posts with none.

6. **PRs / issues**, if `gh` is available and the repo has a GitHub remote:
   ```
   gh pr list --state merged --limit 20
   gh issue list --state closed --limit 20
   ```

Do not fabricate a finding to fill a category. Fewer real findings beat padded ones.

---

## Step 2 - Filter for the thesis, not the feature

This is what keeps the backlog from turning into an engineering log. For each
candidate, ask:

- **ICP fit, against the deep doc, not the pillar name.** If the destination has a deep
  ICP doc (Step 0), score against ITS actual framework - for SM that's `icp-psyche.md`'s
  four jobs: Validate the fear / Show the gap / Teach the fix / Prove it works. A topic
  mapping cleanly to a `content.pillars` name (e.g. `claude_code`) is NOT sufficient on
  its own - internal engineering/ops stories map to that pillar by label while still
  being the wrong altitude for a business-decision-maker reader. Ask concretely: would
  THIS reader (per the ICP doc, not per the pillar list) care, or does this only teach
  another builder something about running Claude Code? Both can be real and
  well-evidenced; only one fits a CEO-ICP channel.
- **Autonomy proof.** Does this show a human bottleneck actually removed - a gate that
  lets work ship without Gen, a loop that re-runs itself, a QA step an agent now does
  that a person used to do? This is a strong angle when the destination's ICP is other
  builders/operators; it is NOT automatically strong for a CEO-ICP channel just because
  it maps to `ai_marketing` / `claude_code` - check the ICP-fit bullet above first.
- **Transferable pattern.** Does it teach something a reader can reuse, not just "look
  what we built"? Prefer the pattern over the product - but "reuse in their own Claude
  Code setup" is only the right pattern-type when the reader IS a builder; for a
  business-decision ICP the reusable thing is usually a finding about their own AI
  visibility, not an engineering pattern.
- **Real payoff.** Is there a genuine artifact or number, or is this a vague "we
  improved things" claim? Kill the latter.

Drop candidates that are pure internal trivia with no reader payoff (a renamed
variable, a routine dependency bump). Keep the ones where a mundane detail proves the
thesis for THIS reader - a 3am alert that fired because a cron job outlived its
usefulness teaches observability-vs-autonomy tension to a builder audience; it teaches
a CEO-ICP reader nothing. If a mining pass's source window skews heavily toward one
material type (e.g., a month of pure ops/infra commits), that is a signal to dig
further into other categories (`lessons/`, past client-audit findings, `docs/`) before
finalizing, not a reason to score the easy-to-find material highly just because it
technically maps to a pillar.

---

## Step 3 - Score what survives

Lightweight rubric, adapted from this repo's Leverage/Effort/Evidence/Freshness
pattern but built for content, not tasks. Score 0-2 on each,
threshold >=5/8 to make the active backlog; below that, keep as "parked."

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| **Proof** | No real artifact | Named but not quantified | Real number or screenshot-able artifact |
| **Thesis fit** | Feature description only | Touches autonomy or a reusable pattern | Directly proves a human bottleneck removed |
| **ICP fit** | Doesn't map to the deep ICP doc's framework (or only to a pillar name) | Loosely fits one of the ICP doc's jobs/pillars | Clean fit - matches a named job in the deep ICP doc (e.g. Validate the fear / Show the gap / Teach the fix / Prove it works), not just a pillar label |
| **Freshness** | 3+ months old | 2-4 weeks old | Shipped/learned this week |

When uncertain, score lower (repo-wide convention - see CLAUDE.md).

---

## Step 4 - Package each surviving idea

For every idea that clears the threshold, produce:

```
IDEA: [working title]
HOOK: [one line, <125 chars if LinkedIn is the likely channel]
PILLAR: [aeo / ai_marketing / claude_code / b2b_saas]
CHANNEL FIT: [LinkedIn / Blog / YouTube / Email - and why that one]
EVIDENCE: [file path(s), commit SHA(s), or line refs - must be checkable]
SCORE: proof=_ thesis=_ icp-fit=_ freshness=_ (total /8)
NEXT SKILL: [blog-writer if it needs an interview / narrative arc |
             linkedin-post-writer if it's a single sharp insight |
             youtube-script-agent if it's a teardown or demo |
             topic-deep-dive first if it needs outside research/competitive context]
```

Hooks are draft text that may get used verbatim downstream - hold them to the same
banned-phrase and no-em-dash rules as any other draft (config `voice.never_say` +
`lessons.md` Always-apply), even though the full voice-validator pass only runs on the
finished piece.

**Dedupe before finalizing:** check the destination repo's `production/` (blog,
linkedin, youtube subfolders) for anything already published on the same angle. Drop or
explicitly note the newer wrinkle that makes it a different post.

---

## Step 5 - Write the backlog and hand off

Write to `{destination}/research/content-ideas/{YYYY-MM-DD}.md` (create the directory
if it doesn't exist). Header states the target repo(s) mined and the mining date. Body
is the active backlog (score-sorted, highest first) followed by a Parked section for
anything under threshold, kept for later instead of discarded.

Then in chat:
1. Show the top 5-8 ideas (title, hook, score, next skill) - not the full file dump.
2. Ask which one(s) to run with.
3. On a pick, offer to hand off directly to the recommended skill (e.g., "want me to
   kick this to blog-writer now?") rather than making the user re-explain the idea.

---

## Step 6 - Optional Notion push

If the Notion MCP is reachable and the user confirms, add ONLY the picked idea(s) to
the Content Calendar DB at "Idea" status - not the whole backlog, to avoid cluttering a
shared surface with unscored maybes. This step is optional and never automatic; Notion
stays the single task/content state store per CLAUDE.md Operating Rule 3.

---

## Output template

```markdown
# Content Idea Backlog - {YYYY-MM-DD}

**Mined from:** {target repo path(s)}
**Destination:** {destination repo}
**Pillars source:** {destination}/config.yaml

## Active (score >= 5/8)

### 1. [Title] - score X/8
- HOOK:
- PILLAR:
- CHANNEL FIT:
- EVIDENCE:
- NEXT SKILL:

[... repeat, score-sorted ...]

## Parked (score < 5/8, revisit later)

- [Title] - score X/8 - why it's parked (e.g., "no real number yet, revisit after next run")
```

---

## Quality rules (non-negotiable)

1. Every idea traces to real, checkable evidence in the target repo - no invented
   commits, numbers, or artifacts.
2. Grep or `git log` to confirm a file/commit exists before citing it - do not cite
   from memory.
3. For client target repos: respect confidentiality. Don't name the client in content
   meant for Gen's own channels without permission; anonymize ("a Series B fintech
   client's repo") unless the client config explicitly grants naming rights.
4. Score honestly - when uncertain, score lower rather than inflate the backlog.
5. Never silently drop a source category because it was inconvenient to check (e.g.,
   skipping `gh` because it wasn't installed) - say so in the output instead of just
   omitting it.
6. No em dashes in any generated text (house rule - hyphens only). No banned phrases
   from the destination's `voice.never_say` or the generic list in the active output
   style.

## Related

- **blog-writer** - Path B does a lighter, single-post version of Step 1-2 for SM only;
  use this skill instead when you want the full cross-channel, scored backlog, or when
  mining a repo other than the SM ones.
- **linkedin-post-writer** / **youtube-script-agent** - typical hand-off targets from
  Step 5.
- **topic-deep-dive** - run first when a picked idea needs outside research or
  competitive context before it's ready to write.
- **compound** - if mining surfaces a lesson that isn't already captured in
  `lessons/`, capture it there too, separately from the content idea.
  (that one scores OKR-derived tasks, not content ideas - don't conflate the two).
