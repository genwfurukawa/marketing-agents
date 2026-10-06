# Gate: Fit

**Fails when:** the piece serves reach rather than the buyer in `brain/ICP.md`.

This is the least obvious gate and the most valuable one. Content designed for
reach performs and brings nobody. Tool lists, trend takes and "10 prompts for
marketers" are the usual shape.

**The test:** if the piece would not make some readers think *this is not for
me*, it is probably not for anyone.

## What it checks

1. **ICP match.** Does this address the buyer in `brain/ICP.md`, or a generic
   audience?
2. **Brief intent.** Does it serve the stated goal of the queue item it came
   from? A draft that drifted off its own brief fails here even if it is good.
3. **Truth alignment.** Is it consistent with `brain/CONTEXT.md`, or does it
   quietly assert a position the company does not hold?
4. **Pipeline logic.** Is there a plausible line from reading this to a
   conversation? Not a CTA. A reason.

## Output

```
FIT: FAIL
  check: ICP match
  reason: written for marketers in general; the ICP is founders who have
          already tried an agency and been burned
  evidence: no passage addresses the prior-agency objection
```

## Waiver

Waivable for a deliberate top-of-funnel piece. Waiving is a strategy decision,
so record the reason, then check the Ledger later to see whether those pieces
actually produced anything. Usually they do not, which is the point of the
gate.
