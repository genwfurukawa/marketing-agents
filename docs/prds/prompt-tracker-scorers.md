# Prompt tracker scorers: stacked draft

Status: implemented draft. Depends on the collection, sources and inventory PR.
Provider contracts are fixture-tested; no paid scoring calls have been made.

## Outcome

Turn collected answers into suggested company and competitor labels, with evidence
that the operator can review in the existing Answer evidence workflow.

Source URL extraction remains deterministic and separate from scoring. This change
does not crawl sites or regenerate answers.

## First scope

- Score captured Comparison answers only; Discovery and Accuracy answers are untouched.
- Use explicit subject/product names for basic mention detection.
- Identify a single overall recommendation within the configured pair, keeping a
  mention, a conditional comparison and a recommendation distinct.
- For comparison prompts, distinguish a single overall winner, a conditional or
  balanced comparison, and an answer that does not compare the products.
- Retain supporting passages and the scorer/provider/model version for each
  decision. An invalid or unsupported judgment is a hold, not a negative score.
- Map approved labels into the existing mentioned, recommended and recommended
  brands fields. Preserve the human-review flag and manual editing path.

Short subject/competitor assessments and exact supporting passages accompany the
three S7 decisions. Claims, factual accuracy, vocabulary, feature-roster scoring,
per-table-row judgments and playbook generation remain outside this first port.

## Provider split

- **Jev through TypeSafe:** bounded choices from a supplied company roster and
  outcome vocabulary. Start from the existing KnitKnot decision contracts.
- **OpenAI:** structured extraction/evidence work needed by those contracts.
  Do not add a second model call where a deterministic check is sufficient.
- Use `TYPESAFE_API_KEY` and `OPENAI_API_KEY` from the local environment. Explicit
  model configuration is required; never substitute a different scoring provider
  silently. Model/account access must be verified separately from fixture tests.

This is Jev, not Gemini. Collection engine and scoring provider are independent:
an answer collected from any supported engine can use the same scorer contract.

## Integration boundaries

- Consume successful captures from PR #1, preserving exact prompt versions,
  source URLs, collection method, answer text and client project identity.
- Keep scores separate from immutable raw captures. Rescoring must not overwrite
  manual corrections or marks of human review.
- Include answer content, roster, scorer contract version and model configuration
  in scoring identity. Reuse completed results only when that identity matches.
- Keep errors, holds and unreviewed suggestions out of reviewed recommendation
  denominators. Do not manufacture zeroes for missing judgments.
- Reuse the existing local runner's bounded execution where appropriate. No
  hosted worker, queue service, scheduler or extra database is required.

## Acceptance checks

- Fixture tests exercise valid and malformed Jev/OpenAI responses without paid
  calls. Preserve explicit holds, provider failures and incomplete responses.
- Cover an unconditional pick, conditional recommendations, balanced tradeoffs,
  multiple recommended vendors, off-roster picks and answers with no comparison.
- Bind supporting passages to the actual answer with one canonical quote matcher;
  cover Unicode, case/whitespace variants and negative mismatches.
- Include more than one industry and company shape. No customer-specific rules.
- Verify client isolation, resume identity, import compatibility, manual review
  preservation and existing metric denominators at the backend boundary.
- Run the existing npm tests and build. Live scoring requires a separately bounded
  run with an explicit request cap; fixtures do not establish model quality.

## Operator flow

Collect and import answers using PR #1. Copy the example scorer config, map each
Comparison prompt ID to a tracked competitor, and configure the available OpenAI
model. Run `scripts/score.py` with `--dry-run`, then run the bounded scoring command.
The CLI attaches suggestions to the current local workspace without changing
manual labels or review status. Refresh the dashboard, open an answer, inspect
the supporting passages and use or correct the suggested labels. Confirm review
through the existing Edit capture form before results enter win-rate metrics.

The Overview reports per-competitor and weekly UTC results using the canonical
`wins / (wins + losses + ties)` denominator. Unreviewed, unscored, held and
not-compared answers do not count as decided comparisons.

## Stack

The scorer branch is based on `feat/site-inventory`, the head of upstream PR #1.
Its draft PR is opened inside the fork against that branch so reviewers see only
the scorer work. GitHub cannot use a fork-only branch as the base of a PR inside
the upstream repository. Once PR #1 merges upstream, rebase this branch onto the
updated upstream main and open the scorer PR there.
