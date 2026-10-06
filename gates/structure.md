# Gate: Structure

**Fails when:** the draft is not shaped for an answer engine to cite.

Voice and truth can both be right while the piece stays uncitable. This gate is
about form, and it has a rubric behind it:
`visibility-system/citability_score_rubric.md`, six sections, 0 to 100.

## What it checks

| Check | Fails when |
|---|---|
| Answer-first opening | The first paragraph sets up rather than answers |
| Definition block | The core term is never defined in a liftable sentence |
| Entity clarity | The subject appears only as a pronoun or "the platform" |
| Heading structure | Headings are clever rather than interrogative |
| Extractability | No passage stands alone as a correct answer out of context |
| Schema | Required structured data for the page type is absent |

## Enforced by

The `aeo-checker` skill scores the draft against the rubric. `aeo-injector`
fixes the mechanical gaps it finds. `schema-generator` handles the last row.

Channel matters. A LinkedIn post is not held to schema; an AEO page is. Read
the channel off the draft and apply the matching subset. A gate that demands
FAQ schema on a YouTube description is noise, and noisy gates get ignored.

## Output

```
STRUCTURE: FAIL
  check: answer-first opening
  text: "There's been a lot of talk lately about answer engines."
  reason: the opening does not answer the title question
  fix: lead with the one-sentence answer, move the setup below it
```

## Waiver

Waivable on a piece where citation is not the goal, such as an announcement or
a personal post. Record the reason. Do not waive on a page whose whole purpose
is to be cited.
