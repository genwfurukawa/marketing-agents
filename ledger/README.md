# The Ledger

One page, every month. What shipped, what it replaced, what it produced, what is
next.

The Ledger is the fourth artifact, and the one that makes IMPROVE possible. Without
it, "the system is working" is a feeling. With it, it is a row you can point at.

## What goes in

| Column | Holds |
|---|---|
| `id`, `format`, `channel` | What it was and where it went |
| `shipped_at`, `url` | When, and the thing itself |
| `build_attempts`, `gate_failures` | How much work it took to clear APPROVE |
| `approval_decision`, `revise_note` | What the human said, and why |
| `impressions_7d`, `clicks_7d` | Reach, once measured |
| `engine_citations_30d` | Whether engines picked it up, once measured |
| `replies_or_leads` | The only column that pays for the others |

## Two rules

**Metrics stay blank until measured.** Never backfilled with an estimate. A blank
cell is information. A guessed cell is a lie you will later believe.

**A row means it shipped.** Not drafted, not approved. Shipped. The Ledger is not a
plan.

## What it is for

The gate and build columns are the ones people skip, and they are the ones that pay.
`gate_failures` tells you which gate is doing work and which has not caught anything
in months. `revise_note` tells you what the human keeps fixing by hand, and a note
that shows up three times is not a note, it is a missing gate or a missing voice
rule.

That is the feedback loop. IMPROVE reads this file and proposes a change to the
Brain, the Voice, or the Gates. The proposal goes through APPROVE like any other
output, because a system that can silently rewrite its own guardrails does not have
guardrails.
