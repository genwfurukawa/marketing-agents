# Commands

All 19 slash commands, grouped by stage. Each command orchestrates one
or more agents/skills. Files live in `.claude/commands/` for Claude
Code auto-discovery.

## Sprint Orchestration (the core operating rhythm)

| Command | When to use |
|---------|------------|
| [/sprint](.claude/commands/sprint.md) | Run the weekly cycle: audit → plan → create → review → qa → distribute → retro. Subcommands: `start`, `audit`, `plan`, `create`, `review`, `qa`, `ship`, `retro`, `auto`, `status` |

## Foundation (Brand Setup)

| Command | When to use |
|---------|------------|
| [/build-brand-brain](.claude/commands/build-brand-brain.md) | Generate the 12-section Brand Brain for a new client |
| [/founder-session](.claude/commands/founder-session.md) | Turn a 30-min founder transcript into 8–12 scored atomic insights |
| [/clone-ops](.claude/commands/clone-ops.md) | Scaffold a clean client directory or standalone client repo |

## Brain (Audit, Query Bank, Analytics)

| Command | When to use |
|---------|------------|
| [/audit-blueprint](.claude/commands/audit-blueprint.md) | Full $3K paid AEO Blueprint audit — 10 deliverables, 9-dim score, 90-day roadmap |
| [/build-audit-report](.claude/commands/build-audit-report.md) | Chain aeo_audit + competitor analysis + crawler audit into one client deliverable |
| [/build-query-bank](.claude/commands/build-query-bank.md) | ICP → audience mining → 20–30 tagged AEO queries |
| [/competitive-monitor](.claude/commands/competitive-monitor.md) | Week-over-week competitor visibility tracking |
| [/pull-analytics](.claude/commands/pull-analytics.md) | GA4 + Search Console pull, partitioned CSVs + markdown summaries |
| [/monthly-briefing](.claude/commands/monthly-briefing.md) | CEO-grade monthly AI visibility briefing (HTML + memo) |

## Brand (Content Production)

| Command | When to use |
|---------|------------|
| [/produce-weekly-content](.claude/commands/produce-weekly-content.md) | Full weekly pipeline: score → build objects → write → validate → AEO check |
| [/produce-video](.claude/commands/produce-video.md) | YouTube — scaffold, script, thumbnail, SEO, or publish package |
| [/generate-content-bundle](.claude/commands/generate-content-bundle.md) | One input → LinkedIn + blog + email + video script + carousel |
| [/process-podcast](.claude/commands/process-podcast.md) | Podcast transcript → titles, summary, takeaways, thumbnails, clip timestamps |
| [/generate-image](.claude/commands/generate-image.md) | Prompt + optional Nano Banana (Gemini) generation |

## Cross-stage (Review, Distribute, Retro)

| Command | When to use |
|---------|------------|
| [/content-review](.claude/commands/content-review.md) | 4 parallel reviewers: voice, AEO, brand, conversion |
| [/content-qa](.claude/commands/content-qa.md) | Pre-publish checks: char counts, links, UTMs, format |
| [/distribute](.claude/commands/distribute.md) | Schedule reviewed content across channels, log distribution |
| [/campaign-retro](.claude/commands/campaign-retro.md) | Sprint retro — performance, citations, pipeline signals, lessons |
