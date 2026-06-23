---
description: Generate a complete Brand Brain document for a client
argument-hint: <client-name> [--url <website>] [--samples <path>]
allowed-tools: Task, Read, Write, Glob, Grep, WebSearch, WebFetch
---

## Task

Generate a complete 12-section Brand Brain for a client. The Brand Brain teaches AI everything about a brand's identity, voice, audience, and style.

**Arguments:**
- `<client-name>`: Required. Client slug (e.g., `iterate-ai`)
- `--url <website>`: Optional. Brand website URL for research
- `--samples <path>`: Optional. Path to founder writing samples (LinkedIn posts, blogs)

## Process

### Step 1: Validate Client Workspace

Resolve the client root path from `clients_registry.json`, or default to `../{client_root}/`.

1. Check that `{client_root}/` exists
2. Check for existing Brand Brain at `{client_root}/03_insight_layer/brand_brain.md`
   - If found, ask user to confirm overwrite
3. Read client config from `{client_root}/00_admin/config.json`

### Step 2: Gather Existing Inputs

Pull from completed pipeline steps if available:

1. **Step 1 output** (ICP): Check `{client_root}/02_research/icp/icp_profile_*.json`
   - Populates: Section 03 (ICP), Section 04 (Competitors)
2. **Step 2 output** (Positioning): Check `{client_root}/03_insight_layer/pillars/positioning_framework_*.json`
   - Populates: Section 05 (Brand POV)
3. **Founder content**: Check `{client_root}/01_founder_capture/`
   - LinkedIn posts, transcripts, raw captures
   - Populates: Sections 06-08, 10 (voice, style, examples)
4. **Existing brand docs**: Check `{client_root}/00_admin/brand/`

### Step 3: Research (if --url provided)

1. WebFetch the brand's homepage, about page, product pages, and blog
2. WebSearch for the brand name + competitors, press mentions, reviews
3. Extract: brand identity, products, positioning, key messaging

### Step 4: Analyze Voice (if --samples provided)

1. Read all files at the samples path
2. Analyze for:
   - Opening patterns (how they start posts/articles)
   - Sentence length and rhythm
   - Vocabulary and jargon
   - Tone markers (formal/casual, serious/playful)
   - Structural patterns (lists, stories, data)
   - CTA style

### Step 5: Generate the Brand Brain

Generate all 12 sections following this template. Be specific, not generic. Use the brand's actual language. Mark gaps with "[NEEDS INPUT: description]". Always include the full 100+ banned words list across all 8 categories. Include reference examples with annotations.

Sections:
1. Brand Identity & Positioning
2. Products, Services & Solutions
3. Ideal Customer Profile (ICP)
4. Competitors & Differentiation
5. Brand Point of View
6. Author Persona
7. Voice & Tone
8. Writing Style Rules
9. Banned Words & Phrases
10. Reference Examples
11. CTAs & Conversion Language
12. Platform-Specific Guidelines

For any section that cannot be confidently populated, mark with `[NEEDS INPUT: description of what's needed]`.

### Step 6: Save the Unified Brand Brain

Save to: `{client_root}/03_insight_layer/brand_brain.md`

### Step 7: Extract to Step 3 Subfolders

Create the subfolder structure and extract sections:

```
{client_root}/03_insight_layer/
  voice_rules/
    voice_rules.md          <- Sections 07 + 08
    ctas.md                 <- Section 11
    platforms.md            <- Section 12
  brand_kit/
    brand_identity.md       <- Section 01
  context_library/
    products.md             <- Section 02
    icp.md                  <- Section 03
    competitors.md          <- Section 04
    pov.md                  <- Section 05
    author.md               <- Section 06
  good_examples/
    reference_examples.md   <- Section 10
  constraints/
    banned_words.md         <- Section 09
```

Each extracted file should include a header:
```markdown
<!-- Extracted from brand_brain.md Section XX — Do not edit directly. Edit brand_brain.md and re-extract. -->
```

### Step 8: Report

Output a summary:

```
## Brand Brain Complete

**Client**: {client-name}
**Saved to**: {client_root}/03_insight_layer/brand_brain.md

### Sources Used
- [x/o] Step 1 ICP output
- [x/o] Step 2 Positioning output
- [x/o] Website research
- [x/o] Founder content samples
- [x/o] Existing brand docs

### Section Status
| Section | Status | Source |
|---------|--------|--------|
| 01: Brand Identity | Complete/Needs Input | Research / Step 1 / Manual |
| 02: Products | ... | ... |
| ... | ... | ... |

### Extracted Files
- voice_rules/ (3 files)
- brand_kit/ (1 file)
- context_library/ (5 files)
- good_examples/ (1 file)
- constraints/ (1 file)

### Next Steps
1. Review sections marked [NEEDS INPUT]
2. Add founder writing samples to Section 10 (Reference Examples)
3. Run /sync-templates to push the template to other clients
4. When satisfied, run the voice-agent to generate voice_framework JSON
```

## Important Notes

- The Brand Brain is markdown (.md) for portability - it can be copy-pasted into Claude Projects
- The unified `brand_brain.md` is the source of truth; subfolders are derived extractions
- The voice-agent still produces `voice_framework_{run_id}.json` for structured agent consumption
- Mark ALL gaps with `[NEEDS INPUT: ...]` rather than inventing content
- Include the standard 40+ AI cliche banned words in Section 09 for every client
