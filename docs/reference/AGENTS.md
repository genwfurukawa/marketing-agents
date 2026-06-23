# Agents

All 34 client-agnostic agents, grouped by stage. Each agent is a role
definition Claude Code can spawn via the Agent tool. Files live in
`.claude/agents/` so Claude Code's auto-discovery works.

## Foundation (ICP, Positioning, Voice)

| Agent | Role |
|-------|------|
| [foundations-orchestrator](.claude/agents/foundations-orchestrator.md) | Master orchestrator for Steps 1–3; coordinates ICP, positioning, voice builds |
| [icp-definition-agent](.claude/agents/icp-definition-agent.md) | Step 1 — produces validated ICP profile |
| [positioning-agent](.claude/agents/positioning-agent.md) | Step 2 — develops differentiated positioning with contrarian POVs |
| [voice-agent](.claude/agents/voice-agent.md) | Step 3 — extracts founder voice and creates replicable rules |

## Brain (Research, Audit, Architecture)

| Agent | Role |
|-------|------|
| [audience-question-miner-agent](.claude/agents/audience-question-miner-agent.md) | Finds real ICP questions across Reddit, Quora, forums |
| [competitor-analysis-agent](.claude/agents/competitor-analysis-agent.md) | Messaging analysis, content strategy breakdown, positioning gaps |
| [trend-scout-agent](.claude/agents/trend-scout-agent.md) | Cross-platform trend analysis (LinkedIn, YouTube, X, news, AI) |
| [idea-mining-agent](.claude/agents/idea-mining-agent.md) | Cross-format content ideation engine |
| [insight-capture-agent](.claude/agents/insight-capture-agent.md) | Step 4 — extracts atomic insights from transcripts/docs |
| [ai-content-architect-agent](.claude/agents/ai-content-architect-agent.md) | Plans AI-retrievable content architecture (7 AEO page types) |
| [ai-crawler-audit-agent](.claude/agents/ai-crawler-audit-agent.md) | Technical audit of AI crawler accessibility |
| [aeo-page-brief-agent](.claude/agents/aeo-page-brief-agent.md) | Citation-optimized briefs for 7 AEO page types |
| [entity-authority-agent](.claude/agents/entity-authority-agent.md) | Brand entity consistency + citation seeding plans |
| [gap-to-content-mapper-agent](.claude/agents/gap-to-content-mapper-agent.md) | Maps audit gaps to 90-day content plan |
| [content-refresh-agent](.claude/agents/content-refresh-agent.md) | Monitors published content for citation decay |
| [prospect-scorecard-agent](.claude/agents/prospect-scorecard-agent.md) | AI search visibility scorecard for prospect companies |

## Brand (Channel Content Production)

| Agent | Role |
|-------|------|
| [content-brief-agent](.claude/agents/content-brief-agent.md) | Step 5 — strategic content briefs from approved insights |
| [carousel-agent](.claude/agents/carousel-agent.md) | Visual carousel with slide copy + design direction |
| [email-agent](.claude/agents/email-agent.md) | Email/newsletter generation with subject line optimization |
| [hook-writer-agent](.claude/agents/hook-writer-agent.md) | 10 hook options for any topic |
| [case-study-agent](.claude/agents/case-study-agent.md) | Raw client results → structured case study |
| [newsletter-curator-agent](.claude/agents/newsletter-curator-agent.md) | Weekly industry link curation + takes |
| [youtube-strategy-agent](.claude/agents/youtube-strategy-agent.md) | Trend, competitor, ideation for YouTube |
| [youtube-script-agent](.claude/agents/youtube-script-agent.md) | Long-form, shorts, green-screen scripts optimized for retention |
| [youtube-seo-agent](.claude/agents/youtube-seo-agent.md) | YouTube metadata/SEO for discovery + CTR |
| [youtube-thumbnail-agent](.claude/agents/youtube-thumbnail-agent.md) | Thumbnail CTR psychology + A/B specs |
| [youtube-publish-agent](.claude/agents/youtube-publish-agent.md) | Descript transcript → publish package |

## Cross-stage (Review, Distribution, Tracking, Scoring, Plumbing)

| Agent | Role |
|-------|------|
| [brand-consistency-reviewer](.claude/agents/brand-consistency-reviewer.md) | Reviews content against client Brand Brain |
| [conversion-reviewer](.claude/agents/conversion-reviewer.md) | Reviews for pipeline effectiveness (CTA, ICP pain, social proof) |
| [distribution-orchestrator](.claude/agents/distribution-orchestrator.md) | Cross-channel scheduling, platform variants, Notion calendar |
| [strategy-planner](.claude/agents/strategy-planner.md) | Strategic planning for content workflows |
| [visibility-tracker-agent](.claude/agents/visibility-tracker-agent.md) | Step 8 — aggregates engagement, generates visibility reports |
| [icp-scorer-agent](.claude/agents/icp-scorer-agent.md) | Step 9 — lead scoring on ICP fit, role, intent stage |
| [execution-agent](.claude/agents/execution-agent.md) | Implementation specialist for approved plans (file ops, data) |
