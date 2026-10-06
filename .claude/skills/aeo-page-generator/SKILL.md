---
name: aeo-page-generator
description: "Generate publish-ready AEO pages across all 14 page types (comparison, alternatives, what-is, best-tools, problem-solution, use-case, integration, faq-hub, glossary, statistics, buyer-guide, competitor-review, roi-business-case, case-study). Reads the structural template for the chosen type, generates the draft, then auto-chains aeo-checker -> aeo-injector -> voice-validator. Use when the user says 'create an AEO page', 'generate a comparison page', 'build an alternatives page', 'write a what-is page', 'make a FAQ hub', or any phrasing requesting one of the 14 page types."
metadata:
  version: 1.0.0
---

# AEO Page Generator

You generate complete, publish-ready AEO pages structured for AI retrieval. You cover all 14 page types in `templates/aeo_page_types/`. Every page you produce ships through the quality chain automatically: aeo-checker -> aeo-injector -> voice-validator.

This skill is the single path for AEO page generation, all 14 types.

---

## When To Use

User says any of:
- "create an AEO page"
- "generate a {page_type} page"
- "write a comparison page" / "X vs Y page"
- "build an alternatives page"
- "make a what-is page" / "definition page"
- "create a FAQ hub" / "FAQ page"
- "build a use case page"
- "write an integration page"
- "make a best tools list"
- "produce a glossary"
- "build a buyer's guide"
- "write a competitor review"
- "make an ROI page" / "business case page"
- "draft a case study page"
- "build a problem-solution page"
- "build a statistics/research page"

---

## The 14 Page Types

| Type slug | Template file | Best for | Schema |
|---|---|---|---|
| `comparison` | product_comparison.md | "{A} vs {B}" queries | Article + FAQPage |
| `alternatives` | alternatives.md | "best {category} alternatives to {brand}" | ItemList + FAQPage |
| `what_is` | what_is_definition.md | "what is {term}" queries | DefinedTerm + FAQPage |
| `best_tools` | best_tools_list.md | "best {category} tools" listicle | ItemList + FAQPage |
| `problem_solution` | problem_solution.md | "how to {solve problem}" MOFU | Article + FAQPage |
| `use_case` | use_case_page.md | "{product} for {specific use case}" | Article + FAQPage |
| `integration` | integration.md | "{A} + {B} integration" co-occurrence | HowTo + FAQPage |
| `faq_hub` | faq_answer_hub.md | 20-40 Q topical hub | FAQPage |
| `glossary` | glossary.md | category knowledge base | DefinedTermSet |
| `statistics` | statistics_research.md | "X statistics" data queries | Dataset + FAQPage |
| `buyer_guide` | buyer_guide.md | comprehensive evaluation guide | Article + FAQPage |
| `competitor_review` | competitor_review.md | "{competitor} review" honest assessment | Review + FAQPage |
| `roi_business_case` | roi_business_case.md | "ROI of {category}" budget justification | Article + FAQPage |
| `case_study` | case_study_page.md | "{client} + {product} case study" | Article + FAQPage |

---

## Required Inputs

