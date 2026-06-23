# Step 6: AEO + Structure Optimization

> **Question**: Is your content designed for AI discovery?

## Pipeline Position
- **Receives from**: Step 5 (Draft content across all formats)
- **Produces for**: Step 7 (AEO-optimized content with definitions, FAQs, schema markup)
- **Agent**: `.claude/agents/aeo-optimizer-agent.md`
- **Schema**: `schemas/aeo_optimization_input.json` -> `schemas/aeo_optimization_output.json`

## Purpose
Structure content to be cited by AI search tools (ChatGPT, Claude, Perplexity). Uses definitions, steps, examples, and FAQs.

## Subfolders

| Folder | What Goes Here |
|--------|---------------|
| `aeo_audits/` | Audit results for existing content |
| `optimized_content/` | AEO-structured versions of content |
| `refresh_queue/` | Content that needs updating/refresh |
| `citation_tracking/` | Where our content is being cited by AI |

## Checklist
- [ ] Uses definitions, steps, examples, and FAQs
- [ ] Structured to be cited by AI search tools
- [ ] Regular refresh cycles on key content

## Failure Signal
Content performs briefly, then disappears. Content that performs today and disappears tomorrow.

## Output
AEO-optimized content library with monthly refresh logic.
