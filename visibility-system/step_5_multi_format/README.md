# Step 5: Multi-Format Engine

> **Question**: Can one insight reliably become many assets?

## Pipeline Position
- **Receives from**: Step 4 (Structured atoms + content briefs)
- **Produces for**: Step 6 (Draft content across all formats)
- **Agent**: `agents/format_execution.py` | `.claude/agents/content-brief-agent.md`
- **Schema**: `schemas/content_brief_input.json` -> `schemas/format_bundle_output.json`

## Purpose
Turn structured insights into content across all formats. One input produces LinkedIn, video, blog, and email without rewriting from scratch each time.

## Subfolders

| Folder | What Goes Here |
|--------|---------------|
| `briefs/` | Content briefs (input for generation) |
| `linkedin/` | LinkedIn posts (`drafts/`, `final/`) |
| `blogs/` | Blog posts (`drafts/`, `final/`) |
| `newsletters/` | Email newsletters |
| `carousels/` | Visual carousel content |
| `youtube/` | Video scripts and metadata |
| `podcasts/` | Podcast scripts and show notes |
| `threads/` | Twitter/X threads |

## Checklist
- [ ] One input produces LinkedIn, video, blog, and email
- [ ] Consistent structure across formats
- [ ] No rewriting from scratch each time

## Failure Signal
High effort, low output, team burnout. Repurposing chaos. Inconsistent quality.

## Output
Multi-format content ready for AEO optimization (Step 6) or direct publishing (Step 7).
