# The map

Every agent in this repo, by loop and by stage, with the path to the file.

The directories `brain/`, `loops/`, `gates/` and `ports/` explain the system.
The agents themselves live in `.claude/`, because that is where Claude Code
looks for them. This file connects the two.

Levels are from the Autonomy Ladder. See [`AUTONOMY.md`](AUTONOMY.md).

## `sm-content`  (16 agents)

**CAPTURE**

| Agent | Level | Path |
|---|---|---|
| `ideate-content-ideas` | L1 | [`.claude/skills/ideate-content-ideas/SKILL.md`](.claude/skills/ideate-content-ideas/SKILL.md) |
| `insight-capture-agent` | L2 | [`.claude/agents/insight-capture-agent.md`](.claude/agents/insight-capture-agent.md) |
| `insight-scorer` | L1 | [`.claude/skills/insight-scorer/SKILL.md`](.claude/skills/insight-scorer/SKILL.md) |
| `original-research-designer` | L1 | [`.claude/skills/original-research-designer/SKILL.md`](.claude/skills/original-research-designer/SKILL.md) |
| `topic-deep-dive` | L1 | [`.claude/skills/topic-deep-dive/SKILL.md`](.claude/skills/topic-deep-dive/SKILL.md) |

**BUILD**

| Agent | Level | Path |
|---|---|---|
| `blog-writer` | L2 | [`.claude/skills/blog-writer/SKILL.md`](.claude/skills/blog-writer/SKILL.md) |
| `case-study-agent` | L2 | [`.claude/agents/case-study-agent.md`](.claude/agents/case-study-agent.md) |
| `content-refresh-agent` | L2 | [`.claude/agents/content-refresh-agent.md`](.claude/agents/content-refresh-agent.md) |
| `email-agent` | L2 | [`.claude/agents/email-agent.md`](.claude/agents/email-agent.md) |
| `hook-writer-agent` | L2 | [`.claude/agents/hook-writer-agent.md`](.claude/agents/hook-writer-agent.md) |
| `insight-object-builder` | L2 | [`.claude/skills/insight-object-builder/SKILL.md`](.claude/skills/insight-object-builder/SKILL.md) |
| `storyboard-builder` | L2 | [`.claude/skills/storyboard-builder/SKILL.md`](.claude/skills/storyboard-builder/SKILL.md) |

**APPROVE**

| Agent | Level | Path |
|---|---|---|
| `brand-consistency-reviewer` | L1 | [`.claude/agents/brand-consistency-reviewer.md`](.claude/agents/brand-consistency-reviewer.md) |
| `conversion-reviewer` | L1 | [`.claude/agents/conversion-reviewer.md`](.claude/agents/conversion-reviewer.md) |
| `voice-validator` | L1 | [`.claude/skills/voice-validator/SKILL.md`](.claude/skills/voice-validator/SKILL.md) |

**IMPROVE**

| Agent | Level | Path |
|---|---|---|
| `compound` | L1 | [`.claude/skills/compound/SKILL.md`](.claude/skills/compound/SKILL.md) |

## `sm-aeo`  (15 agents)

**CAPTURE**

| Agent | Level | Path |
|---|---|---|
| `aeo-engine-scan` | L4 | [`.claude/skills/aeo-engine-scan/SKILL.md`](.claude/skills/aeo-engine-scan/SKILL.md) |
| `ai-content-architect-agent` | L1 | [`.claude/agents/ai-content-architect-agent.md`](.claude/agents/ai-content-architect-agent.md) |
| `ai-crawler-audit-agent` | L1 | [`.claude/agents/ai-crawler-audit-agent.md`](.claude/agents/ai-crawler-audit-agent.md) |
| `cited-page-teardown` | L1 | [`.claude/skills/cited-page-teardown/SKILL.md`](.claude/skills/cited-page-teardown/SKILL.md) |
| `gap-to-content-mapper-agent` | L1 | [`.claude/agents/gap-to-content-mapper-agent.md`](.claude/agents/gap-to-content-mapper-agent.md) |

**BUILD**

| Agent | Level | Path |
|---|---|---|
| `aeo-injector` | L2 | [`.claude/skills/aeo-injector/SKILL.md`](.claude/skills/aeo-injector/SKILL.md) |
| `aeo-page-generator` | L2 | [`.claude/skills/aeo-page-generator/SKILL.md`](.claude/skills/aeo-page-generator/SKILL.md) |
| `schema-generator` | L2 | [`.claude/skills/schema-generator/SKILL.md`](.claude/skills/schema-generator/SKILL.md) |

