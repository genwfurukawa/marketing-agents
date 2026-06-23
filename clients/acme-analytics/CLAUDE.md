# Acme Analytics — Client Routing (DEMO)

This is the **Acme Analytics** demo client — a fictional B2B SaaS company that ships
inside this repo so the toolkit runs out of the box. It rides on the methodology at
the repo root.

## Active client

When you want the system to act for this client, set:

    CLIENT_CONFIG=clients/acme-analytics/config.yaml

(or pass `client_config_path` explicitly to skills/agents that accept it).

## Routing

- All methodology — agents, skills, commands, templates — lives at the repo root
  (`.claude/`, `templates/`, `visibility-system/`).
- Read the root `CLAUDE.md` for the global routing table.
- Read the root `lessons.md` AND this client's `./lessons.md` before generating content.

## Critical rules

- ALWAYS read `./config.yaml`, `./config/voice-guide.md`, and `./config/icp-psyche.md`
  before generating content.
- NEVER use phrases listed under `voice.never_say` in `config.yaml`.
- Outputs land in `./production/`, `./research/`, or `./intelligence/`.
- This is demo data. To use the toolkit for real, run `/clone-ops "Your Company"` or
  edit these files to point at your own brand.
