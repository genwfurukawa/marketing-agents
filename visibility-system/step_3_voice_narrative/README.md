# Step 3: Voice + Narrative Rules

> **Question**: Can your content system scale without degrading?

## Pipeline Position
- **Receives from**: Step 2 (Opinionated angle with contrarian take)
- **Produces for**: Step 4 (Voice-constrained content seed and brand rules)
- **Agent**: `.claude/agents/voice-agent.md`
- **Schema**: `schemas/voice_rules_input.json` -> `schemas/voice_rules_output.json`

## Purpose
Document HOW you sound so AI and humans can maintain consistency at scale. This is REFERENCE MATERIAL, not content.

## Subfolders

| Folder | What Goes Here |
|--------|---------------|
| `voice_rules/` | Tone, style, sentence patterns, structural rules |
| `brand_kit/` | Visual + verbal identity, terminology |
| `context_library/` | Background info for AI prompts (company history, founder bio, product details) |
| `good_examples/` | Annotated examples of ideal content |
| `constraints/` | What NOT to do (banned phrases, off-limits topics) |

## Checklist
- [ ] Documented voice, tone, and structural rules
- [ ] Clear examples of what "good" looks like
- [ ] Clear constraints on what not to say or do
- [ ] Structural patterns defined

## Failure Signal
Inconsistent quality, AI content rot, founder says "this doesn't sound like me."

## Output
Brand kit and context library that agents and humans check before creating content.
