# Step 1: ICP + Category Definition

> **Question**: What reality are we operating in?

## Pipeline Position
- **Receives from**: Raw idea, keyword, or market signal
- **Produces for**: Step 2 (ICP-validated topic with buyer context)
- **Agent**: `.claude/agents/icp-definition-agent.md`
- **Schema**: `schemas/icp_definition_input.json` -> `schemas/icp_definition_output.json`

## Purpose
Define who we're talking to and what market we're in. This is the foundation that prevents generic, broadly-applicable content.

## Subfolders

| Folder | What Goes Here |
|--------|---------------|
| `icp_profiles/` | Detailed ICP documents with firmographics, pain points, motivations |
| `category_maps/` | Category landscape analysis, market positioning |
| `buying_triggers/` | What makes them buy, timing signals |
| `competitors/` | Alternative solutions they consider |

## Checklist
- [ ] A specific ICP, not "B2B" or "mid-market"
- [ ] Clear buying triggers and deal context
- [ ] Competitive alternatives buyers compare you against
- [ ] What makes them hesitate

## Failure Signal
Content feels generic, safe, or broadly applicable.

## Output
ICP and Category Map ready for use in all downstream steps.
