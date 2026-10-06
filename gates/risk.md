# Gate: Risk

**Fails when:** the draft makes a legal, competitive or brand-sensitive claim
that a named human must see before it ships.

This gate does not judge. It routes. A fail here does not mean the claim is
wrong. It means a model is not the right thing to decide it.

## Triggers

| Category | Examples |
|---|---|
| **Legal** | Compliance claims, regulatory assertions, guarantees |
| **Competitive** | A named competitor, a comparison table, "unlike X" |
| **Customer** | A named customer, their numbers, an implied endorsement |
| **Financial** | Pricing, ROI promises, revenue claims, funding |
| **Personnel** | A named individual outside the company's leadership |
| **Prediction** | A dated forecast stated as fact |

## Behaviour

A trigger sends the piece to a human with the category named and the passage
quoted. It never auto-passes and it never auto-rejects. Internal-only work that
trips this gate waits for a human too.

## Output

```
RISK: ESCALATE
  category: competitive
  text: "Unlike Clearscope, we do not resell your data."
  reason: named competitor plus an implied claim about their practices
  needs: a human to confirm the claim is defensible
```

## Waiver

Not applicable. The only two outputs are "clear" and "escalate". The human it
escalates to is the waiver.
