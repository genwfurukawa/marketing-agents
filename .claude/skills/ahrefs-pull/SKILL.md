---
name: ahrefs-pull
description: "Pull AI visibility data from Ahrefs Brand Radar (SOV, cited domains/pages, mentions, AI responses) and write to research/ahrefs/{YYYY-MM}/. Use when the user says 'pull ahrefs', 'pull brand radar', 'pull visibility', 'refresh visibility data', or as a precursor to /sprint audit, /monthly-briefing, or /competitive-monitor. Calculates Source Control Rate, computes deltas vs prior pull, renders scorecard/time-series charts via Ahrefs render tools."
metadata:
  version: 1.0.0
---

# Ahrefs Brand Radar Pull

You pull the full Brand Radar dataset for a client and write structured outputs that downstream skills/commands consume. You are the primary visibility data source for the visibility ops methodology. The legacy Perplexity-only scanner at `scripts/aeo_audit/` is retained for ad-hoc use only.

---

## Why This Exists

Visibility tracking moved from Perplexity-only (`scripts/aeo_audit/`) to Ahrefs Brand Radar in May 2026. Brand Radar covers Perplexity, ChatGPT, Google AI Overviews, and Claude in one API with historical tracking baked in. This skill is the canonical entrypoint.

---

## Inputs

Required:
- `client_slug` (default: derive from current working directory or clients/{client}/config.yaml `brand.name`)

Optional:
- `report_id` - Ahrefs Brand Radar report ID. If missing, the skill calls `management-brand-radar-reports` to list reports and picks the one matching the brand domain.
- `lookback_days` - default 28
- `mode` - `weekly` (default) or `monthly`. Weekly writes to `research/ahrefs/{YYYY-Www}/`, monthly writes to `research/ahrefs/{YYYY-MM}/`.

---

## What This Skill Pulls

Call these Ahrefs MCP tools in parallel where independent:

| Tool | Why | Output field |
|---|---|---|
| `mcp__claude_ai_Ahrefs__brand-radar-sov-overview` | Current Share of Voice for the brand vs competitors | `sov` |
| `mcp__claude_ai_Ahrefs__brand-radar-sov-history` | SOV trend over lookback window | `sov_history` |
| `mcp__claude_ai_Ahrefs__brand-radar-mentions-overview` | Current mention count + sentiment | `mentions` |
| `mcp__claude_ai_Ahrefs__brand-radar-mentions-history` | Mention trend | `mentions_history` |
| `mcp__claude_ai_Ahrefs__brand-radar-impressions-overview` | Estimated impressions in AI responses | `impressions` |
| `mcp__claude_ai_Ahrefs__brand-radar-impressions-history` | Impressions trend | `impressions_history` |
| `mcp__claude_ai_Ahrefs__brand-radar-cited-domains` | Which domains AI cites when answering brand queries | `cited_domains` |
| `mcp__claude_ai_Ahrefs__brand-radar-cited-pages` | Specific URLs cited | `cited_pages` |
| `mcp__claude_ai_Ahrefs__brand-radar-ai-responses` | Sample AI responses for top queries | `ai_responses` |
| `mcp__claude_ai_Ahrefs__management-brand-radar-prompts` | Tracked prompts (the query bank) | `prompts` |

Reminder: monetary values in Ahrefs responses are USD cents. Divide by 100.

When a tool response includes `render_with` in its metadata, you MUST call the specified render tool with the returned data.

---

## Process

1. **Locate the client.** Read `clients/{client}/config.yaml` for `brand.name`, `brand.website`, competitors. If a `client_slug` is passed, look up at `clients/{client_slug}/config.yaml` first.

2. **Resolve the Brand Radar report.** If no `report_id` was passed, call `management-brand-radar-reports` and pick the one with a domain match against `brand.website`. If none exists, return a clear error: "No Brand Radar report found for {domain}. Create one in Ahrefs first, then re-run."

