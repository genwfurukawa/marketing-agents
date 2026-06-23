# Pipeline Flow: How Every Idea Becomes Pipeline

Every idea, keyword, and insight enters this system at Step 1 and exits at Step 9 as a pipeline signal. No exceptions. No shortcuts. This is a manufacturing line for B2B visibility.

---

## The Flow

```
IDEA / KEYWORD / RAW INSIGHT
         |
         v
  +-----------------+
  | STEP 1: ICP     |  Who cares about this? Does it match our buyer?
  +-----------------+
         |
         v
  +-----------------+
  | STEP 2: POV     |  What's our contrarian take? How is this different?
  +-----------------+
         |
         v
  +-----------------+
  | STEP 3: VOICE   |  Does this sound like us? Apply voice constraints.
  +-----------------+
         |
         v
  +---------------------+
  | STEP 5a: ARCHITECT  |  Map the 7 AEO page types for this client.
  +---------------------+  (Runs once - produces content architecture plan)
         |
         v
  +-----------------+
  | STEP 4: CAPTURE |  Extract the atomic insight. Quote, story, data point.
  +-----------------+
         |
         v
  +-----------------+       +------------------------+
  | STEP 5: CREATE  | ----> | STEP 5: AEO PAGES      |
  | (Founder Track) |       | (Architecture Track)   |
  | Atoms -> social |       | 7 page types for AI    |
  | blog, email,    |       | citation: What Is,     |
  | video, carousel |       | Best Tools, Alts, X vs |
  +-----------------+       | Y, Integration, Stats, |
         |                  | Glossary               |
         |                  +------------------------+
         |                           |
         v                           v
  +-----------------+
  | STEP 6: AEO     |  Structure for AI search. Definitions, FAQs, schema.
  +-----------------+  + Entity Authority (6b): brand descriptions, citation seeding
         |
         v
  +-----------------+
  | STEP 7: PUBLISH |  When, where, in what sequence. Narrative arcs.
  +-----------------+  + Citation seeding distribution (Reddit, G2, communities)
         |
         v
  +-----------------+
  | STEP 8: TRACK   |  What worked? Who engaged? AI citation monitoring.
  +-----------------+  + AI Crawler Audit (GPTBot, ClaudeBot, PerplexityBot access)
         |
         v
  +-----------------+
  | STEP 9: SCORE   |  Score engaged accounts. Surface pipeline signals.
  +-----------------+
         |
         v
  PIPELINE SIGNAL -> SALES CONVERSATION
```

---

## Three Phases

**Foundations (Steps 1-3)**: Run once per client. These are the constraints that keep everything consistent. Without them, you get generic content that could belong to any company.

**Architecture (Step 5a)**: Run once per client after foundations. Maps the 7 AEO page types to the client's category, competitors, and integrations. Produces a prioritized roadmap of citation-optimized pages to build. Use `/architect` to run.

**Engine (Steps 4-9)**: Run every month. Two parallel production tracks:
- **Founder Content Track**: 30 minutes of founder input -> 16+ LinkedIn posts, 4 long-form articles, email sequences, video scripts, carousel decks.
- **AEO Page Track**: Generate citation-optimized pages from the architecture plan using `/aeo-page`. 7 page types: What Is, Best Tools, Alternatives, Comparisons, Integrations, Statistics, Glossary.

---

## What Moves Between Steps

Each step produces a specific artifact that feeds the next step.

