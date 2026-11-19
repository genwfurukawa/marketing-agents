---
name: compound-lite
description: Turn a human edit or a revise decision into a one-rule lesson file in lessons/, so the writers don't repeat the mistake. Files-only version of the compound skill. Use after every revise.
---

1. Compare the draft before and after the human's edit, or read the revise reason. You write the lesson only; the human makes the edit. After any edit, the gates must be run again: their passes go stale.
2. Write one rule, in one sentence a writer can follow, with one before line and one after line.
3. Save it as `lessons/<short-slug>.md` with front matter `applies_to: linkedin | email | page | all` and `date:`.
4. If a lesson already says the same thing, add the example to it instead of creating a new file.
5. Update `lessons/README.md`: one line per lesson.

Writers read `lessons/` before drafting. Keep each lesson short enough to read in 10 seconds.
