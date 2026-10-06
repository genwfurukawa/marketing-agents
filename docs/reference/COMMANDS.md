# Commands

All 25 slash commands, grouped by stage. Each command orchestrates one
or more agents/skills. Files live in `.claude/commands/` for Claude
Code auto-discovery. The operating rhythm itself is not a command — it
is the Notion task loop plus the weekly planning review (see
[docs/OPERATING.md](../OPERATING.md)).

## Foundation (Brand Setup)

| Command | When to use |
|---------|------------|
| [/build-brand-brain](.claude/commands/build-brand-brain.md) | Generate the 12-section Brand Brain for a new client |
| [/founder-session](.claude/commands/founder-session.md) | Turn a 30-min founder transcript into 8–12 scored atomic insights |
| [/clone-ops](.claude/commands/clone-ops.md) | Scaffold a clean client directory or standalone client repo |

## Brain (Audit, Query Bank, Analytics)

| Command | When to use |
|---------|------------|
| [/build-audit-report](.claude/commands/build-audit-report.md) | The Citability Audit at any depth (snapshot / gameplan / baseline / pulse) + client-facing report |
| [/build-query-bank](.claude/commands/build-query-bank.md) | ICP → audience mining → 20–30 tagged AEO queries |
| [/competitive-monitor](.claude/commands/competitive-monitor.md) | Week-over-week competitor visibility tracking |
| [/pull-analytics](.claude/commands/pull-analytics.md) | GA4 + Search Console pull, partitioned CSVs + markdown summaries |
| [/monthly-briefing](.claude/commands/monthly-briefing.md) | CEO-grade monthly AI visibility briefing (HTML + memo) |

## Brand (Content Production)

| Command | When to use |
|---------|------------|
| [/produce-weekly-content](.claude/commands/produce-weekly-content.md) | Full weekly pipeline: score → build objects → write → validate → AEO check |
| [/produce-video](.claude/commands/produce-video.md) | YouTube — scaffold, script, thumbnail, SEO, or publish package |
| [/process-podcast](.claude/commands/process-podcast.md) | Podcast transcript → titles, summary, takeaways, thumbnails, clip timestamps |
| [/generate-image](.claude/commands/generate-image.md) | Prompt + optional Nano Banana (Gemini) generation |

## Ops self-audit (ops repo only - excluded from client sync and public export)

| Command | When to use |
|---------|------------|
| [/audit-fleet](.claude/commands/audit-fleet.md) | Verbose run of the weekly fleet-audit engine, incl. acknowledged findings |
| [/audit-hygiene](.claude/commands/audit-hygiene.md) | Deep cruft/doc-drift pass; produces a deletion manifest for approval |
| [/audit-costs](.claude/commands/audit-costs.md) | Loop/recap/sync cost-and-value analysis with per-job recommendations |
| [/audit-security](.claude/commands/audit-security.md) | Full-history gitleaks, endpoint posture, permissions, guard coverage |

## Cross-stage (Review, Distribute, Retro)

| Command | When to use |
|---------|------------|
| [/content-review](.claude/commands/content-review.md) | 4 parallel reviewers: voice, AEO, brand, conversion |
| [/content-qa](.claude/commands/content-qa.md) | Pre-publish checks: char counts, links, UTMs, format |
| [/distribute](.claude/commands/distribute.md) | Schedule reviewed content across channels, log distribution |
| [/campaign-retro](.claude/commands/campaign-retro.md) | Campaign retro — performance, citations, pipeline signals, lessons |
