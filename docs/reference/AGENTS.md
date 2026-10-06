# Agents

All 24 client-agnostic agents, grouped by stage. Each agent is a role
definition Claude Code can spawn via the Agent tool. Files live in
`.claude/agents/` so Claude Code's auto-discovery works.

## Foundation (ICP, Positioning, Voice)

| Agent | Role |
|-------|------|
| [icp-definition-agent](.claude/agents/icp-definition-agent.md) | Step 1 — produces validated ICP profile |
| [positioning-agent](.claude/agents/positioning-agent.md) | Step 2 — develops differentiated positioning with contrarian POVs |

## Brain (Research, Audit, Architecture)

| Agent | Role |
|-------|------|
| [audience-question-miner-agent](.claude/agents/audience-question-miner-agent.md) | Finds real ICP questions across Reddit, Quora, forums |
| [competitor-analysis-agent](.claude/agents/competitor-analysis-agent.md) | Messaging analysis, content strategy breakdown, positioning gaps |
| [insight-capture-agent](.claude/agents/insight-capture-agent.md) | Step 4 — extracts atomic insights from transcripts/docs |
| [ai-content-architect-agent](.claude/agents/ai-content-architect-agent.md) | Plans AI-retrievable content architecture (14 AEO page types) |
| [ai-crawler-audit-agent](.claude/agents/ai-crawler-audit-agent.md) | Technical audit of AI crawler accessibility |
| [entity-authority-agent](.claude/agents/entity-authority-agent.md) | Brand entity consistency + citation seeding plans |
| [gap-to-content-mapper-agent](.claude/agents/gap-to-content-mapper-agent.md) | Maps audit gaps to 90-day content plan |
| [content-refresh-agent](.claude/agents/content-refresh-agent.md) | Monitors published content for citation decay |
| [prospect-scorecard-agent](.claude/agents/prospect-scorecard-agent.md) | AI search visibility scorecard for prospect companies |

## Brand (Channel Content Production)

| Agent | Role |
|-------|------|
| [carousel-agent](.claude/agents/carousel-agent.md) | Visual carousel with slide copy + design direction |
| [email-agent](.claude/agents/email-agent.md) | Email/newsletter generation with subject line optimization |
| [hook-writer-agent](.claude/agents/hook-writer-agent.md) | 10 hook options for any topic |
| [case-study-agent](.claude/agents/case-study-agent.md) | Raw client results → structured case study |
| [youtube-script-agent](.claude/agents/youtube-script-agent.md) | Long-form, shorts, green-screen scripts optimized for retention |
| [youtube-seo-agent](.claude/agents/youtube-seo-agent.md) | YouTube metadata/SEO for discovery + CTR |
| [youtube-thumbnail-agent](.claude/agents/youtube-thumbnail-agent.md) | Thumbnail CTR psychology + A/B specs |
| [youtube-publish-agent](.claude/agents/youtube-publish-agent.md) | Descript transcript → publish package |

## Cross-stage (Review, Tracking, Scoring)

| Agent | Role |
|-------|------|
| [aeo-cross-model-reviewer](.claude/agents/aeo-cross-model-reviewer.md) | Mandatory final gate on every AEO page — runs on a DIFFERENT model than the writer |
| [brand-consistency-reviewer](.claude/agents/brand-consistency-reviewer.md) | Reviews content against client Brand Brain |
| [conversion-reviewer](.claude/agents/conversion-reviewer.md) | Reviews for pipeline effectiveness (CTA, ICP pain, social proof) |
