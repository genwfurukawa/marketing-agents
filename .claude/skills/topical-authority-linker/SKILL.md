---
name: topical-authority-linker
description: "Use when a site has AEO pages but they're not internally linked into a
hub-and-spoke that builds topical authority for AI crawlers. Triggers on: 'audit my
internal links', 'build topical authority', 'hub and spoke linking', 'how should I
link my AEO pages', 'internal linking for AEO', 'my pages are orphaned', 'connect my
content cluster'. Compares a site's existing internal links against the planned
architecture from ai-content-architect-agent and outputs the specific links to add.
Produces a linking plan, not live site changes."
metadata:
  version: 1.0.0
---

# Topical Authority Linker

`ai-content-architect-agent` *plans* the hub-and-spoke content architecture — which
pillar pages anchor which clusters. Nothing audits whether the live site actually
links that way. This skill closes that gap: it maps the real internal-link graph,
compares it to the intended topical clusters, and outputs the exact links to add so
crawlers (and AI models inferring topical authority) see a coherent cluster instead
of orphaned pages.

## Why Internal Linking Matters for AEO

AI crawlers infer topical authority partly from internal structure: a tightly
interlinked cluster around a pillar signals depth on that topic, which raises the
odds the cluster's pages get surfaced and cited. Dimension 4 (Content Architecture)
of the visibility rubric scores internal-linking depth — hub-and-spoke = 2 pts,
partial = 1, flat = 0. Orphaned AEO pages (no inbound internal links) are the most
common failure: great pages no crawler can find a path to.

## The Hub-and-Spoke Model

- **Hub (pillar)** — a broad page owning a topic (e.g. a `glossary`, `what_is`, or
  `buyer_guide` for the category). Links out to every spoke.
- **Spokes** — specific pages in that topic (comparisons, alternatives, use-cases,
  integrations, problem-solution). Each links UP to the hub and ACROSS to 2-4
  sibling spokes.
- **Rule of thumb:** every page reachable within 2-3 clicks of the homepage; no
  orphans; bidirectional hub↔spoke; sibling cross-links only where contextually
  relevant (don't link-stuff).

## Before Starting

You need:
1. **The intended architecture** — `ai-content-architect-agent` output (clusters +
   page roadmap) if it exists; otherwise derive clusters from the 14 page types
   present on the site (group by topic).
2. **The current page inventory + link graph** — from one of:
   - a crawl/sitemap + WebFetch of each page to read its internal `<a href>` links,
   - the audit's top-pages data,
   - or a pasted list. For a small site, WebFetch each page; for large, work from the
     pages that matter (AEO pages + pillars).
3. **The domain** (to distinguish internal from external links).

## How It Works

### Step 1 — Build the current link graph
For each page in scope, list its internal outbound links and infer inbound links.
Identify:
- **Orphans** — pages with zero internal inbound links (critical: crawlers may never
  reach them)
- **Dead-end hubs** — pillar pages that don't link out to their spokes
- **Missing up-links** — spokes that don't link back to their hub
- **Cross-cluster noise** — links that blur topical focus

### Step 2 — Overlay the intended clusters
Map each page to its cluster (hub + spokes). For each cluster, compute what links
*should* exist vs what *does*.

### Step 3 — Generate the link plan
Output the specific additions, each as: source page → target page, suggested anchor
text (descriptive, query-relevant, not "click here"), and why. Prioritize:
1. Fix orphans first (add at least one inbound internal link from the relevant hub)
2. Complete hub→spoke and spoke→hub pairs
3. Add high-relevance sibling cross-links (cap ~2-4 per page)

## Output

Write to `clients/{slug}/research/internal-linking/{YYYY-MM-DD}.md`:
1. **Cluster map** — hub + spokes per topic, with current vs target link counts
2. **Orphan list** — pages with no internal inbound links (fix first)
3. **Link additions table** — | source | target | anchor text | priority | why |
4. **Anchor-text guidance** — descriptive, varied, query-relevant; avoid exact-match
   stuffing and "read more"
5. **Architecture score** — current hub-and-spoke depth (flat/partial/full) mapped to
   the Dimension 4 sub-score, and where it lands after the plan

## Hand-offs

- The link additions are a build task for whoever owns the CMS (not auto-applied)
- New AEO pages from `aeo-page-generator` should be added to the relevant cluster
  here so they never ship as orphans
- Re-run after major content additions

## Quality Gate

- [ ] Every page mapped to a cluster (hub or spoke)
- [ ] Orphans explicitly identified and prioritized first
- [ ] Each suggested link has source, target, anchor text, and a reason
- [ ] Anchor text is descriptive and varied (no "click here", no exact-match stuffing)
- [ ] Sibling cross-links capped (no link-stuffing)
- [ ] Current + projected Dimension 4 internal-linking sub-score stated
