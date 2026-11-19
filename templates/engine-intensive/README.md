# Engine intensive template

The starter repo for the 3-day "Install your AI marketing engine" intensive. Fork it, fill it with your own company, and keep it.

It runs on files only: no Notion, no paid connectors. Tested with Claude Code on Nov 18, 2026. Re-test and update this line every cohort.

## Start here

```
make check          # setup: Claude Code, model access, the template's own tests
make check-brain    # every Brain line has a source, or sits under "needs a human"
make gate F=drafts/<file>.md   # gate 1, the deterministic check
```

## Folders

| Folder | What goes in it | Day |
|---|---|---|
| `inputs/` | Your call transcripts, your 10 best pieces of writing, `site.txt` | Pre-work |
| `brain/` | `CONTEXT.md`, `ICP.md`, `BRAND.md`. Every fact ends with `source:` | 1 |
| `voice/` | `banned.txt` (grep tests) and `rules.md` (what the voice checker scores) | 1 |
| `drafts/` | Writer output, with front matter `approved: false` until you approve | 2 |
| `.gates/` | Pass marks written by each gate. The publish hook reads them | 2 |
| `lessons/` | One rule per file, written from your edits. Writers read them first | 3 |
| `ledger/` | `ledger.csv`: what shipped, the time and cost it took, and whether AI answers name you | 1, 3 |
| `prompts/` | `fan-out.md`, `engine-guide.md`, `redact.md` | 2, 3 |
| `worksheets/` | The Autonomy Ladder and your 20 buyer questions | Pre-work |

`routine.md` is the weekly run. `.claude/settings.json` holds the publish hook, which works inside Claude Code. Outside it, `scripts/publish.sh` runs the same check itself, so nothing ships ungated either way. A gate pass goes stale if the draft is edited afterward: run the gates again.

`docs/capture/` holds the full methods for call mining, voice extraction, review mining and the founder interview.

The example content in `brain/` and `inputs/` is for a fictional company, Acme Analytics (from `clients/acme-analytics/` in this repo). Replace it with your own.
