<!-- Public export QUICKSTART. Copied to the export root by scripts/export-public.sh. -->

# Quickstart

Get a real AEO output in a few minutes. This repo ships with a fictional demo client
(`clients/acme-analytics/`) so everything runs before you've configured anything.

## 1. Prerequisites

- [Claude Code](https://claude.com/claude-code) installed and working
- (Optional, for live audits) API keys — set whichever you have in `.env`
  (copy `.env.example` to `.env`):
  - `ANTHROPIC_API_KEY` — Claude direct scans
  - `PERPLEXITY_API_KEY` — the Perplexity retrieval-index audit (`scripts/aeo_audit/`)
  - Ahrefs Brand Radar MCP — ChatGPT/Gemini visibility (optional)
- (Optional) Python 3.10+ if you want to run the audit scripts under `scripts/`

You can generate pages and run the methodology with **no API keys at all** — keys only
unlock the live multi-engine visibility scans.

## 2. Open the repo in Claude Code

```bash
git clone https://github.com/genwfurukawa/aeo-os.git
cd aeo-os
```

Open the folder in Claude Code. The root `CLAUDE.md` is the router — it tells the
assistant how to behave and which skill each request maps to.

## 3. Run something real

The demo client is `acme-analytics` (a fictional product-analytics SaaS). Try:

| Say this | What happens |
|----------|--------------|
| "create an AEO page: comparison of Acme Analytics vs Amplitude" | `aeo-page-generator` writes a full, schema'd comparison page |
| "generate llms.txt for acme-analytics" | `llms-txt-generator` produces a root-ready llms.txt |
| "fix my robots.txt for AI crawlers" | `ai-crawler-fix` outputs a corrected AI-bot ruleset |
| "build the query bank" | `/build-query-bank` produces 20-30 tagged queries |
| "where do I show up in AI search" | `aeo-engine-scan` runs the bank across engines (needs keys) |
| "why does Amplitude get cited for 'best product analytics'" | `cited-page-teardown` reverse-engineers the winner |

Outputs land under `clients/acme-analytics/production/` and `.../research/`.

## 4. Point it at your own brand

Two options:

- **Edit in place** — open `clients/acme-analytics/config.yaml` and the files in
  `clients/acme-analytics/config/` and replace the demo values with yours.
- **Scaffold a fresh client** — run `/clone-ops "Your Company"` to create a clean
  client directory with blank config templates.

Then set the active client:

```bash
export CLIENT_CONFIG=clients/your-slug/config.yaml
```

The critical files to fill: `config.yaml` (ICP, voice rules, competitors),
`config/voice-guide.md` (how your founder writes), and `config/icp-psyche.md` (who
you're talking to). Everything reads from these.

## 5. The order that works

For new content: **research → outline → produce → validate → optimize**.

1. `topic-deep-dive` → research brief
2. `storyboard-builder` → outline
3. channel skill (`aeo-page-generator`, `linkedin-post-writer`, …) → draft
4. `voice-validator` → `aeo-checker` → `aeo-injector` → quality gates
5. `aeo-engine-scan` → did it get cited? `citation-decay-monitor` → is it still cited?

## Troubleshooting

- **A skill asks for a target query** — give it the exact phrase a buyer would type
  into ChatGPT/Perplexity. That's the anchor for AEO.
- **Audit scripts fail** — you're missing a key in `.env`, or the Python venv isn't
  set up. The page-generation skills don't need keys; the live scans do.
- **Want the autonomous version** — that's the gated layer (see the README). This repo
  is the toolkit you drive yourself.

---

AEO OS is built by [SuperMarketers](https://www.supermarketers.ai) — the AEO system for B2B SaaS.
