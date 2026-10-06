# Gate: Fabrication

**Fails when:** a number, company name, person's name, quote or outcome appears
in the draft that is not in the Brain.

This gate exists because the failure mode is invisible. A fabricated statistic
reads exactly like a real one. The writer's own model will not catch it,
because the model produced it and finds it plausible.

## Why a different model runs this

The builder rationalizes its own output. Running the check on the same model
family reproduces the same blind spot: inherited patterns, habitual phrasings
and plausible-but-wrong facts all survive. The cross-model pass is what catches
them.

If the builder ran on Opus, run the checker on Sonnet, and the reverse.

## What the checker extracts and verifies

| Shape | Example | Must appear in |
|---|---|---|
| Any digit-bearing claim | "42% of buyers", "3x", "in 2024" | the Brain |
| Named company | a competitor, a customer | `brain/CONTEXT.md` |
| Named person | a founder, an analyst | the Brain, with a source line |
| Quoted speech | anything in quotation marks | a transcript or proof file |
| Claimed outcome | "cut their CAC in half" | a proof file with the receipt |

Rounding counts as fabrication. "Nearly half" from a source that says 38% is a
fail. So is attributing an unattributed number to a named study.

## Output

Quote the offending text verbatim. A finding that paraphrases is not
actionable.

```
FABRICATION: FAIL
  text: "Buyers now run 4.7 searches before shortlisting"
  reason: no entry in the Brain contains this figure
  action: cut, or replace with a sourced figure
```

## Waiver

None.
