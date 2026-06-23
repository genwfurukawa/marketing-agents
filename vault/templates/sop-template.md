---
type: sop
status: draft
owner:
created: {{date}}
updated: {{date}}
tags: [sop]
---

# SOP: {{Title}}

> One-sentence summary of what this SOP produces and for whom.

## Trigger

When does this SOP run? Name the event, cadence, or condition that kicks it off.

- Example: "Run once per new client during onboarding."
- Example: "Run every Monday before sprint planning."
- Example: "Run whenever a new competitor ships a repositioning."

## Inputs

What must exist before you start? List credentials, files, access, and prior SOPs.

- Required credentials: `NOTION_TOKEN`, etc.
- Required files: `config.yaml`, `.env`
- Required access: Notion workspace admin, GitHub repo push
- Prior SOPs: [[00-index]] — link any SOPs that must run first

## Steps

Numbered, atomic, and copy-pasteable. Each step is one action with an expected result. A contractor who has never touched this system should be able to follow it.

1. **Step name.** Exact command or action.
   ```bash
   command --flag value
   ```
   Expected result: what you should see.

2. **Step name.** Next action.
   Expected result: what you should see.

3. **Step name.** And so on.

## Checks

How do you know it worked? Concrete, verifiable signals.

- [ ] File X exists at path Y
- [ ] Command returns exit code 0
- [ ] Notion page shows the expected children
- [ ] Value appears in `.env`

## Outputs

What exists after this SOP runs that did not exist before? Name the artifacts.

- New file: `path/to/file.md`
- New Notion page: `Client Name - Marketing Hub`
- New env vars: `NOTION_CLIENT_HUB_PAGE_ID=...`

## Escalation

What to do when it breaks.

- **Symptom:** API returns 401. **Fix:** Token is wrong or the integration is not shared to the target page. Re-grant access.
- **Symptom:** Script exits with partial progress. **Fix:** Read the printed IDs, delete the partial Notion resources, re-run.
- **Who to ping:** Gen for strategic calls. Claude Code for execution failures.

## Notes

Free-form space for gotchas, links to related SOPs, and historical context.

- Related: [[00-index]]
- Reference: link to docs or prior sessions
