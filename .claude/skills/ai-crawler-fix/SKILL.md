---
name: ai-crawler-fix
description: "Use when an AI crawler audit found blocked bots, a missing/stale
sitemap, or no AI-bot policy, and you need the actual files to fix it. Triggers on:
'fix my robots.txt for AI', 'unblock GPTBot/ClaudeBot/PerplexityBot', 'generate a
robots.txt', 'my AI crawler audit failed', 'generate a sitemap', 'make AI bots able
to crawl my site', 'generate llms.txt', 'create an llms.txt', 'add an LLM manifest',
'make my site AI-crawlable'. Takes ai-crawler-audit-agent output (or a site URL) and
produces the three legs of technical AI readiness: a corrected robots.txt AI-bot
ruleset, a sitemap stub/recommendation, and a curated llms.txt.
This generates file content; it does not deploy anything."
metadata:
  version: 1.0.0
---

# AI Crawler Fix

`ai-crawler-audit-agent` *diagnoses* crawler-access problems (blocked bots, missing
sitemap, no llms.txt) and scores them. This skill *remediates* them: it generates
the corrected `robots.txt` AI-bot ruleset, a `sitemap.xml` recommendation or stub,
and a curated `llms.txt`. It closes the loop on Dimension 5 (Technical AI Readiness)
of the visibility rubric — audit finds, this fixes.

## Before Starting

You need one of:
1. **`ai-crawler-audit-agent` output** (preferred) — it already lists which bots are
   blocked, sitemap state, and structured-data gaps. Read it and target only the
   real problems.
2. **A site URL** — if no audit exists, WebFetch `{domain}/robots.txt` and
   `{domain}/sitemap.xml` first to see the current state, then fix from there.

