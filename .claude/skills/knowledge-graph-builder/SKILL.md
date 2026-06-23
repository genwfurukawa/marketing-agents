---
name: knowledge-graph-builder
description: "Use when building a brand's knowledge-graph entity — Wikidata,
Crunchbase, knowledge-panel signals — so AI engines recognize it as a real,
consistent entity. Triggers on: 'build my knowledge graph', 'get a Wikidata entry',
'knowledge panel', 'entity recognition for AI', 'Crunchbase/Wikidata optimization',
'make AI recognize my brand'. Turns entity-authority-agent's locked descriptions into
a concrete entity package + submission plan. The rubric scores knowledge-graph
presence (Dimension 6); nothing built it until now. Prepares submissions; the human
submits."
metadata:
  version: 1.0.0
---

# Knowledge Graph Builder

AI engines trust entities they can resolve. When a brand has a consistent presence
across the structured-data web — Wikidata, Crunchbase, G2, an Organization schema,
consistent founder bios — models recognize it as a real entity and are far more
willing to name and cite it. Dimension 6 (Brand Fingerprint) of the visibility rubric
scores exactly this: knowledge-graph presence (Wikidata + Wikipedia = 3 pts),
directory consistency, and locked entity descriptions. `entity-authority-agent`
produces the locked descriptions; this skill turns them into an actual entity package
and submission plan.

## What an AI-Legible Entity Looks Like

A resolvable entity has the same identity everywhere:
- A **Wikidata item** (the backbone of most knowledge graphs) with correct
  properties and identifiers
- A **Crunchbase** profile (founding, funding, people, category)
- Consistent **directory** presence (G2, Capterra, LinkedIn company page) using the
  same description and category
- **Organization JSON-LD** on the homepage with `sameAs` linking all of the above
- **Founder/leadership** identity consistent across bios (so the people resolve too)

Consistency is the whole game: the same name, category, one-line description, founding
year, and links everywhere. Divergence is what makes engines uncertain and reluctant
to cite.

## Before Starting

You need:
1. **The locked entity descriptions** (Tagline / Short / Medium / Long) + entity
   keywords from `entity-authority-agent`. If they don't exist, run that agent first —
   this skill depends on having one canonical description.
2. **Verifiable facts** — founding year, founders, HQ, funding (if public), category,
   official URL, official social handles. Use only facts you can source; Wikidata and
   Crunchbase require verifiability and will reject or flag unsourced claims.
3. **Eligibility check** — Wikipedia (not Wikidata) requires notability (significant
   independent coverage). Be honest: most early-stage B2B SaaS is *not* yet
   Wikipedia-eligible. Wikidata and Crunchbase have far lower bars and are the right
   first targets.

## How It Works

### Step 1 — Audit current entity presence
Search for the brand on Wikidata, Crunchbase, G2/Capterra, and via a "{brand}" +
"{brand} founder" web search. Record what exists, what's inconsistent (different
descriptions/categories/years across platforms), and what's missing. Inconsistency is
usually the biggest, cheapest win.

### Step 2 — Assemble the entity package
Produce the canonical fact sheet every platform will draw from:
- **Identity** — legal/display name, founding year, HQ, founders, category
- **Descriptions** — the locked Tagline/Short/Medium/Long (verbatim from
  `entity-authority-agent`)
- **Links (`sameAs` set)** — website, LinkedIn, Crunchbase, G2, X/social, any press
- **Identifiers** — domain, official handles; existing Wikidata QID if any

### Step 3 — Generate platform-specific submissions
- **Wikidata** — the item structure: label, description (the short one), and the key
  statements/properties with values and **sources** (instance of: business/software
  company; industry; inception; official website; founders; Crunchbase ID; etc.).
  Provide it as a clear property→value→source list a human can enter, and flag any
  value lacking a citable source (don't submit unsourced).
- **Crunchbase** — the profile fields: description, founded date, category, people,
  funding (if public), links.
- **Organization JSON-LD** — call `schema-generator` (type: `Organization`) with the
  locked description + the full `sameAs` set for the homepage.
- **Directory consistency fixes** — the exact description/category to standardize on
  G2, Capterra, LinkedIn so all match the canonical fact sheet.
- **Founder bios** — a standard bio paragraph (using locked entity keywords) to apply
  across LinkedIn, the site, podcast/press appearances.

### Step 4 — Eligibility-honest Wikipedia note
If the brand plausibly meets notability (multiple independent, substantial sources),
outline what a neutral Wikipedia article would need and the independent sources to
cite. If it doesn't, say so plainly and recommend revisiting after more press/coverage
accrues — a rejected or deleted article is worse than none.

## Output

Write to `clients/{slug}/production/entity/{YYYY-MM-DD}/`:
1. `entity_fact_sheet.md` — the canonical identity + descriptions + sameAs set
2. `wikidata_submission.md` — property→value→source list, ready to enter (flagged
   where a source is missing)
3. `crunchbase_profile.md` — the profile fields
4. `organization_schema.json` — the homepage JSON-LD (from `schema-generator`)
5. `consistency_fixes.md` — per-platform description/category corrections
6. `founder_bio.md` — the standard bio to deploy everywhere
7. A submission checklist (what the human submits where, in what order)

## Hand-offs

- Organization schema → ship on the homepage alongside `ai-crawler-fix` outputs
- Consistent descriptions reinforce `community-seeding` and every AEO page's author
- Re-check entity resolution in 4-8 weeks → does the brand now resolve cleanly and get
  named more often? (`aeo-engine-scan`)

## Quality Gate

- [ ] Every submitted fact is verifiable and sourced (unsourced values flagged, not submitted)
- [ ] Descriptions are verbatim-consistent with `entity-authority-agent` across all platforms
- [ ] `sameAs` set is complete and links resolve
- [ ] Wikipedia eligibility assessed honestly (no doomed article pushed)
- [ ] Organization JSON-LD generated via `schema-generator` (one Organization, not per-page)
- [ ] Directory inconsistencies named with the exact corrected text
- [ ] Output is a human-submittable package, not auto-submitted
