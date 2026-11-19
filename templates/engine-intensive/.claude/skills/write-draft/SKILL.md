---
name: write-draft
description: Write one draft (linkedin, email or page) from one Insight Object, using only facts in brain/. The files-only writer for the course template. Fuller channel writers are in the marketing-agents repo (linkedin-post-writer, email-agent, aeo-page-generator).
---

Before writing, read `brain/`, `voice/rules.md`, `voice/banned.txt` and every file in `lessons/`.

Then write the draft for the channel you're given:

- **linkedin:** a hook line that states the specific thing, then 120 to 220 words, then one question at the end.
- **email:** a subject under 50 characters and a body under 150 words, with one call to action.
- **page:** the buyer question word for word as the H1, the answer in the first 60 words, then a short table or list and a FAQ. One real number with its source, in plain HTML or markdown, never loaded by a script.

Rules:

- Every factual claim ends with `src:<id>` from the Brain. If the Brain doesn't have it, write `[NEEDS SOURCE]`, never a guess.
- Use the buyer's phrases from `brain/ICP.md` ("The buyer's words") where they fit.
- Save the draft to `drafts/<date>-<channel>.md` with front matter `approved: false`.
