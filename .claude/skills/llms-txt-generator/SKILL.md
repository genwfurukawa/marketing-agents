---
name: llms-txt-generator
description: "Use when generating an llms.txt or llms-full.txt file for a site so
AI crawlers and answer engines can find and prioritize the right content. Triggers
on: 'generate llms.txt', 'create an llms.txt', 'build llms-full.txt', 'add an LLM
manifest', 'make my site AI-crawlable', 'I scored low on llms.txt in the audit'.
Run after ai-crawler-audit-agent flags a missing or weak llms.txt. Produces the
file content ready to drop at the site root. For robots.txt and sitemap fixes, see
ai-crawler-fix. This is content generation, not a technical site change."
metadata:
  version: 1.0.0
---

# llms.txt Generator

You generate `llms.txt` (and optionally `llms-full.txt`) — the emerging standard
that tells AI crawlers and answer engines which pages on a site matter and what
they contain. The AI Visibility Score rubric (Dimension 5: Technical AI Readiness)
awards up to 2 points for a present, well-structured llms.txt. The crawler audit
*detects* its absence; this skill *produces* it.

## What llms.txt Is

`llms.txt` is a Markdown file at a site's root (`/llms.txt`) that gives LLMs a
curated map of the site: a one-line description, then sections of links with short
context. It is to AI crawlers what a sitemap is to search engines — but
human-readable and prioritized. `llms-full.txt` is the expanded variant that
inlines the actual content of the most important pages so a model can answer
without fetching each URL.

This is a discovery and prioritization signal, not an access-control file
(that's robots.txt — see `ai-crawler-fix`).

## Before Starting

You need:
1. **Domain** (e.g. `acme.com`)
2. **A page inventory** — one of:
   - the site's `sitemap.xml` (fetch it), or
   - `ai-crawler-audit-agent` output (it lists top pages), or
   - `04_keyword_opportunities` / `top-pages` data from `/audit-blueprint`, or
   - a pasted list of URLs + titles
3. **The entity description** — pull the locked Tagline + Short description from
   `entity-authority-agent` output if it exists; otherwise from
   `clients/{slug}/config.yaml` `brand`. If neither exists, ask for one line on
   what the company does.

If you have no page inventory: WebFetch the sitemap or the homepage nav to build one.
Never invent URLs — every link in llms.txt must resolve.

## How to Build It

### Step 1 — Classify pages by AI-answer value
Sort the inventory into sections, highest-citation-value first:
- **Core** — homepage, product, pricing (the entity-defining pages)
- **Docs / Guides** — how-tos, integration guides, problem-solution pages
- **AEO pages** — the 14 page types (what-is, comparisons, alternatives, glossary,
  statistics, FAQ hubs) — these are the citation magnets, list them prominently
- **Proof** — case studies, original research/statistics pages
- **Optional** — blog index, changelog, about (lower priority; include under an
  `## Optional` section, which the spec treats as skippable)

Drop: login, cart, legal boilerplate, tag/pagination pages, anything thin.

### Step 2 — Write the file
Follow the llms.txt spec format exactly:

```
# {Company Name}

> {One-sentence description — what the company does, for whom. Use the locked
> Tagline. No marketing fluff, no banned phrases.}

{Optional 1-2 sentences of orienting context — the category, the core POV.}

## Core

- [{Page title}](https://{domain}/{path}): {8-15 word description of what's on it}
- [Pricing](https://{domain}/pricing): {what plans/model}

## Guides

- [{Guide title}](https://{domain}/{path}): {what question it answers}

## AEO Pages

- [What is {term}](https://{domain}/{path}): {the definition it owns}
- [{A} vs {B}](https://{domain}/{path}): {the comparison verdict}

## Proof

- [{Case study}](https://{domain}/{path}): {the result, with the metric}

## Optional

- [Blog](https://{domain}/blog): {what topics}
```

Rules:
- The `>` blockquote description is mandatory and must be self-contained.
- Every bullet: `[title](absolute-url): description`. Descriptions are for the
  model, not for SEO — say what's actually answerable on the page.
- Order sections by citation value (Core → Guides → AEO → Proof → Optional).
- Keep it scannable. A good llms.txt is 20-60 links, not the whole sitemap.

### Step 3 — (Optional) llms-full.txt
If asked for the full variant, produce `llms-full.txt`: same header, then for the
top 5-15 pages inline the actual extractable content (definition block, key
sections, FAQ) under `## {Page title}` headers. Pull real page content via WebFetch
— never fabricate. This is large; only build it when explicitly requested or when
the site is small enough that a model fetching every page is impractical.

## Output

Write to `clients/{slug}/production/technical/llms.txt` (and `llms-full.txt` if
built). Include a short deploy note:

> Place this file at `https://{domain}/llms.txt` (site root). Re-generate when you
> publish new AEO pages or restructure the site. Pair with `ai-crawler-fix` to make
> sure GPTBot/ClaudeBot/PerplexityBot are actually allowed in robots.txt — an
> llms.txt is useless if the crawlers are blocked.

## Quality Gate

- [ ] Every URL is absolute and resolves (no invented paths)
- [ ] The `>` description is present and self-contained
- [ ] AEO pages section leads with the highest-citation-value pages
- [ ] No banned phrases (check the client `voice.never_say` + `lessons.md`)
- [ ] File is curated (20-60 links), not a sitemap dump
- [ ] Deploy note tells the user where to put it and what to pair it with
