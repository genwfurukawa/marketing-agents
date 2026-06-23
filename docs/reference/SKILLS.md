# Skills

All 23 skills, grouped by purpose. Skills are composable, reusable units
invoked via the Skill tool. Files live in `.claude/skills/{name}/SKILL.md`
for Claude Code auto-discovery. Each skill folder may contain `evals/`,
`scripts/`, `assets/`, and templates — these stay co-located with the
skill.

## AEO Suite (citation-optimized content)

| Skill | Purpose | Inputs / Outputs |
|-------|---------|------------------|
| [aeo-checker](.claude/skills/aeo-checker/SKILL.md) | Audit content for AEO retrievability | Draft → checklist of missing elements |
| [aeo-injector](.claude/skills/aeo-injector/SKILL.md) | Inject missing AEO elements identified by aeo-checker | Draft + checklist → updated draft |
| [aeo-page-generator](.claude/skills/aeo-page-generator/SKILL.md) | Generate publish-ready pages across 14 AEO page types | Topic + page type → full page (auto-chains checker → injector → voice-validator) |
| [schema-generator](.claude/skills/schema-generator/SKILL.md) | Generate JSON-LD structured data blocks | Page content → schema.org JSON-LD |

## Technical AI Readiness (audit finds → these fix)

| Skill | Purpose | Inputs / Outputs |
|-------|---------|------------------|
| [llms-txt-generator](.claude/skills/llms-txt-generator/SKILL.md) | Generate `llms.txt` / `llms-full.txt` so AI crawlers find and prioritize the right pages | Page inventory → root-ready llms.txt |
| [ai-crawler-fix](.claude/skills/ai-crawler-fix/SKILL.md) | Generate a corrected robots.txt AI-bot ruleset + sitemap (remediates `ai-crawler-audit-agent`) | Audit output → robots.txt + sitemap.xml |

## AEO Measurement & Displacement

| Skill | Purpose | Inputs / Outputs |
|-------|---------|------------------|
| [aeo-engine-scan](.claude/skills/aeo-engine-scan/SKILL.md) | Run a query bank across ChatGPT/Claude/Perplexity/Gemini/Google AIO/Copilot → one presence map | Query bank → engine_map.json/.md, Source Control Rate |
| [citation-decay-monitor](.claude/skills/citation-decay-monitor/SKILL.md) | Re-run a saved scan, diff vs prior, flag lost/displaced citations (read-only monitor) | Prior scan → decay_report.md + deltas |
| [cited-page-teardown](.claude/skills/cited-page-teardown/SKILL.md) | Reverse-engineer WHY a competitor URL wins a citation → build-ready displace plan | Query + cited URL → teardown + displace brief |
| [topical-authority-linker](.claude/skills/topical-authority-linker/SKILL.md) | Audit internal links vs the planned hub-and-spoke; fix orphans | Link graph + architecture → link additions plan |

## Off-site Authority (where AI answers pull from)

| Skill | Purpose | Inputs / Outputs |
|-------|---------|------------------|
| [community-seeding](.claude/skills/community-seeding/SKILL.md) | Find Reddit/Quora/G2 threads AI cites + draft non-promotional answers (human posts) | Target queries → thread targets + drafted answers |
| [original-research-designer](.claude/skills/original-research-designer/SKILL.md) | Design a citation-magnet study / "State of X" report → feeds the statistics page type | Category + gap → study brief + packaging plan |
| [knowledge-graph-builder](.claude/skills/knowledge-graph-builder/SKILL.md) | Build a Wikidata/Crunchbase/knowledge-panel entity package from locked descriptions | Entity descriptions → submission package |

## Visibility Data

| Skill | Purpose | Inputs / Outputs |
|-------|---------|------------------|
| [ahrefs-pull](.claude/skills/ahrefs-pull/SKILL.md) | Pull AI visibility data from Ahrefs Brand Radar | Brand → SOV, cited domains/pages, mentions, AI responses, deltas |

## Research

| Skill | Purpose | Inputs / Outputs |
|-------|---------|------------------|
| [topic-deep-dive](.claude/skills/topic-deep-dive/SKILL.md) | Channel-agnostic intelligence brief for any topic | Topic → full research package feeding all formats |
| [last30days](.claude/skills/last30days-skill-main/SKILL.md) | 30-day research across Reddit, X, YouTube, TikTok, HN, web | Topic → grounded cited report |
| [podcast-prep](.claude/skills/podcast-prep/SKILL.md) | Guest research → interview prep package | Guest name + company URL → bio, themes, questions, screen shares |

## Insight Pipeline

| Skill | Purpose | Inputs / Outputs |
|-------|---------|------------------|
| [insight-scorer](.claude/skills/insight-scorer/SKILL.md) | Score and select the best insight from observations | Observations → ranked insights |
| [insight-object-builder](.claude/skills/insight-object-builder/SKILL.md) | Turn a selected insight into a structured 6-field object | Insight → object ready for content brief |

## Content Production

| Skill | Purpose | Inputs / Outputs |
|-------|---------|------------------|
| [linkedin-post-writer](.claude/skills/linkedin-post-writer/SKILL.md) | Write LinkedIn posts in a founder/brand voice | Insight + voice config → post + CTA variants |
| [storyboard-builder](.claude/skills/storyboard-builder/SKILL.md) | Build SAY/SHOW storyboard or post/blog outline from research | Deep dive → channel-appropriate outline |
| [voice-validator](.claude/skills/voice-validator/SKILL.md) | Validate any draft against a founder's documented voice rules | Draft + voice guide → pass/fail + corrections |

## YouTube (idea → package → produce → diagnose)

Idea-and-packaging-first system that wraps the existing 5 YouTube agents. Real outlier data via the YouTube Data API (`scripts/youtube/yt_api.py`; key setup in each skill's `setup.md`).

| Skill | Purpose | Inputs / Outputs |
|-------|---------|------------------|
| [youtube-competitor-research](.claude/skills/youtube-competitor-research/SKILL.md) | Keyword → top videos → outlier multiples + packaging/hook teardown → gap map | Keyword → `research/youtube/<kw>/` gap-map + CSV |
| [youtube-idea-validation](.claude/skills/youtube-idea-validation/SKILL.md) | Score a concept before scripting (Demand/Breadth/Outlier/Angle/Feasibility, 0-2, ≥7 greenlight) | Idea + competitor data → go/no-go + sharpen |
| [youtube-packaging-first](.claude/skills/youtube-packaging-first/SKILL.md) | Title + thumbnail FIRST, then script to fit; chains research→validate→package→script→produce→publish | Greenlit idea → locked packaging → finished video |
| [youtube-analytics-retro](.claude/skills/youtube-analytics-retro/SKILL.md) | Diagnose CTR vs retention vs AVD from a Studio CSV; isolate the failing lever | Studio export + packaging.md → retro.md + lesson |

## Visual

| Skill | Purpose | Inputs / Outputs |
|-------|---------|------------------|
| [excalidraw-diagram](.claude/skills/excalidraw-diagram-skill-main/SKILL.md) | Create Excalidraw diagram JSON files | Concept → Excalidraw JSON |
