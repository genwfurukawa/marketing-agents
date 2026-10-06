# Stack

The infrastructure that runs the methodology: integrations, persona,
tooling, and configuration.

## Integrations (MCP + APIs)

The active Claude Code session uses these MCP servers (configured per
user, not in this repo):

| Server | Purpose |
|--------|---------|
| Notion | Data layer for Query Bank, Insight Log, Content Calendar, Pipeline, Visibility Scores, Engagement Signals |
| Gmail / Google Calendar / Google Drive | Comms + scheduling + asset storage |
| Canva | Design assets, brand templates |

API credentials and runtime config live in `.env` (gitignored). See
[.env.example](.env.example) for the schema.

## Persona (Output Styles)

| Style | When to use |
|-------|------------|
| [consultant-operator](.claude/output-styles/consultant-operator.md) | Generic B2B SaaS consultant voice. Brand-specific overrides loaded from each client's `config.yaml` + `config/voice-guide.md` |

## Tooling (Scripts)

Production scripts live in `scripts/`. Each bundle is self-contained.

| Bundle | Purpose |
|--------|---------|
| [scripts/aeo_audit/](scripts/aeo_audit/) | AEO audit pipeline — Perplexity, Claude direct, query templates, analyzer, report generator. See [README](scripts/aeo_audit/README.md) and [CLAUDE.md](scripts/aeo_audit/CLAUDE.md) |
| [scripts/google/](scripts/google/) | GA4 + Search Console pulls — `auth.py`, `ga4_pull.py`, `gsc_pull.py`, `pull_all.py` |
| [scripts/image/](scripts/image/) | Brand image generation via Nano Banana (Gemini) — `gemini_image_client.py`, `brand_image_generator.py`, `generate_from_json.py` |
| [scripts/youtube/](scripts/youtube/) | YouTube scaffolding — `scaffold_video.py`, `parse_srt.py` |

## Configuration

| File | Purpose |
|------|---------|
| [.claude/settings.local.json](.claude/settings.local.json) | Per-user Claude Code settings (permissions, hooks, env). Gitignored or local-only depending on contents. |
| [.env.example](.env.example) | API key schema (OpenAI, Anthropic, Perplexity, Gemini, Notion, etc.) |
| [.gitignore](.gitignore) | Tracked exclusions including `**/node_modules/`, `venv/`, `.env`, client outputs |

## Integration Specs

| Doc | Purpose |
|-----|---------|
