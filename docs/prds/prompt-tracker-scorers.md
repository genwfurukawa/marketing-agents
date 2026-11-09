# Prompt tracker scorers: stacked draft

Status: implementation plan. Depends on the collection, sources and inventory PR.
No scoring code or paid model runs are included in this draft yet.

## Outcome

Turn collected answers into suggested company and competitor labels, with evidence
that the operator can review in the existing Answer evidence workflow.

Source URL extraction remains deterministic and separate from scoring. This change
does not crawl sites or regenerate answers.

## First scope

- Identify subject and tracked-competitor mentions.
- Identify recommendations, keeping a mention distinct from a recommendation.
- For comparison prompts, distinguish a single overall winner, a conditional or
  balanced comparison, and an answer that does not compare the products.
- Retain supporting passages and the scorer/provider/model version for each
  decision. An invalid or unsupported judgment is a hold, not a negative score.
- Map approved labels into the existing mentioned, recommended and recommended
  brands fields. Preserve the human-review flag and manual editing path.

Claims, factual accuracy, vocabulary, feature-level assessment authoring and
playbook generation are outside this first scorer port.

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

## Stack

The scorer branch is based on `feat/site-inventory`, the head of upstream PR #1.
Its draft PR is opened inside the fork against that branch so reviewers see only
the scorer work. GitHub cannot use a fork-only branch as the base of a PR inside
the upstream repository. Once PR #1 merges upstream, rebase this branch onto the
updated upstream main and open the scorer PR there.
