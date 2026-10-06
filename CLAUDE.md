# Marketing Agents

The open subset of the SuperMarketers system. Read this before running anything.

## The loop

```
CAPTURE -> BUILD -> APPROVE -> SHIP -> IMPROVE
```

Five stages, one shared Brain. Four artifacts carry state: Brain (`brain/`),
Voice (`brain/BRAND.md`), Gates (`gates/`), Ledger (`ledger/`).

## The order of operations

1. **Brain first.** `brain/CONTEXT.md`, `brain/BRAND.md`, `brain/ICP.md`.
   Nothing downstream is better than these three files. If a user asks you to
   generate content before they exist, build them first and say why.
2. **Then a loop.** `loops/sm-content`, `sm-aeo`, `sm-social`, `sm-demand`.
   Each runs the same five stages on its own clock.
3. **Always through the gates.** Nothing reaches a human without passing
   `gates/`. A gate that auto-approves is not a gate.
4. **Maker is not checker.** The agent that wrote a draft never gates it. Run
   the gate pass on a different model family than the one that wrote it. A
   model does not catch what it just rationalized.
5. **Record it.** Append to `ledger/LEDGER.md`: what shipped, hours it would
   have taken versus what it took, what it produced.

## Rules

- Never fabricate a metric. Measured or absent.
- Every claim gets matched to evidence in the Brain, or it does not ship.
- The subject of every sentence is the reader or their business, never the tool.
- Voice comes from `brain/BRAND.md`, extracted from the user's own best work.
  Never invent a voice.
- Banned: seamless, powerful, cutting-edge, unlock, supercharge, leverage,
  AI-powered, revolutionize.
- No em dashes. Commas, periods and colons only. If you reach for one, split
  the sentence.
- Tag every agent you add with its Autonomy Ladder level (L1 to L4) and its
  stage (CAPTURE, BUILD, APPROVE, SHIP, IMPROVE). Untagged agents do not get
  merged.

## What this repo does not do

No orchestration. No scheduler. No scraper. If a task needs one, say so plainly
rather than improvising a workaround.
