# The Autonomy Ladder, scored

**44 of 46 agents in this repo are L1 or L2.** That is 96 percent
of the work still needing a human to decide or to ship.

Every vendor in this category implies L4. This is what a real production
system looks like when you score it honestly, one row at a time.

Regenerate this file yourself: `python3 scripts/score_autonomy.py > AUTONOMY.md`

## The distribution

| Level | Name | Count | Share |
|---|---|---|---|
| **L1** | Suggests | 23 | 50% |
| **L2** | Drafts | 21 | 46% |
| **L3** | Ships with approval | 1 | 2% |
| **L4** | Autonomous | 1 | 2% |

## What this means

Sensing automates first. Making follows. **Deciding stays longest.**
Value migrates to whoever sets the bounds, which is the honest answer to
what a marketer is worth once software does the work: they move up the ladder.

Note where the L1s cluster. The judgment half of CAPTURE and the whole of
APPROVE are almost entirely L1, and those are the two places that
determine whether the output is worth anything.

## Every agent, scored

### CAPTURE

| Agent | Level | Why |
|---|---|---|
| `aeo-engine-scan` | L4 | Runs one query bank across engines on a schedule, returns a presence map |
| `ai-content-architect-agent` | L1 | Proposes site architecture and internal linking plans |
| `ai-crawler-audit-agent` | L1 | Flags blocked bots and missing files. The fix is a separate step. |
| `audience-question-miner-agent` | L1 | Finds real buyer questions. Does not decide which to answer. |
| `cited-page-teardown` | L1 | Explains why a competitor page wins a citation. Changes nothing. |
| `competitor-analysis-agent` | L1 | Surfaces competitor positioning and gaps for a human to weigh |
| `gap-to-content-mapper-agent` | L1 | Maps gaps to content types and priorities for review |
| `icp-definition-agent` | L1 | Proposes an ICP for a human to confirm against real deals |
| `ideate-content-ideas` | L1 | Proposes and ranks ideas. A human picks. |
| `insight-capture-agent` | L2 | Drafts structured insight objects from raw source material |
| `insight-scorer` | L1 | Scores insights against a rubric. Ranking is not deciding. |
| `original-research-designer` | L1 | Designs a study. Running it is a human commitment. |
| `positioning-agent` | L1 | Drafts positioning options. Positioning is never auto-adopted. |
| `prospect-scorecard-agent` | L1 | Scores prospects. Who gets touched stays human. |
| `topic-deep-dive` | L1 | Researches a topic to inform a brief |
| `youtube-packaging-first` | L1 | Tests title and thumbnail concepts before production is committed |

### BUILD

| Agent | Level | Why |
|---|---|---|
| `aeo-injector` | L2 | Inserts missing structural elements into an existing draft |
| `aeo-page-generator` | L2 | Generates a page against a structural template |
| `blog-writer` | L2 | Produces a draft. Never publishes. |
| `carousel-agent` | L2 | Drafts carousel slides |
| `case-study-agent` | L2 | Drafts a case study from ledger entries and interviews |
| `content-refresh-agent` | L2 | Drafts updates to decaying content |
| `email-agent` | L2 | Drafts email. Sending is a separate, human act. |
| `hook-writer-agent` | L2 | Drafts opening lines for a human to choose between |
| `insight-object-builder` | L2 | Builds reusable insight objects from captured material |
| `linkedin-post-writer` | L2 | Produces a draft. Never publishes. |
| `schema-generator` | L2 | Generates structured data markup for review |
| `storyboard-builder` | L2 | Drafts a storyboard from a script |
| `youtube-script-agent` | L2 | Drafts a script |
| `youtube-thumbnail-agent` | L2 | Generates thumbnail options |

### APPROVE

| Agent | Level | Why |
|---|---|---|
| `aeo-checker` | L1 | Flags structural failures. A gate that auto-approves is not a gate. |
| `aeo-cross-model-reviewer` | L1 | Checks a draft against several models before it ships |
| `brand-consistency-reviewer` | L1 | Flags brand inconsistency across a set of artifacts |
| `conversion-reviewer` | L1 | Flags conversion weaknesses in a draft |
| `voice-validator` | L1 | Flags voice violations against BRAND.md |

### SHIP

| Agent | Level | Why |
|---|---|---|
| `ai-crawler-fix` | L2 | Produces robots.txt, sitemap and llms.txt fixes for a human to apply |
| `community-seeding` | L2 | Drafts community contributions. Posting them is human. |
| `entity-authority-agent` | L2 | Drafts entity and authority signals for external profiles |
| `knowledge-graph-builder` | L2 | Drafts entity submissions. Third party sites gate the publish. |
| `topical-authority-linker` | L2 | Proposes internal link changes as a diff |
| `youtube-publish-agent` | L3 | Publishes on approval. The human is a gate, not an editor. |
| `youtube-seo-agent` | L2 | Drafts titles, descriptions and tags |

### IMPROVE

| Agent | Level | Why |
|---|---|---|
| `compound` | L1 | Proposes how a lesson should change the system |
| `youtube-analytics-retro` | L1 | Reports what performed and proposes what it means |
| `youtube-competitor-research` | L1 | Reports competitor performance patterns |
| `youtube-idea-validation` | L1 | Validates an idea against observed demand |

