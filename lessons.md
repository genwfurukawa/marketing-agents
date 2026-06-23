# Lessons

Compounding methodology corrections. Read this before generating content — same
priority as the active client config. Add a rule after any correction:
`[date] **Problem:** [what]. **Rule:** [fix]. **Applies to:** [scope]`.

These are generic, de-identified methodology lessons. Client-specific lessons live in
each client's `clients/{slug}/lessons.md`.

## Voice & hooks

- **Problem:** Openings that explain before they hook lose the reader. **Rule:** The
  first line must earn the second. Lead with the insight or the specific moment, never
  setup or throat-clearing. **Applies to:** all content.
- **Problem:** AI-slop verbs and intensifiers make content sound generic and read as
  untrustworthy to both humans and AI engines. **Rule:** Ban leverage/seamless/robust/
  unlock/elevate and very/really/significantly. Plain, specific language. **Applies to:**
  all content.

## AEO structure

- **Problem:** Pages that read well but have no extractable passages don't get cited.
  **Rule:** Every AEO page needs a self-contained definition block in the first 300
  words, query-matched headings, and a 5+ Q&A FAQ. AI models extract passages, not
  pages. **Applies to:** all AEO pages.
- **Problem:** Claims without named sources get cited far less. **Rule:** Back claims
  with specific stats and named sources (+37% citation rate). Never "studies show".
  **Applies to:** all AEO content.
- **Problem:** Fabricated ratings/reviews in schema get pages penalized. **Rule:**
  Never invent aggregateRating, review counts, or customer results. **Applies to:**
  schema-generator, all pages.

## Process

- **Problem:** Generating before reading the client config produces off-voice,
  off-ICP content. **Rule:** Always read `config.yaml`, `voice-guide.md`, and
  `lessons.md` before generating. **Applies to:** every generation task.

---

Lesson count: 6
