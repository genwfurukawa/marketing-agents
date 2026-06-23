# Step 9: ICP Scoring + Signals

> **Question**: Can you turn visibility into conversations?

## Pipeline Position
- **Receives from**: Step 8 (Engagement data + ICP profiles)
- **Produces for**: Sales team (Scored accounts, pipeline signals, suggested follow-ups)
- **Agent**: `.claude/agents/icp-scorer-agent.md`
- **Schema**: `schemas/icp_scoring_input.json` -> `schemas/icp_scoring_output.json`

## Purpose
Identify who engaged with content and score them for pipeline readiness. Convert visibility into qualified conversations.

## Subfolders

| Folder | What Goes Here |
|--------|---------------|
| `engaged_accounts/` | Who engaged with content (companies, people) |
| `scoring_results/` | Fit + behavior + timing scores |
| `pipeline_signals/` | Ready-to-contact accounts |
| `suggested_followups/` | Recommended actions for sales/outreach |

## Checklist
- [ ] Identify who engaged with your content
- [ ] Score fit + behavior + timing
- [ ] Surface pipeline-ready accounts
- [ ] Suggested follow-ups generated

## Failure Signal
High engagement with no revenue impact. "Lots of views, no revenue."

## Output
ICP scoring system, weekly pipeline signals, CRM sync.
