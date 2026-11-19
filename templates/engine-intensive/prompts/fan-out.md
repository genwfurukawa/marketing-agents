# Fan-out: one insight, three channels (Day 2)

Paste into Claude Code, replacing the brackets:

> Read `brain/`, `voice/rules.md` and every file in `lessons/`. Take Insight Object [N] from `inputs/insights.md`. In parallel, as three subagents:
> 1. `write-draft` (linkedin), or `linkedin-post-writer` from the marketing-agents repo: one LinkedIn post
> 2. `write-draft` (email), or `email-agent`: one email to [audience]
> 3. `write-draft` (page), or `aeo-page-generator` or `content-refresh-agent` on [URL]: one page that answers [buyer question], word for word
>
> Rules for all three:
> - Every claim carries `src:<brain id>`, or `[NEEDS SOURCE]` if the Brain doesn't have it.
> - Invent no numbers, names or quotes.
> - Save each as `drafts/<date>-<channel>.md` with front matter `approved: false`.

For the page, use the Lesson 1 checklist:
- the answer in the first paragraph
- the buyer's exact phrase in the title and H1
- one real number with its source, in static HTML
