#!/usr/bin/env python3
"""Regenerate the `## Index by category` section of lessons.md from the files in lessons/.

Deterministic: parses each learning's frontmatter (stdlib only, no PyYAML) and rewrites
the index + derived footer. Everything ABOVE the `## Index by category` marker (the protocol
prose) is preserved verbatim, so the index can never drift from the files again.

Run from the repo root:  python3 .claude/skills/compound/scripts/reindex.py
"""
import glob
import os
import re
import sys

MARKER = "## Index by category"

# Display order + one-line scope per category. New categories not listed here are
# appended alphabetically with a generic heading.
CATEGORIES = {
    "voice":             "tone, word choice, banned phrases, how Gen sounds",
    "hooks":             "opening lines and first impressions",
    "structure":         "post architecture and content shape",
    "aeo":               "structuring content for AI citation + factual accuracy",
    "html-site":         "visual rendering, accessibility, deploy/crawler config",
    "client-context":    "loading and respecting client-specific source material",
    "workflow":          "how the ops system runs, gates, repo hygiene",
    "youtube":           "competitor research, outlier scoring, packaging",
    "audit-positioning": "grounding competitive work in real data",
    "notion":            "master DBs, portals, schema mutations, data integrity",
    "cost-routing":      "which model runs where vs quality",
    "security":          "handling credentials on commit/push/move",
}

FOOTER = """
---

The lesson count is **derived, not hand-maintained**. To count: `find lessons -name '*.md' | wc -l`.
"""


def parse_frontmatter(path):
    """Return dict of frontmatter fields. Stdlib only; handles scalars and `[a, b]` lists."""
    txt = open(path, encoding="utf-8").read()
    if not txt.startswith("---"):
        return None
    fm = txt.split("---", 2)[1]
    out = {}
    for line in fm.splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            out[key] = [x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()] if inner else []
        else:
            # strip exactly one matching outer quote pair (a blanket strip of all quote
            # chars corrupts a title like `'... "I"'` - keep interior quotes intact)
            if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
                val = val[1:-1]
            out[key] = val
    return out


def main():
    repo = os.environ.get("REPO", os.getcwd())
    lessons_dir = os.path.join(repo, "lessons")
    index_path = os.path.join(repo, "lessons.md")
    if not os.path.isdir(lessons_dir):
        sys.exit(f"No lessons/ directory at {lessons_dir} - run from repo root.")
    if not os.path.isfile(index_path):
        sys.exit(f"No lessons.md at {index_path}.")

    by_cat = {}
    bad = []
    for p in sorted(glob.glob(os.path.join(lessons_dir, "**", "*.md"), recursive=True)):
        fm = parse_frontmatter(p)
        if not fm or "slug" not in fm or "category" not in fm:
            bad.append(p)
            continue
        by_cat.setdefault(fm["category"], []).append(fm)

    # category order: known first (in CATEGORIES order), then any new ones alphabetically
    ordered = [c for c in CATEGORIES if c in by_cat] + sorted(c for c in by_cat if c not in CATEGORIES)

    sections = [""]
    for cat in ordered:
        desc = CATEGORIES.get(cat, "")
        heading = f"### {cat}" + (f" ({desc})" if desc else "")
        sections.append("")
        sections.append(heading)
        sections.append("")
        for fm in sorted(by_cat[cat], key=lambda x: x.get("date", "")):
            slug = fm["slug"]
            title = fm.get("title", slug)
            applies = ", ".join(fm.get("applies_to", []) or [])
            sections.append(f"- [{slug}](lessons/{cat}/{slug}.md), {title} `[{applies}]`")
        sections.append("")

    head = open(index_path, encoding="utf-8").read().split(MARKER)[0] + MARKER + "\n"
    # No em dashes and no dash-hyphens in the store. We do not auto-substitute (a hyphen is also
    # banned now); the lint flags any that slip in for a manual comma/period fix.
    new_text = head + "\n".join(sections) + FOOTER
    open(index_path, "w", encoding="utf-8").write(new_text)

    total = sum(len(v) for v in by_cat.values())
    print(f"Reindexed {total} learnings across {len(ordered)} categories.")
    if bad:
        print("WARNING - files missing slug/category frontmatter (excluded):")
        for p in bad:
            print("  ", p)


if __name__ == "__main__":
    main()