3. **Parallel pulls.** Call all 10 endpoints above in parallel. Use the resolved `report_id` and `lookback_days`.

4. **Calculate Source Control Rate.** From `cited_domains`, count citations to owned domains (the client domain + known subdomains from `clients/{client}/config.yaml` `brand.website` and `brand.owned_domains`). Divide by total citation count. This is the north-star KPI.

5. **Compute deltas.** Read the prior pull at `research/ahrefs/_latest/data.json` (symlinked). For each metric (sov, mentions, impressions, source_control_rate), compute absolute delta and % change.

6. **Write structured output.** Create `research/ahrefs/{period}/data.json` with this schema:

```json
{
  "client_slug": "acme",
  "report_id": "...",
  "period": "2026-W19",
  "pulled_at": "2026-05-11T08:00:00Z",
  "lookback_days": 28,
  "metrics": {
    "sov": { "value": 0.18, "delta_abs": 0.03, "delta_pct": 0.20 },
    "mentions": { "value": 142, "delta_abs": 18, "delta_pct": 0.145 },
    "impressions": { "value": 12400, "delta_abs": 2100, "delta_pct": 0.20 },
    "source_control_rate": { "value": 0.34, "delta_abs": 0.05, "delta_pct": 0.17 }
  },
  "sov_history": [...],
  "mentions_history": [...],
  "impressions_history": [...],
  "cited_domains": [...],
  "cited_pages": [...],
  "ai_responses": [...],
  "prompts": [...],
  "competitors": [
    { "domain": "competitor1.com", "sov": 0.42, "trend": "up" },
    ...
  ]
}
```

7. **Write a markdown summary.** Create `research/ahrefs/{period}/summary.md` with:
   - Top-line scorecard (4 metrics, deltas, arrows)
   - Top 5 queries where you moved up
   - Top 5 queries where competitors moved up (gap queries)
   - New cited domains (potential earned-authority targets)
   - Sentiment shifts

8. **Update `_latest` symlink.** Point `research/ahrefs/_latest/` to the new period folder so deltas work next run.

9. **Sync to Notion.** Append a row to the Visibility Scores DB with the period, four metric values, and a link to the markdown summary. Use the Notion MCP server.

10. **Render scorecard inline.** Call `mcp__claude_ai_Ahrefs__render-scorecard` with the four metrics so the user sees the result in chat.

---

## Output

```
research/ahrefs/
  _latest/                         (symlink to most recent period)
  2026-W19/
    data.json                      (structured payload)
    summary.md                     (human-readable)
    raw/
      sov_overview.json
      sov_history.json
      mentions.json
      cited_domains.json
      ...
```

---

## When to Call Other Skills After

- After pulling: if Source Control Rate dropped >10% week-over-week, recommend running `content-refresh-agent`.
- If a competitor's SOV jumped >15%, recommend `/competitive-monitor`.
- For monthly pulls: chain into `/monthly-briefing` automatically.

---

## Notion Sync Schema

Visibility Scores DB columns:
- `period` (title)
- `pulled_at` (date)
- `sov` (number)
- `mentions` (number)
- `impressions` (number)
- `source_control_rate` (number)
- `delta_sov` (number)
- `delta_mentions` (number)
- `delta_source_control` (number)
- `summary_link` (url to the markdown)

---

## Critical Rules

1. **Never invent metric values.** If an Ahrefs tool returns empty data, write `null` in the JSON and a `data_quality` warning in the summary.
2. **Always call `render-scorecard` and `render-time-series-chart` when Ahrefs metadata includes `render_with`.** The MCP server requires it.
3. **Source Control Rate is the north star.** Always include it in the summary, always sync to Notion.
4. **Deltas require a prior pull.** First-ever pull has no deltas - explicitly note "baseline" in the summary.
5. **Owned domain matching.** Match cited domains against `brand.website` AND subdomains (blog.x.com, docs.x.com, etc.). Pull from `clients/{client}/config.yaml` `brand.owned_domains` array if set.
