# Gate: Voice

**Fails when:** the draft breaks the documented voice rules in
`brain/BRAND.md`.

## Two layers, in order

**Layer 1, deterministic.** A grep pass over the draft for:

- em dashes and en dashes (banned; commas, periods and colons only)
- every banned word: seamless, powerful, cutting-edge, unlock, supercharge,
  leverage, AI-powered, revolutionize
- anything the user added to their own banned list

This layer is mechanical on purpose. A model asked to spot a banned phrase will
miss it some percentage of the time. Grep will not.

**Layer 2, model.** The `voice-validator` skill checks what grep cannot:
register, rhythm, attribution patterns, format compliance, and the documented
do/don't pairs in `brain/BRAND.md`.

Layer 1 failing short-circuits. Fix the mechanical violations before spending a
model pass on register.

## The rule behind the rule

Voice comes from the user's own best existing work, extracted by
`brain/capture/voice-extract.md`. It is never invented. A gate checking an
invented voice is theatre: it will pass drafts that sound like nobody, very
consistently.

## Output

```
VOICE: FAIL
  layer: 1 (deterministic)
  text: "This is a game-changer for teams"
  rule: banned phrase list
```

## Waiver

A voice fail can be waived by the human at APPROVE, with the reason recorded.
A rule waived three times is evidence the rule is wrong. Change the rule rather
than keep waiving it.