Required for every type:
- `page_type` (one of the 14 slugs above)
- `topic` (the specific subject)
- `client_slug` (if omitted, resolve via the `CLIENT_CONFIG` env var pointing at the client's config.yaml)

Type-specific required inputs:

| page_type | Additional inputs |
|---|---|
| `comparison` | `product_a`, `product_b` |
| `alternatives` | `incumbent_brand`, `alternatives_list` (5-7) |
| `what_is` | `term`, `category` |
| `best_tools` | `category`, `tools_to_include` (5-10) |
| `problem_solution` | `problem`, `target_icp` |
| `use_case` | `product`, `use_case_scenario`, `target_icp` |
| `integration` | `product_a`, `product_b` |
| `faq_hub` | `topic_cluster`, `target_q_count` (default 25) |
| `glossary` | `category`, `term_count` (default 40) |
| `statistics` | `topic`, `data_sources` (cite URLs) |
| `buyer_guide` | `category`, `target_icp` |
| `competitor_review` | `competitor` |
| `roi_business_case` | `category`, `target_icp`, `cost_range` |
| `case_study` | `client_name`, `product`, `results_data` |

If required inputs are missing, ask for them before generating.

---

## Process

1. **Read context files in parallel:**
   - `clients/{client}/config.yaml` (brand identity, voice, ICP, competitors)
   - `lessons.md` (compounding corrections)
   - `clients/{client}/config/voice-guide.md` (voice rules)
   - `clients/{client}/config/icp-psyche.md` (deep ICP)
   - `templates/aeo_page_types/{page_type_template_file}.md` (structural template)
   - `clients/{client}/config/brand-brain.md` (if present)

2. **Web research pass.** For any type that needs real data (comparison, alternatives, best_tools, statistics, competitor_review, integration), use WebSearch + WebFetch to pull pricing, features, reviews, citations. Never hallucinate tables.

3. **Generate the draft.** Follow the template's required structure exactly. Required elements every page MUST have:
   - 40-60 word extraction block immediately after H1
   - FAQ section (5-7 Qs for most types, 20-40 for faq_hub)
   - Section headings phrased as questions where natural
   - Internal link placeholders to related pages
   - Specific numbers (no "many," "lots," "various")
   - JSON-LD block at the bottom (call schema-generator skill)

4. **Auto-chain quality gates.** After writing the draft:
   - Call `aeo-checker` skill on the draft. Get the AEO_REPORT.
   - If aeo-checker finds gaps, call `aeo-injector` skill with the draft + report.
   - Call `voice-validator` skill on the injected draft.
   - If voice-validator fails, fix and re-run (max 2 cycles).
   - **Cross-model gate (mandatory, final):** dispatch the `aeo-cross-model-reviewer`
     agent on the post-validation draft. It runs on a DIFFERENT model on purpose - the
     same-model checks above bless patterns this writer (and its gold-standard example)
     already treat as correct. Pass it the draft path, page_type, client slug, the
     strategic brief, and the gold-standard page it mirrors. It returns PASS/FAIL with
     severity-tagged findings and never edits the page.
     - Apply every BLOCKER and SHOULD-FIX that is an unambiguous mechanical fix (a banned
       term, a wrong fact, a missing canonical phrase), then note them in the report.
     - For any finding the reviewer marks **systemic** (the gold-standard page shares it)
       or any genuine judgment call (a voice-guide rule that conflicts with AEO strategy),
       do NOT silently rewrite - surface it to the human with the reviewer's evidence and
       let them decide, then record the resolution as a lesson in `lessons.md`.
     - Never ship a draft to publish with an open BLOCKER.

5. **Generate schema markup.** Call `schema-generator` skill with the page_type and the draft. Embed returned JSON-LD at the bottom of the page.

6. **Write outputs.** (In a standalone client repo, `clients/{client}/` means the repo root.)

```
clients/{client}/production/aeo_pages/{page_type}/{topic_slug}/
  draft.md              (final post-validation draft)
  draft_pre_check.md    (draft before quality gates, for diff)
  aeo_report.md         (aeo-checker output)
  voice_report.md       (voice-validator output)
  schema.jsonld         (structured data block)
  metadata.yaml         (page_type, topic, inputs, generated_at)
```

7. **Suggest internal links.** After generation, surface 3-5 existing pages in the repo that should link to this new page (and vice versa) based on topic clustering.

---

## Critical Rules

1. **Templates are not suggestions.** Every required structural element from `templates/aeo_page_types/{type}.md` must be in the output. The extraction block, the comparison table, the FAQ block, the verdict box - all required.

2. **Specificity over fluency.** "30 minutes per month" beats "fast and easy." "$8,500/month" beats "affordable." Templates require specific numbers; do not soften.

3. **Honest comparison.** When generating comparison or competitor_review pages, the competitor MUST win some rows. LLMs detect one-sided content and discount it.

4. **Auto-chain is mandatory.** Never deliver a draft without running aeo-checker -> aeo-injector -> voice-validator -> aeo-cross-model-reviewer. The user expects validated output, cross-checked by a different model, not a first draft. The cross-model gate is the last step and is not optional - it exists because same-model checks miss inherited and habitual errors.

5. **JSON-LD is mandatory.** Every page ships with structured data. Use `schema-generator` skill.

6. **Voice rules apply to AEO pages too.** Banned phrases in `clients/{client}/config.yaml` voice.never_say apply equally. Run voice-validator. No exceptions.

7. **Web research before tables.** Do not invent pricing, feature lists, or competitor data. Use WebSearch/WebFetch. Cite sources for statistics pages.

---

## Auto-Chain Sequence (Explicit)

```
1. Read context files (parallel)
2. Read template for page_type
3. Web research (if applicable)
4. Generate draft -> write to draft_pre_check.md
5. Call aeo-checker -> get AEO_REPORT
6. If FAIL items exist:
   a. Call aeo-injector with draft + AEO_REPORT
   b. Write injected version to draft.md
7. Call voice-validator on draft.md
8. If voice FAIL:
   a. Fix flagged sentences
   b. Re-run voice-validator (max 2 cycles)
9. Dispatch aeo-cross-model-reviewer agent (DIFFERENT model) on draft.md
   a. Apply unambiguous BLOCKER/SHOULD-FIX mechanical fixes
   b. Surface systemic / judgment-call findings to the human; record resolution in lessons.md
   c. Do not proceed to publish with an open BLOCKER
10. Call schema-generator with page_type + draft.md
11. Embed schema.jsonld at the bottom of draft.md
12. Write all artifacts to clients/{client}/production/aeo_pages/{page_type}/{topic_slug}/
13. Surface 3-5 internal link suggestions
14. Report: word count, FAQ count, schema types, validation pass status, cross-model verdict
```

---

## Related

- Strategy: `ai-content-architect-agent` (plans which page types to build)
- Quality gates: `aeo-checker`, `aeo-injector`, `voice-validator`
- Schema: `schema-generator`
- Distribution: `/distribute` once published
