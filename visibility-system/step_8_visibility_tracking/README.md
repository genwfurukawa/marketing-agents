# Step 8: Visibility + Engagement Tracking

> **Question**: Do you learn from how the market responds?

## Pipeline Position
- **Receives from**: Step 7 (Published content URLs + publishing log)
- **Produces for**: Step 9 (Engagement data, theme performance, AI citation tracking)
- **Agent**: `.claude/agents/visibility-tracker-agent.md`
- **Schema**: `schemas/visibility_tracking_input.json` -> `schemas/visibility_tracking_output.json`

## Purpose
Track what's working to inform future content decisions. Turn engagement data into intelligence.

## Subfolders

| Folder | What Goes Here |
|--------|---------------|
| `engagement_data/` | Raw engagement metrics from all channels |
| `theme_performance/` | Which topics/themes resonate |
| `llm_visibility/` | AI citation tracking (ChatGPT, Claude, Perplexity mentions) |
| `weekly_reports/` | Summary reports and insights |

## Checklist
- [ ] Track topic resonance and engagement patterns
- [ ] Understand which ideas create pull
- [ ] Visibility data informs future decisions
- [ ] LLM visibility tracked where applicable

## Failure Signal
Vanity metrics, no iteration. No feedback loop.

## Output
Visibility dashboard and theme performance tracking.
