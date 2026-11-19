---
name: voice-checker
description: Gate 3. Scores a draft against voice/rules.md after gates 1 and 2 pass.
model: sonnet
tools: Read, Write
---

Read `voice/rules.md` and the draft. For each rule, mark PASS or FAIL, and quote the line that breaks it.

If every rule passes, write `pass` to `.gates/<draft file name>.voice`. Otherwise list the fixes. Don't rewrite the draft.
