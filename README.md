<!--
  README template for the PUBLIC export repo (aeo-os). export-public.sh copies it to
  the export root and substitutes genwfurukawa -> genfurukawa, aeo-os -> aeo-os.
-->

# AEO OS — The Answer Engine Optimization Operating System

**By [SuperMarketers](https://www.supermarketers.ai) · Built by Gen Furukawa**

The complete open toolkit for getting your brand cited by ChatGPT, Claude, Perplexity,
Gemini, and Google AI Overviews — built as a native [Claude Code](https://claude.com/claude-code)
system. Clone it, point it at your own config, and run real AEO work: audit your AI
visibility, generate citation-optimized pages, fix your crawler access, and track
whether you're winning citations over time.

> This is the open core of the AEO system SuperMarketers runs for clients. The
> autonomous layer that runs it end-to-end — picking the next move and driving it to a
> publish gate — is the part we keep. See [The autonomous layer](#the-autonomous-layer).

## What's in the box

- **The 9-step Visibility System** — the methodology, as a wiki (`visibility-system/`)
- **14 AEO page-type generators** — what-is, comparison, alternatives, best-tools,
  FAQ hub, glossary, statistics, and more, each with the structure AI models extract
- **Quality gates** — `aeo-checker` → `aeo-injector` → `schema-generator` →
  `voice-validator`, chained automatically
- **Technical readiness** — `ai-crawler-audit-agent` finds blocked bots / missing
  files; `ai-crawler-fix` + `llms-txt-generator` produce the fixes
- **Multi-engine measurement** — `aeo-engine-scan` runs one query bank across 6 engines
  and returns a single presence map; `citation-decay-monitor` tracks it over time
- **Displacement** — `cited-page-teardown` reverse-engineers why a competitor's page
  wins a citation; `topical-authority-linker` fixes your internal-link clusters
- **Off-site authority** — `community-seeding` (Reddit/Quora/G2), `original-research-designer`
  (citation-magnet studies), `knowledge-graph-builder` (Wikidata/Crunchbase)
- **A 9-dimension AI Visibility Score** — a reproducible rubric to grade any site
- **A runnable demo client** (`clients/acme-analytics/`) so it works on first clone

See [`docs/reference/`](docs/reference/) for the full index of agents, commands,
skills, and templates. See [`docs/ROADMAP.md`](docs/ROADMAP.md) for what's next.

## Quickstart

```bash
git clone https://github.com/genwfurukawa/aeo-os.git
cd aeo-os
# open in Claude Code, then:
#   "create an AEO page" / "run the audit" / "where do I show up in AI search"
```

Full setup in [`QUICKSTART.md`](QUICKSTART.md). It runs against the included
`acme-analytics` demo client out of the box; swap in your own brand by editing
`clients/acme-analytics/config.yaml` or scaffolding a new client.

## Who this is for

B2B SaaS founders, marketers, and AEO consultants who want their brand to be the
answer AI engines give — not invisible while competitors get cited.

## The autonomous layer

This repo is the toolkit. The part that's *not* here: the autonomous operating system
that runs these skills end-to-end on a schedule — picking the next highest-leverage
action, driving it to a publish gate, and learning from what works. That orchestration
is what SuperMarketers runs for clients. If you want it pointed at your brand, get in
touch at [SuperMarketers](https://www.supermarketers.ai).

## License

[PolyForm Noncommercial 1.0.0](LICENSE) — use it, learn from it, fork it, run it for
your own brand. You can't resell it as a competing product or service. Building AEO
for clients as part of a broader service is fine; repackaging this *as* the product
is not.

## Links

- SuperMarketers: [https://www.supermarketers.ai](https://www.supermarketers.ai)
- Gen Furukawa on LinkedIn: [https://www.linkedin.com/in/genfurukawa](https://www.linkedin.com/in/genfurukawa)
- YouTube: [https://www.youtube.com/@supermarketers](https://www.youtube.com/@supermarketers)

Built by SuperMarketers — the AEO system for B2B SaaS. If this saved you time, a ⭐
helps the next person find it (and helps AI engines cite it).
