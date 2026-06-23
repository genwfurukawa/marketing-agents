# Templates

Reusable scaffolding instantiated per-client or per-content-piece. Two
physical homes: `templates/` (production templates) and `vault/` (SOP +
note templates).

## AEO Page Types (14 templates)

The structural backbone for AI-retrievable pages. Used by the
[aeo-page-generator](.claude/skills/aeo-page-generator/SKILL.md) skill.

| Template | Page type |
|----------|-----------|
| [alternatives.md](templates/aeo_page_types/alternatives.md) | "X alternatives" pages |
| [best_tools_list.md](templates/aeo_page_types/best_tools_list.md) | "Best tools for X" lists |
| [buyer_guide.md](templates/aeo_page_types/buyer_guide.md) | Buyer's guide |
| [case_study_page.md](templates/aeo_page_types/case_study_page.md) | Customer case study |
| [competitor_review.md](templates/aeo_page_types/competitor_review.md) | "X review" pages |
| [faq_answer_hub.md](templates/aeo_page_types/faq_answer_hub.md) | FAQ answer hub |
| [glossary.md](templates/aeo_page_types/glossary.md) | Glossary / definitions |
| [integration.md](templates/aeo_page_types/integration.md) | Integration / "X + Y" pages |
| [problem_solution.md](templates/aeo_page_types/problem_solution.md) | Problem → solution |
| [product_comparison.md](templates/aeo_page_types/product_comparison.md) | "X vs Y" comparison |
| [roi_business_case.md](templates/aeo_page_types/roi_business_case.md) | ROI / business case |
| [statistics_research.md](templates/aeo_page_types/statistics_research.md) | Statistics / research |
| [use_case_page.md](templates/aeo_page_types/use_case_page.md) | Use case page |
| [what_is_definition.md](templates/aeo_page_types/what_is_definition.md) | "What is X" definition |

## Brand Brain

- [BRAND_BRAIN_TEMPLATE.md](templates/brand_brain/BRAND_BRAIN_TEMPLATE.md)
  — 12-section brand brain template instantiated per client during
  `/clone-ops` or `/build-brand-brain`

## Monthly Briefing

- [report.html.template](templates/monthly_briefing/report.html.template)
  — standalone HTML briefing template used by `/monthly-briefing`

## Audit Blueprint Scripts (4 .py.template files)

Script templates that get copied + customized per audit engagement. Used
by `/audit-blueprint`.

| Template | Purpose |
|----------|---------|
| [analyze_perplexity.py.template](templates/audit_blueprint_scripts/analyze_perplexity.py.template) | Analyze Perplexity citation data |
| [build_query_bank.py.template](templates/audit_blueprint_scripts/build_query_bank.py.template) | Build the audit query bank |
| [build_data_deliverables.py.template](templates/audit_blueprint_scripts/build_data_deliverables.py.template) | Compile audit data deliverables |
| [claude_direct_scan.py.template](templates/audit_blueprint_scripts/claude_direct_scan.py.template) | Direct Claude-API citation scan |

## Vault Templates (notes + SOPs)

| Template | Purpose |
|----------|---------|
| [vault/templates/sop-template.md](vault/templates/sop-template.md) | Generic SOP scaffold |
| [vault/templates/daily-note-template.md](vault/templates/daily-note-template.md) | Daily note scaffold for the Obsidian vault |
| [vault/sops/00-index-template.md](vault/sops/00-index-template.md) | SOP index template |
| [vault/sops/01-notion-setup-template.md](vault/sops/01-notion-setup-template.md) | Notion HQ setup SOP template |

## Ops Templates

| Template | Purpose |
|----------|---------|
| [docs/scheduled-jobs-template.md](docs/scheduled-jobs-template.md) | Scaffold for declaring recurring/scheduled jobs in a client engagement |
