# aeo_audit: the reference implementation

Runs a bank of buyer questions against one AI answer engine and records who got
cited. One engine, one pass, standard library only. No dependencies to install.

## Run it

Fastest path, no query bank needed. It generates a starter bank and scores it:

```bash
export PERPLEXITY_API_KEY=...
python3 scripts/aeo_audit/aeo_audit.py audit \
    --company "Acme" --domain acme.com \
    --category "conversation intelligence" \
    --competitors "rival.com,other.com" \
    --output ./results
```

Once you have a real bank, score that instead:

```bash
export PERPLEXITY_API_KEY=...
python3 scripts/aeo_audit/aeo_audit.py batch \
    --input scripts/aeo_audit/sample-queries.csv \
    --domain acme.com \
    --company "Acme" \
    --competitors "rival.com,other.com" \
    --output ./results
```

The generated bank is a starting point, not a substitute for `build-query-bank`,
which mines questions buyers actually ask rather than permuting your category name.
`sample-queries.csv` is there so the command runs on a fresh clone.

## Engines

This build runs **perplexity**. Pass `--engines perplexity,chatgpt,claude,gemini`
and it runs what it supports and prints what it skipped, recording both in
`metrics-*.json` under `engines_run` and `engines_skipped`. It never silently
pretends to have queried an engine it cannot reach.

## What it writes

| File | Holds |
|---|---|
| `metrics-{slug}.json` | Every query scored, plus the aggregate |
| `raw-results-{slug}.json` | Full answer text and citations, so you can check the scoring |
| `audit-report-{slug}.md` | The readable summary |

## How a query is scored

| Score | Presence | Means |
|---|---|---|
| 3 | featured | Your domain is cited in the first third of the sources |
| 2 | cited | Your domain is among the sources |
| 1 | mentioned | Your brand appears in the prose, but nothing of yours is cited |
| 0 | absent | You are not in the answer |

The gap between 1 and 2 is the one that matters. Being named is not being cited,
and only the citation sends anyone to you.

Aggregates: **answer rate** (how often you appear at all), **share of voice** (your
mentions against named rivals), **source control rate** (citations you own against
citations you do not), and **average prominence** (where you land when cited).

## What this version does not do

Several engines in one pass, cross-engine merge, concurrency, sentiment analysis,
or decay tracking across runs. Those live in the version SuperMarketers runs.

It is enough to take a real baseline and re-run it, which is the part that matters.
A single run is a screenshot.

## Reading the output honestly

Report the **delta against your own baseline**, never an absolute score. Citation
share moves slowly, is not fully attributable, and no one can promise you a
ranking. Anyone who does is misrepresenting how these systems work.

A failed API call is recorded as `absent` rather than dropped, so a flaky run
reads as a worse score instead of a smaller sample. Check `raw-results` before
you trust a sudden drop.