Also confirm the **crawl intent**: does the user want AI answer-engine crawlers
allowed (almost always yes — that's the whole point of AEO) but AI *training*
crawlers handled separately? Default policy below allows retrieval bots and lets
the user decide on training/Common Crawl.

## The AI Crawler Landscape

| Bot | Operator | Purpose | Default policy |
|-----|----------|---------|----------------|
| `GPTBot` | OpenAI | ChatGPT browsing/retrieval | ALLOW |
| `OAI-SearchBot` | OpenAI | ChatGPT Search index | ALLOW |
| `ClaudeBot` | Anthropic | Claude web access | ALLOW |
| `PerplexityBot` | Perplexity | Perplexity real-time answers | ALLOW |
| `Perplexity-User` | Perplexity | User-initiated fetches | ALLOW |
| `Googlebot` | Google | Search + AI Overviews | ALLOW |
| `Google-Extended` | Google | Gemini/Bard training & grounding | ALLOW (note below) |
| `Applebot-Extended` | Apple | Apple Intelligence | user choice |
| `CCBot` | Common Crawl | Open crawl used in training sets | user choice |

Key distinction to explain to the user:
- **Retrieval/answer bots** (GPTBot, ClaudeBot, PerplexityBot, OAI-SearchBot,
  Googlebot) — block these and you are invisible in AI answers. For AEO, ALLOW.
- **Training-only bots** (Google-Extended for some uses, CCBot, Applebot-Extended)
  — allowing them helps a brand show up in model knowledge over time but some
  brands prefer to opt out of training. Surface the tradeoff; default to ALLOW for
  visibility but flag it as a real choice.

## Step 1 — Generate the robots.txt AI-bot block

Produce an explicit, per-bot ruleset. Do NOT rely on `User-agent: *` alone — many
sites set `Disallow: /` globally and accidentally block everything.

```
# --- AI answer-engine crawlers (allow for AEO visibility) ---
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Google-Extended
Allow: /

# --- Standard search ---
User-agent: Googlebot
Allow: /

# --- Optional: AI training crawlers (uncomment to allow) ---
# User-agent: CCBot
# Allow: /
# User-agent: Applebot-Extended
# Allow: /

# --- Everything else ---
User-agent: *
Allow: /
Disallow: /cart
Disallow: /checkout
Disallow: /account
Disallow: /*?*sessionid=

Sitemap: https://{domain}/sitemap.xml
```

Rules:
- Preserve any legitimate existing `Disallow` rules (private/app routes) — merge,
  don't blow away. If working from an existing robots.txt, show a diff.
- Always end with the `Sitemap:` line pointing at the real sitemap URL.
- If the audit found a global `Disallow: /` blocking AI bots, call it out
  explicitly as the root cause in the deploy note.

## Step 2 — Sitemap recommendation or stub

- **If a sitemap exists but is stale/incomplete** (per audit): list what's missing
  (new AEO pages, no `<lastmod>`, doesn't cover key pages) and give the exact
  entries to add.
- **If no sitemap exists**: generate a `sitemap.xml` stub from the page inventory
  (same inventory Step 3 uses — sitemap, audit top-pages, or pasted
  list). Include `<lastmod>` (use the known publish/update date; never fabricate a
  date — if unknown, omit `<lastmod>` for that URL rather than guessing).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemap.org/schemas/sitemap/0.9">
  <url>
    <loc>https://{domain}/</loc>
    <lastmod>{YYYY-MM-DD}</lastmod>
    <priority>1.0</priority>
  </url>
  <!-- one <url> per real page, AEO pages included -->
</urlset>
```

## Step 3 — Generate llms.txt

`llms.txt` is a Markdown file at the site root that gives LLMs a curated map of
the site: a one-line description, then sections of links with short context — a
prioritized, human-readable sitemap for AI crawlers. It is a discovery and
prioritization signal, not an access-control file (that's robots.txt, Step 1).
robots.txt access + a sitemap + llms.txt are the three legs of technical AI
readiness; ship all three together.

If `/llms.txt` already exists and the audit scored it fine, skip this step.

**Inputs:** the same page inventory as Step 2, plus the entity description — the
locked Tagline/Short description from `entity-authority-agent` output if it
exists, otherwise `clients/{slug}/config.yaml` `brand`. Never invent URLs — every
link must resolve.

Classify pages by AI-answer value and write, following the llms.txt spec:

```
# {Company Name}

> {One-sentence description — what the company does, for whom. Use the locked
> Tagline. No marketing fluff, no banned phrases.}

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
- Every bullet: `[title](absolute-url): description` — say what's actually
  answerable on the page, for the model, not for SEO.
- Order sections by citation value (Core → Guides → AEO → Proof → Optional).
  Drop login, cart, legal boilerplate, tag/pagination, anything thin.
- Curated, not a dump: a good llms.txt is 20-60 links.
- Optional `llms-full.txt` (only when explicitly requested): same header, then
  inline the actual extractable content of the top 5-15 pages under
  `## {Page title}` headers, pulled via WebFetch — never fabricated.

## Output

Write to `clients/{slug}/production/technical/`:
- `robots.txt` (the corrected ruleset, or a diff against the existing one)
- `sitemap.xml` (stub or the list of additions)
- `llms.txt` (and `llms-full.txt` if requested)

Plus a deploy note:
> Replace `https://{domain}/robots.txt` with this file. {If applicable: "Your
> current robots.txt blocks {bots} via {rule} — that's why you score 0 on crawler
> access."} Upload the sitemap to the site root and submit it in Google Search
> Console. Place llms.txt at `https://{domain}/llms.txt` and re-generate it when
> new AEO pages publish — an llms.txt is useless if the crawlers are blocked, so
> ship it with the robots.txt fix.

## Quality Gate

- [ ] Targets only the problems the audit actually found (no needless changes)
- [ ] Every retrieval/answer bot is explicitly addressed (not just `User-agent: *`)
- [ ] Existing legitimate Disallow rules preserved
- [ ] `Sitemap:` line present and correct
- [ ] No fabricated `<lastmod>` dates
- [ ] Training-bot tradeoff surfaced, not silently decided
- [ ] llms.txt: every URL absolute and resolving, `>` description self-contained,
      curated (20-60 links), no banned phrases (client `voice.never_say` + lessons)
- [ ] Deploy note names the root cause and ships all three legs together