**APPROVE**

| Agent | Level | Path |
|---|---|---|
| `aeo-checker` | L1 | [`.claude/skills/aeo-checker/SKILL.md`](.claude/skills/aeo-checker/SKILL.md) |
| `aeo-cross-model-reviewer` | L1 | [`.claude/agents/aeo-cross-model-reviewer.md`](.claude/agents/aeo-cross-model-reviewer.md) |

**SHIP**

| Agent | Level | Path |
|---|---|---|
| `ai-crawler-fix` | L2 | [`.claude/skills/ai-crawler-fix/SKILL.md`](.claude/skills/ai-crawler-fix/SKILL.md) |
| `community-seeding` | L2 | [`.claude/skills/community-seeding/SKILL.md`](.claude/skills/community-seeding/SKILL.md) |
| `entity-authority-agent` | L2 | [`.claude/agents/entity-authority-agent.md`](.claude/agents/entity-authority-agent.md) |
| `knowledge-graph-builder` | L2 | [`.claude/skills/knowledge-graph-builder/SKILL.md`](.claude/skills/knowledge-graph-builder/SKILL.md) |
| `topical-authority-linker` | L2 | [`.claude/skills/topical-authority-linker/SKILL.md`](.claude/skills/topical-authority-linker/SKILL.md) |

## `sm-social`  (10 agents)

**CAPTURE**

| Agent | Level | Path |
|---|---|---|
| `youtube-packaging-first` | L1 | [`.claude/skills/youtube-packaging-first/SKILL.md`](.claude/skills/youtube-packaging-first/SKILL.md) |

**BUILD**

| Agent | Level | Path |
|---|---|---|
| `carousel-agent` | L2 | [`.claude/agents/carousel-agent.md`](.claude/agents/carousel-agent.md) |
| `linkedin-post-writer` | L2 | [`.claude/skills/linkedin-post-writer/SKILL.md`](.claude/skills/linkedin-post-writer/SKILL.md) |
| `youtube-script-agent` | L2 | [`.claude/agents/youtube-script-agent.md`](.claude/agents/youtube-script-agent.md) |
| `youtube-thumbnail-agent` | L2 | [`.claude/agents/youtube-thumbnail-agent.md`](.claude/agents/youtube-thumbnail-agent.md) |

**SHIP**

| Agent | Level | Path |
|---|---|---|
| `youtube-publish-agent` | L3 | [`.claude/agents/youtube-publish-agent.md`](.claude/agents/youtube-publish-agent.md) |
| `youtube-seo-agent` | L2 | [`.claude/agents/youtube-seo-agent.md`](.claude/agents/youtube-seo-agent.md) |

**IMPROVE**

| Agent | Level | Path |
|---|---|---|
| `youtube-analytics-retro` | L1 | [`.claude/skills/youtube-analytics-retro/SKILL.md`](.claude/skills/youtube-analytics-retro/SKILL.md) |
| `youtube-competitor-research` | L1 | [`.claude/skills/youtube-competitor-research/SKILL.md`](.claude/skills/youtube-competitor-research/SKILL.md) |
| `youtube-idea-validation` | L1 | [`.claude/skills/youtube-idea-validation/SKILL.md`](.claude/skills/youtube-idea-validation/SKILL.md) |

## `sm-demand`  (5 agents)

**CAPTURE**

| Agent | Level | Path |
|---|---|---|
| `audience-question-miner-agent` | L1 | [`.claude/agents/audience-question-miner-agent.md`](.claude/agents/audience-question-miner-agent.md) |
| `competitor-analysis-agent` | L1 | [`.claude/agents/competitor-analysis-agent.md`](.claude/agents/competitor-analysis-agent.md) |
| `icp-definition-agent` | L1 | [`.claude/agents/icp-definition-agent.md`](.claude/agents/icp-definition-agent.md) |
| `positioning-agent` | L1 | [`.claude/agents/positioning-agent.md`](.claude/agents/positioning-agent.md) |
| `prospect-scorecard-agent` | L1 | [`.claude/agents/prospect-scorecard-agent.md`](.claude/agents/prospect-scorecard-agent.md) |

