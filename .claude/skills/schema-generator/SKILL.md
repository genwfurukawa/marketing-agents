---
name: schema-generator
description: "Generate schema.org JSON-LD structured data blocks for AEO pages and any web content. Supports FAQPage, Product, AggregateRating, Organization, BreadcrumbList, Article, HowTo, SoftwareApplication, DefinedTerm, DefinedTermSet, ItemList, Dataset, Review. Use when the user says 'generate schema', 'add JSON-LD', 'add structured data', 'add schema markup', 'add FAQ schema', or automatically as the final step in aeo-page-generator."
metadata:
  version: 1.0.0
---

# Schema Generator

You generate valid schema.org JSON-LD blocks for any page or content type. LLMs use structured data as a synthesis signal - schema markup is required on every AEO page the system produces.

---

## When To Use

User says any of:
- "generate schema"
- "add JSON-LD" / "add structured data"
- "add schema markup"
- "add FAQ schema"
- "create Product schema"
- "wrap this with Organization schema"

Auto-invoke when:
- `aeo-page-generator` skill calls you at its final step
- Any agent producing publish-ready web content needs structured data

---

## Required Inputs

Required:
- `content` (the page draft, OR explicit structured fields)
- `schema_types` (one or more from the supported list, OR `auto` to infer from content)

Optional:
- `page_type` (one of the 14 AEO page types - drives schema type defaults)
- `client_slug` (defaults to current repo brand from clients/{client}/config.yaml)
- `canonical_url` (the eventual published URL)

---

## Supported Schema Types

| Schema | Use case | Required fields |
|---|---|---|
| `FAQPage` | Any page with Q&A blocks (most AEO pages) | `name`, `mainEntity[]` (Question + acceptedAnswer) |
| `Article` | Blog posts, framework posts, POV content | `headline`, `author`, `datePublished`, `description` |
| `Product` | Comparison, alternatives, best-tools, competitor-review | `name`, `description`, `brand`, `offers`, optional `aggregateRating` |
| `AggregateRating` | When review/rating data is available | `ratingValue`, `reviewCount`, `bestRating`, `worstRating` |
| `Review` | competitor_review pages | `itemReviewed`, `author`, `reviewRating`, `reviewBody` |
| `Organization` | Site-wide / About page | `name`, `url`, `logo`, `sameAs[]`, `description` |
| `BreadcrumbList` | All hub pages | `itemListElement[]` (position, name, item) |
| `HowTo` | integration, problem_solution pages with steps | `name`, `step[]` (HowToStep with name, text) |
| `SoftwareApplication` | SaaS product pages | `name`, `applicationCategory`, `operatingSystem`, `offers` |
| `DefinedTerm` | what_is pages | `name`, `description`, `inDefinedTermSet` |
| `DefinedTermSet` | glossary pages | `name`, `hasDefinedTerm[]` |
| `ItemList` | best_tools, alternatives | `itemListElement[]` (position, name, url) |
| `Dataset` | statistics pages | `name`, `description`, `creator`, `temporalCoverage` |

---

## Default Schema By Page Type

When `page_type` is provided and `schema_types: auto`:

| page_type | Default schemas |
|---|---|
| comparison | Article + FAQPage + Product (x2) |
| alternatives | Article + FAQPage + ItemList |
| what_is | Article + FAQPage + DefinedTerm |
| best_tools | Article + FAQPage + ItemList |
| problem_solution | Article + FAQPage + HowTo |
| use_case | Article + FAQPage |
| integration | Article + FAQPage + HowTo |
| faq_hub | FAQPage (extended, 20-40 Q) + Article |
| glossary | DefinedTermSet + Article |
| statistics | Dataset + FAQPage + Article |
| buyer_guide | Article + FAQPage |
| competitor_review | Review + FAQPage + Product |
| roi_business_case | Article + FAQPage |
| case_study | Article + FAQPage |

Site-wide additions (every page): `Organization` + `BreadcrumbList`.

---

## Process

1. **Read clients/{client}/config.yaml** to get brand identity (name, website, logo URL, founder).

2. **Parse the content.** Extract:
   - `headline` from H1
   - `description` from extraction block (first 40-60 word paragraph)
   - FAQ blocks (look for `### FAQ` or `## Frequently Asked Questions` then parse Q/A pairs)
   - Steps (look for ordered lists under sections with "step" / "how to" headings)
   - Product mentions (for comparison/alternatives/best_tools)
   - Comparison tables (for ratings, pricing)

3. **Generate each requested schema block.** Use the templates in `references/{type}.json` as starting points. Fill in the parsed values.

4. **Validate.** Every block must include `"@context": "https://schema.org"` and `"@type": "{SchemaType}"`. Nested types require their own `@type`.

5. **Combine.** Wrap multiple schema blocks in a single `<script type="application/ld+json">` array, OR output as separate script tags (user's choice).

6. **Write output.**

```
{output_dir}/schema.jsonld          (the combined JSON-LD block)
{output_dir}/schema_validation.md   (which fields were filled, which fell back to defaults)
```

If called from `aeo-page-generator`, return the JSON-LD string for inline embedding.

---

## Output Format

Single combined block (default):

```html
<script type="application/ld+json">
[
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "...",
    "author": {...},
    "datePublished": "...",
    "description": "..."
  },
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [...]
  }
]
</script>
```

---

## Critical Rules

1. **Never invent ratings or review counts.** If `AggregateRating` data is not in the content, do not emit AggregateRating. Adding fake ratings violates schema.org guidelines and gets pages penalized.

2. **Author must be the real founder.** Read from `clients/{client}/config.yaml` `brand.founder`. Default to Organization if no individual author is named in the content.

3. **Canonical URL must be real.** If `canonical_url` is not passed, use a placeholder `{{CANONICAL_URL}}` and flag in the validation report. Never emit `https://example.com`.

4. **FAQPage requires self-contained answers.** Each `acceptedAnswer.text` must answer the question without referencing "above" or "below." If parsed answers contain such references, flag for rewrite.

5. **One Organization per site, not per page.** Organization schema goes on the homepage and about page. For interior pages, link to the Organization via `publisher` field on Article, don't re-emit it.

6. **No duplicate schemas.** If the page already contains a JSON-LD block, parse it, merge, and replace - do not append a second block.

7. **Validate against schema.org spec.** After generation, mentally walk through schema.org/{Type} required fields. Missing required fields = invalid schema = wasted markup.

8. **Sentence-case property values.** "Best CRM Tools for Startups" not "best crm tools for startups".

---

## Related

- Called by: `aeo-page-generator` (auto-chain final step)
- Validate published markup: Ahrefs `site-audit-page-content` MCP tool, or schema.org/validator
- Update: when schema.org adds new types or required fields, update this skill's `references/` directory
