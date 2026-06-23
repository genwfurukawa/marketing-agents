# AEO OS — The Answer Engine Optimization Operating System

By SuperMarketers · built by Gen Furukawa. An open, runnable AEO system for B2B SaaS:
reusable agents, commands, skills, and templates that turn founder insight into content
AI engines cite. This file is the runtime router — what Claude Code reads on every
invocation to know how to behave.

## Identity

This repo is **methodology**. Brand identity, ICP, voice, and other client-specific
values live under `clients/{slug}/`. A fictional demo client ships at
`clients/acme-analytics/` so the system runs out of the box. Before generating
content, load the active client's config:

- `clients/{slug}/config.yaml` — machine-readable settings (ICP, voice rules, offers)
- `clients/{slug}/config/voice-guide.md` — founder voice rules
- `clients/{slug}/config/icp-psyche.md` — deep ICP profile
- `clients/{slug}/config/pillars.md` — content pillar strategy

Set the active client via `CLIENT_CONFIG=clients/{slug}/config.yaml`, or pass the slug
to skills/agents that accept it. Read `lessons.md` (repo root) for accumulated
methodology corrections.

## Structure

- `.claude/agents/` — client-agnostic agents (foundations, channels, research, review)
- `.claude/commands/` — slash commands (sprint system + audit + content orchestrators)
- `.claude/skills/` — production skills (the AEO suite + research + content + measurement)
- `.claude/output-styles/consultant-operator.md` — generic operator persona
- `visibility-system/` — the 9-step methodology wiki + 9-dimension scoring rubric
- `templates/` — reusable scaffolding (14 AEO page types, brand brain, audit scripts)
- `scripts/` — tooling (AEO audit, analytics pulls, image generation, YouTube)
- `docs/reference/` — human-navigation index files; `docs/ROADMAP.md` — what's next
- `clients/` — client instances (`acme-analytics` is the demo)

## Commands

| You say | What happens |
|---------|-------------|
| "create an AEO page" | aeo-page-generator skill (14 page types) |
| "generate llms.txt" / "make my site AI-crawlable" | llms-txt-generator skill |
| "fix my robots.txt for AI" / "unblock AI crawlers" | ai-crawler-fix skill |
| "where do I show up in AI search" / "scan all engines" | aeo-engine-scan skill |
| "check for citation decay" / "did my AI visibility drop" | citation-decay-monitor skill |
| "why does this competitor get cited" / "displace this page" | cited-page-teardown skill |
| "audit my internal links" / "build topical authority" | topical-authority-linker skill |
| "seed Reddit/Quora for AEO" | community-seeding skill |
| "design original research" / "state of X report" | original-research-designer skill |
| "build my knowledge graph" / "get a Wikidata entry" | knowledge-graph-builder skill |
| "run the audit" | /audit command |
| "run the blueprint audit" | /audit-blueprint (10 deliverables, 9-dim score) |
| "build the query bank" | /build-query-bank |
| "write a LinkedIn post" | linkedin-post-writer skill |
| "check this draft" | voice-validator → aeo-checker |
| "generate schema" | schema-generator skill |
| "research [topic]" | topic-deep-dive skill |
| "build storyboard for [topic]" | storyboard-builder skill |
| "run a sprint" | /sprint (full audit-to-retro cycle) |
| "review this content" | /content-review (4 parallel reviewers) |
| "clone ops for [client]" | /clone-ops |

## Sprint System

The core operating rhythm — chains tools into a weekly cycle:

```
Audit -> Plan -> Create -> Review -> QA -> Distribute -> Retro
```

`/sprint start | audit | plan | create | review | qa | ship | retro | status`.
Modes: FULL_SPRINT, AUDIT_ONLY, CONTENT_ONLY, OPTIMIZE_ONLY, DISTRIBUTE_ONLY.

## Content Production Workflow

For new content: research → outline → produce → validate → optimize.

1. **Research:** `topic-deep-dive` → `research/{slug}/deep-dive.md`
2. **Outline:** `storyboard-builder` → `production/{slug}/storyboard.md`
3. **Produce:** channel skill (aeo-page-generator, linkedin-post-writer, …)
4. **Validate:** voice-validator → aeo-checker → aeo-injector → schema-generator
5. **Measure:** aeo-engine-scan → citation-decay-monitor

## AEO Toolchain (how the skills compose)

- **Build a page:** aeo-page-generator (auto-chains checker → injector → voice → schema)
- **Fix technical readiness:** ai-crawler-audit-agent → ai-crawler-fix + llms-txt-generator
- **Measure visibility:** /build-query-bank → aeo-engine-scan → (score via rubric)
- **Find & close gaps:** aeo-engine-scan → cited-page-teardown → aeo-page-generator
- **Track over time:** aeo-engine-scan → citation-decay-monitor
- **Build authority:** entity-authority-agent → knowledge-graph-builder + community-seeding
- **Own the data:** original-research-designer → statistics page → schema-generator

## Critical Rules

- ALWAYS read the active client's `config.yaml` before generating content
- ALWAYS read `lessons.md` before generating content
- ALWAYS read the client's `config/voice-guide.md` before writing in that voice
- NEVER use phrases from the client config's `voice.never_say`
- Score queries using `visibility-system/` rubrics. When uncertain, score lower.
- Content outputs go to `clients/{slug}/production/` and `.../research/`. Never write
  client outputs into the methodology root.

## Self-Improvement

After any correction, write a rule to `lessons.md` in the format:
`[date] **Problem:** [what]. **Rule:** [fix]. **Applies to:** [scope]`. The system
compounds or it dies.
