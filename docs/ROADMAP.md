# AEO Toolkit Roadmap

The toolkit ships a complete AEO practitioner stack today: foundations → research →
14 page-type generation → checker/injector/schema gates → multi-engine measurement →
displacement → off-site authority → 9-dimension scoring. This roadmap is what comes
next — the emerging surface area of Answer Engine Optimization that's real but
earlier in its maturity curve.

These are documented, not yet built. Publishing the roadmap is itself a signal: it
shows where AEO is heading, not just where it is.

## Shipped (the current toolkit)

- **Foundations** — ICP, positioning, voice (Steps 1-3)
- **Research** — topic deep-dives, audience question mining, competitor analysis, query banks
- **Page generation** — 14 AEO page types + checker → injector → voice → schema chain
- **Technical readiness** — crawler audit → `ai-crawler-fix` + `llms-txt-generator`
- **Measurement** — `aeo-engine-scan` (6 engines), `ahrefs-pull` (Brand Radar), `citation-decay-monitor`
- **Displacement** — `cited-page-teardown`, `topical-authority-linker`
- **Off-site authority** — `community-seeding`, `original-research-designer`, `knowledge-graph-builder`
- **Scoring** — 9-dimension AI Visibility Score rubric, prospect scorecard

## Next (second-tier modules)

### 1. Conversational follow-up simulation
Real buyers don't ask one question — they ask a follow-up chain ("best X" → "X vs Y" →
"is X worth it for {use case}"). Today's scans are single-shot. A module that
simulates multi-turn query sessions and tracks where a brand enters, survives, or
drops out of the conversation across the funnel. Why it's next-tier: engine behavior
on multi-turn is less stable and harder to measure reproducibly than single queries.

### 2. Multimodal / image AEO
AI answers increasingly surface images, and multimodal models read them. A module for
image-level optimization: descriptive alt text written for extraction, `ImageObject`
schema, filename/caption signals, and diagram/chart packaging so visual assets
(including the ones the `excalidraw-diagram` skill produces) can themselves be cited.
Why it's next-tier: image citation behavior in answer engines is still emerging and
varies widely by engine.

### 3. People-Also-Ask / autocomplete harvesting
The query bank is currently built from templates + community mining. A module that
harvests the live question graph — Google's "People Also Ask", autocomplete, and
related-question expansions — to ground the query bank in real, current demand and
catch fast-moving question trends. Why it's next-tier: reliable access to these
surfaces needs a scraping/data layer the toolkit doesn't yet standardize.

### 4. Multilingual AEO
All query templates and checks are English-only today. A module for non-English AEO:
locale-specific query banks, per-language engine behavior (engines cite different
sources by language/region), and translation that preserves extractability rather
than just meaning. Why it's next-tier: each locale is effectively a new measurement
surface with its own cited-source ecosystem.

## How these get prioritized

The same way everything in this system is scored — by leverage. A second-tier module
graduates to "build" when (a) enough engines reward it to make the work pay off, and
(b) it can be measured reproducibly. If you want one of these sooner, the gap is
usually the data layer, not the prompt design — open an issue describing the surface
you need access to.