| Step | Receives | Produces | Agent |
|------|----------|----------|-------|
| 1. ICP + Category | Raw idea or keyword | ICP-validated topic with buyer context | `icp-definition-agent` |
| 2. Positioning + POV | ICP-validated topic | Opinionated angle with contrarian take | `positioning-agent` |
| 3. Voice + Narrative | Opinionated angle | Voice-constrained content seed | `voice-agent` |
| 5a. Architecture | ICP + positioning + competitors | Page type roadmap (which AEO pages to build) | `ai-content-architect-agent` |
| 4. Insight Capture | Founder raw material + voice rules | Structured atoms (quotes, stories, data) | `insight-capture-agent` |
| 5. Multi-Format | Atoms + content brief | LinkedIn, blog, email, video, carousel | `content-brief-agent` |
| 5. AEO Pages | Architecture plan + topic | Citation-optimized pages (7 types) | `aeo-page-brief-agent` |
| 6. AEO Optimize | Draft content (all formats) | AI-structured content (definitions, FAQs, schema markup) | `aeo-optimizer-agent` |
| 6b. Entity Authority | Positioning + brand brain | Entity descriptions, citation seeding plan | `entity-authority-agent` |
| 7. Publishing | AEO-optimized content | Scheduled calendar + citation seeding plan | Manual |
| 8. Visibility Track | Published content URLs | Engagement data, AI citations, crawler audit | `visibility-tracker-agent`, `ai-crawler-audit-agent` |
| 9. ICP Scoring | Engagement data + ICP profiles | Scored accounts, pipeline signals, follow-ups | `icp-scorer-agent` |

---

## What Makes This Different

**Traditional content marketing**: Idea -> Write -> Post -> Hope

**This system**: Idea -> Validate against ICP -> Apply POV -> Apply voice -> Extract atoms -> Generate 7+ formats -> Optimize for AI search -> Publish in sequence -> Track engagement -> Score for pipeline

Every piece of content is:
- Validated against a real buyer profile (Step 1)
- Differentiated with a strong point of view (Step 2)
- Consistent with founder voice (Step 3)
- Built from real insight, not blank-page creation (Step 4)
- Produced in every format from a single atom (Step 5)
- Structured so AI search engines cite it (Step 6)
- Published strategically, not randomly (Step 7)
- Measured for what matters (Step 8)
- Connected to pipeline, not vanity metrics (Step 9)

---

## The Math

One founder session (30 minutes) produces:
- 8-12 atomic insights
- Each atom generates: 2 LinkedIn posts + 1 blog section + 1 email + 1 video script + 1 carousel slide
- Net output: 16+ LinkedIn posts, 4 long-form articles, 8+ emails, video scripts, carousel decks
- All AEO-optimized for AI search discovery
- All tracked back to pipeline signals

System, not service. Infrastructure, not content.

---

## Feedback Loops

The pipeline is not strictly linear. Step 8 (Visibility Tracking) generates data that feeds back to refine the Foundations (Steps 1-3). The primary feedback target is the Brand Brain - the 12-section reference doc that lives at `{client_root}/03_insight_layer/brand_brain.md`.

### Step 8 -> Step 3 (Brand Brain Refinement)

| What Step 8 Reveals | What Gets Updated | Brand Brain Section |
|---------------------|-------------------|-------------------|
| High-performing hooks and formats | Opening patterns, structure templates | 08: Writing Style Rules |
| Top-performing content pieces | New reference examples added | 10: Reference Examples |
| Topic/pillar engagement rates | Content pillars reweighted | 05: Brand Point of View |
| Audience demographics from engagement | ICP validated or expanded | 03: ICP |
| Platform-specific performance data | Platform guidelines refined | 12: Platform Guidelines |
| CTA conversion rates | CTA patterns updated | 11: CTAs & Conversion |
| Voice consistency scores | Voice characteristics calibrated | 07: Voice & Tone |

### Step 8 -> Step 1 (ICP Refinement)

| What Step 8 Reveals | What Gets Updated |
|---------------------|-------------------|
| Which accounts engage most | ICP profile sharpened - new buying triggers, job titles |
| Which topics drive pipeline signals | Category map updated with validated demand |

### Cadence

- **Monthly**: Review top-performing content, add best pieces to Reference Examples (Section 10). Update opening patterns if new hooks outperform.
- **Quarterly**: Audit all Brand Brain sections against engagement data. Reweight content pillars. Validate ICP against actual engaged accounts.
- **Annual**: Full Brand Brain rebuild with fresh website research, new competitor analysis, and updated positioning.

### Status

Phase 1: Manual review. The founder or operator reviews Step 8 reports and updates the Brand Brain by hand. This is the current state.

Phase 2 (future): Semi-automated. Step 8 agent flags specific Brand Brain sections for update based on engagement thresholds. Human approves changes.

Phase 3 (future): Automated suggestions. System proposes Brand Brain edits with evidence from engagement data. Human reviews and accepts/rejects.
