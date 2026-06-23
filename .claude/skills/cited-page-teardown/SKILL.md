---
name: cited-page-teardown
description: "Use when a competitor's page wins the AI citation for a query you want,
and you need to know WHY so you can displace it. Triggers on: 'why does this page get
cited', 'tear down the page ranking in Perplexity', 'reverse-engineer this AI
citation', 'how do I outrank this competitor in ChatGPT', 'what makes this page win',
'displace this competitor in AI search'. Takes a query + the cited competitor URL,
analyzes the structural/schema/freshness signals that earn the citation, and outputs
a displace plan. Extends the gap matrix (which shows WHO wins, not WHY). Hands the
plan to aeo-page-generator."
metadata:
  version: 1.0.0
---

# Cited Page Teardown

The gap matrix and `aeo-engine-scan` tell you *who* wins a citation — which
competitor URL the engine cites when you're absent. They don't tell you *why*. This
skill reverse-engineers the winning page against the exact signals that make AI
models extract and cite a passage, then gives you a concrete plan to build something
that displaces it.

## Why Pages Win Citations (the signals to grade against)

From the Princeton GEO study + platform analysis (same research base as
`aeo-checker`): AI models extract passages, not pages. A page wins when it has a
clean, self-contained passage that directly answers the query, backed by trust
signals. Teardown grades the winner on exactly these:
- **Definition / direct-answer block** in the first 300 words, in the query's words
- **Query-matched headings** (H2/H3 phrased as the actual question)
- **Extractable structure** — numbered steps, comparison tables, FAQ blocks
- **Statistics with named sources** (+37% citation rate) and **expert quotes** (+30%)
- **Freshness** — visible publish/update date, recent data
- **Schema** — FAQPage / Article / HowTo / Product JSON-LD present
- **Authority** — domain rating, the page's backlinks, third-party corroboration

## Before Starting

You need:
1. **The target query** (what the buyer asks the engine)
2. **The cited competitor URL** — from `aeo-engine-scan` /
   `citation-decay-monitor` / the gap matrix. If you have the query but not the URL,
   run `aeo-engine-scan` on that query first to capture who's actually cited.
3. **The engine(s)** where it wins (Perplexity vs ChatGPT vs AIO can reward
   different things).

## How to Tear It Down

### Step 1 — Pull the winning page
WebFetch the cited URL. Capture the actual content: opening paragraph, heading
structure, presence of definition/steps/table/FAQ, named stats and sources, visible
dates, and any JSON-LD (check page source). If multiple competitor URLs win across
engines, tear down each — the pattern across winners is the real lesson.

### Step 2 — Grade against the citation signals
Score each signal Present / Partial / Absent and note *how* they did it (the exact
phrasing of their definition, the structure of their FAQ). Build the scorecard:

| Signal | Winner | Notes |
|--------|--------|-------|
| Direct-answer block (first 300w) | ✅ | "X is …" — matches query verbatim |
| Query-matched headings | ◐ | 3 of 7 H2s are questions |
| Numbered steps / table / FAQ | ✅ | 8-row comparison table + 6-Q FAQ |
| Stats with named sources | ✗ | claims, no citations |
| Freshness | ✅ | "Updated {month}" + 2026 data |
| Schema (JSON-LD) | ✅ | FAQPage + Article |
| Domain/page authority | ✅ | DR {n}, {n} refdomains to this URL |

### Step 3 — Find the displacement opening
The winner almost always has a weakness — that's your wedge. Common openings:
- **Thin trust** — they assert without named sources; you cite real data/original
  research (→ `original-research-designer`)
- **Stale** — their data is old; you publish fresher
- **Shallow extraction** — they have prose but no FAQ/table; you out-structure them
- **Generic** — they answer broadly; you answer the specific buyer's version better
- **Weak authority** — if they win on structure but have low DR, structure + a
  citation-seeding push (→ `community-seeding`, `knowledge-graph-builder`) can flip it

Be honest: if the winner is genuinely strong on every axis AND has high authority,
say so and recommend picking a more winnable adjacent query rather than a doomed
head-to-head.

## Output

Write to `clients/{slug}/research/teardowns/{query-slug}.md`:
1. **The query + winners** (URL per engine)
2. **Signal scorecard** per winning page (the table above)
3. **Why it wins** — 2-3 sentences naming the decisive signals
4. **The displacement opening** — the specific weakness to exploit
5. **Displace plan** — a ready-to-build brief: recommended page type (one of the 14),
   the required structural elements to beat them on, the proprietary-data/freshness
   angle, schema to ship, and internal/external links needed. This brief is the
   input to `aeo-page-generator`.

## Hand-offs

- Displace plan → `aeo-page-generator` (build the page that beats it)
- "Need proprietary data to out-trust them" → `original-research-designer`
- "They win on authority, not structure" → `community-seeding` +
  `knowledge-graph-builder` + `topical-authority-linker`
- Re-check after publishing → `aeo-engine-scan` on the same query

## Quality Gate

- [ ] Graded the actual fetched page, not assumptions (WebFetch run)
- [ ] Every citation signal scored Present/Partial/Absent with how-they-did-it notes
- [ ] Schema checked in real page source, not guessed
- [ ] A specific, honest displacement opening named (or an honest "pick another query")
- [ ] Output is a build-ready brief for `aeo-page-generator`, not just analysis
