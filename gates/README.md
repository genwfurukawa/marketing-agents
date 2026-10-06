# The Gates (APPROVE, layer 1)

**A gate that auto-approves is not a gate.**

APPROVE is the stage nobody builds, and it is why AI content has a reputation
problem. Volume without gates is just more editing. That is the experience that
burned most marketing teams last year, and it is the objection every buyer
raises.

Every artifact passes all six before a human sees it. Any failure returns the
piece to BUILD with the specific reason attached. No silent passes.

| Gate | Checks | Fails when |
|---|---|---|
| [**Source**](source.md) | Every claim against the Brain | A claim has no source, or the cited file does not support it |
| [**Fabrication**](fabrication.md) | Numbers, names, quotes, outcomes | A metric is invented, rounded up, or unattributed |
| [**Voice**](voice.md) | The draft against `brain/BRAND.md` | Banned words, wrong register, invented phrasing |
| [**Structure**](structure.md) | Shape against how engines extract | No answer-first opening, no liftable definition, weak entity clarity |
| [**Fit**](fit.md) | The piece against `brain/ICP.md` | It was written for reach rather than for the buyer |
| [**Risk**](risk.md) | Legal, competitive, brand-sensitive claims | A named human needs to see it before it ships |

Each gate is one file in this directory. They are readable on purpose: the
point of making APPROVE its own stage is that you can see exactly where
judgment sits without reading any code.

## Two rules that hold across all six

**Maker is not checker.** The agent that wrote the draft never gates it, and
the gate pass runs on a different model family than the one that wrote it. A
model does not catch what it just rationalized as correct: inherited patterns,
habitual phrasing, and plausible-but-wrong facts all survive a same-model
review.

**Deterministic before model.** Anything a grep can catch (a banned phrase, an
em dash, a missing file path) is caught by a grep first, because a model asked
to spot a banned phrase will miss it some percentage of the time. The model
layer adds strictness. It never removes it.

## Why the Fit gate exists

It is the least obvious and the most valuable. Content designed for reach
performs and brings you nobody. Tool lists, trend takes and "10 prompts for
marketers" are the usual shape. If a piece would not make some readers think
*this is not for me*, it is probably not for anyone.

## Why Risk is a router, not a judge

A Risk failure does not mean the claim is wrong. It means a model is not the
right thing to decide it. The gate's only two outputs are "clear" and
"escalate to a named human".

## The rebuild limit

A rejection goes back to BUILD with the reason attached. Two rebuilds maximum.
The third failure stops and waits for a human instead of looping. A loop that
can retry forever will, and it will spend your tokens doing it.

## Reading the log

Every gate writes a pass or fail with its reason, quoting the offending text,
to the artifact's record. A finding that paraphrases instead of quoting is not
actionable. That log is what makes the system inspectable, which is the
difference between trusting output and checking it. Read it before you
approve, not after something goes wrong.
