# Gate: Source

**Fails when:** any factual claim in the draft lacks a resolvable Brain source.

## What counts as a claim

A sentence a reader could ask "how do you know that" about. Statistics, dated
events, competitor behaviour, customer outcomes, product capabilities, market
size, and anything phrased as "most teams", "buyers now", "the data shows".

Opinion, argument and analogy are not claims and need no source. The test is
whether the sentence asserts a fact about the world outside this document.

## What resolves

A source is a pointer into the Brain that exists on disk:
`brain/CONTEXT.md#<anchor>`, `brain/ICP.md#<anchor>`, or a proof file you added.

The gate resolves each one. A path that does not exist is a fail, not a
warning. A path that exists but does not contain the claim is also a fail.
"Sounds right" is not a resolution.

## Check order

1. Deterministic: every source named in the draft is a real path.
2. Model: the checker opens each one and confirms it supports the claim it is
   attached to.

Step 1 failing short-circuits. Do not spend a model pass on a broken path.

## Output

```
SOURCE: FAIL
  claim: "Teams using answer engines convert 3x faster"
  cited: brain/CONTEXT.md#conversion
  reason: anchor does not exist
```

## Waiver

None. A claim with no source is cut or marked `[NEEDS SOURCE]` and goes back to
BUILD. There is no path where an unsourced claim ships.
