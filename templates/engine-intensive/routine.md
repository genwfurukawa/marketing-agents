# Weekly routine (Day 3)

Runs once a week, for example Monday 6:00. It prepares the week and stops at APPROVE. It never publishes.

## The prompt

> 1. Run `call-mining` on any transcript in `inputs/calls/` added since the last run. Append new items to `inputs/mined.md`.
> 2. Re-rank the insight queue with `insight-scorer-lite`. Keep the top 3 as Insight Objects in `inputs/insights.md`.
> 3. Run `prompts/fan-out.md` for the top insight.
> 4. Run gate 1 (`bash scripts/grep-gate.sh <draft>`), then the `source-checker` and `voice-checker` agents on each draft.
> 5. Run the prompt tracker on `worksheets/questions-20.csv` (ChatGPT and Gemini, 3 runs). It is `tools/prompt-tracker/scripts/run.py` in the marketing-agents repo and needs your own API keys. Without keys, skip this step and ask 5 of the questions by hand once a week and append one ledger row per engine: `date,visibility,<engine>,,,,,<named or cited count>/<answers>,`.
> 6. Write `drafts/WEEK.md`: what's waiting for approval, what failed a gate and why, and the visibility change against last week.
>
> Do not set `approved: true` on anything. Do not run `scripts/publish.sh`.

## How to schedule it

**Option A: a Claude Code scheduled task** (research preview; needs this repo on GitHub). Create a task with the prompt above and a weekly cadence. Docs: https://code.claude.com/docs/en/web-scheduled-tasks

**Option B: cron or launchd on your own machine.** Headless mode logs the cost of each run:

```
0 6 * * 1 cd /path/to/your/repo && claude -p "$(sed -n '/^> /s/^> //p' routine.md)" --output-format json >> ledger/routine-runs.jsonl
```

Each run's JSON includes `total_cost_usd`. Add it to the ledger.
