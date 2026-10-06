---
type: sop-index
updated: {{date}}
tags: [sop, index]
---

# SOP Index — {{REPO_NAME}}

The master list of Standard Operating Procedures for {{REPO_NAME}}. The home for infrastructure and tooling SOPs (Notion, Slack, automations). Client-delivery SOPs live in the business repo, not here. If you run an internal process twice, it becomes an SOP.

## What is an SOP

An SOP is a procedure written so specifically that a new contractor could run it from scratch without a Slack message. It captures the trigger, inputs, steps, checks, outputs, and escalation path. SOPs are the system, not the service — they compound as the team scales.

Rules:

- One SOP per discrete process. No mega-docs.
- Every SOP uses the [[sop-template]].
- Numbered prefix (`01-`, `02-`, ...) for stable ordering and easy linking.
- If a step changes, the SOP changes that day. Stale SOPs are worse than no SOPs.
- Link wiki-style: `[[01-notion-setup]]` resolves in Obsidian.

## How to add a new SOP

1. Duplicate [[sop-template]] into `vault/sops/` with the next number prefix.
2. Fill in every section. Do not ship an SOP with "TBD" in Steps or Checks.
3. Add a row to the table below with status `draft`.
4. Once it has been run end-to-end by someone other than the author, flip status to `active`.

## SOPs

| # | SOP | Status | Owner | Purpose |
|---|-----|--------|-------|---------|
| 01 | [[01-notion-setup]] | active | {{OWNER}} | Stand up the Notion workspace, integration token, and per-client marketing hub |
| 02 | [[02-client-notifications]] | draft | {{OWNER}} | Per-client Slack channel + commentable Notion view, with Notion→Slack status automations |

## Related

- Template: [[sop-template]]
- Corrections log: `lessons.md` at repo root

## Status definitions

- **draft** — Written but not yet run end-to-end by a second person.
- **active** — Verified. Safe to hand to a contractor.
- **deprecated** — No longer used. Kept for historical context. Link to its replacement.

---

## Placeholders

When instantiating this template for a specific repo, replace:

- `{{REPO_NAME}}` — the name of the ops/agency repo (e.g., "Acme Ops")
- `{{OWNER}}` — default SOP owner (typically the founder or operator)
- `{{date}}` — today's date in YYYY-MM-DD form
