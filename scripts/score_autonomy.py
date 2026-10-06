#!/usr/bin/env python3
"""Score every agent in this repo on the Autonomy Ladder and emit AUTONOMY.md.

The point of this file is that you can check the claim rather than take our word
for it. Change a rating, re-run, and the table and the headline number move.

Usage:  python3 scripts/score_autonomy.py > AUTONOMY.md
"""

# unit -> (Engine stage, autonomy level, one-line justification)
# Stages are the five in the Engine loop: CAPTURE BUILD APPROVE SHIP IMPROVE.
# L1 Suggests | L2 Drafts | L3 Ships with approval | L4 Autonomous
SCORES = {
    # CAPTURE
    "aeo-engine-scan":             ("CAPTURE",    4, "Runs one query bank across engines on a schedule, returns a presence map"),
    "cited-page-teardown":         ("CAPTURE",    1, "Explains why a competitor page wins a citation. Changes nothing."),
    "competitor-analysis-agent":   ("CAPTURE",    1, "Surfaces competitor positioning and gaps for a human to weigh"),
    "audience-question-miner-agent":("CAPTURE",   1, "Finds real buyer questions. Does not decide which to answer."),
    "ai-crawler-audit-agent":      ("CAPTURE",    1, "Flags blocked bots and missing files. The fix is a separate step."),
    "insight-capture-agent":       ("CAPTURE",    2, "Drafts structured insight objects from raw source material"),
    # CAPTURE
    "ideate-content-ideas":        ("CAPTURE",  1, "Proposes and ranks ideas. A human picks."),
    "insight-scorer":              ("CAPTURE",  1, "Scores insights against a rubric. Ranking is not deciding."),
    "gap-to-content-mapper-agent": ("CAPTURE",  1, "Maps gaps to content types and priorities for review"),
    "topic-deep-dive":             ("CAPTURE",  1, "Researches a topic to inform a brief"),
    "original-research-designer":  ("CAPTURE",  1, "Designs a study. Running it is a human commitment."),
    "prospect-scorecard-agent":    ("CAPTURE",  1, "Scores prospects. Who gets touched stays human."),
    "ai-content-architect-agent":  ("CAPTURE",  1, "Proposes site architecture and internal linking plans"),
    "positioning-agent":           ("CAPTURE",  1, "Drafts positioning options. Positioning is never auto-adopted."),
    "icp-definition-agent":        ("CAPTURE",  1, "Proposes an ICP for a human to confirm against real deals"),
    "youtube-packaging-first":     ("CAPTURE",  1, "Tests title and thumbnail concepts before production is committed"),
    # BUILD
    "blog-writer":                 ("BUILD",  2, "Produces a draft. Never publishes."),
    "linkedin-post-writer":        ("BUILD",  2, "Produces a draft. Never publishes."),
    "aeo-page-generator":          ("BUILD",  2, "Generates a page against a structural template"),
    "aeo-injector":                ("BUILD",  2, "Inserts missing structural elements into an existing draft"),
    "schema-generator":            ("BUILD",  2, "Generates structured data markup for review"),
    "storyboard-builder":          ("BUILD",  2, "Drafts a storyboard from a script"),
    "carousel-agent":              ("BUILD",  2, "Drafts carousel slides"),
    "case-study-agent":            ("BUILD",  2, "Drafts a case study from ledger entries and interviews"),
    "email-agent":                 ("BUILD",  2, "Drafts email. Sending is a separate, human act."),
    "hook-writer-agent":           ("BUILD",  2, "Drafts opening lines for a human to choose between"),
    "youtube-script-agent":        ("BUILD",  2, "Drafts a script"),
    "youtube-thumbnail-agent":     ("BUILD",  2, "Generates thumbnail options"),
    "insight-object-builder":      ("BUILD",  2, "Builds reusable insight objects from captured material"),
    "content-refresh-agent":       ("BUILD",  2, "Drafts updates to decaying content"),
    # APPROVE
    "aeo-checker":                 ("APPROVE",  1, "Flags structural failures. A gate that auto-approves is not a gate."),
    "voice-validator":             ("APPROVE",  1, "Flags voice violations against BRAND.md"),
    "brand-consistency-reviewer":  ("APPROVE",  1, "Flags brand inconsistency across a set of artifacts"),
    "conversion-reviewer":         ("APPROVE",  1, "Flags conversion weaknesses in a draft"),
    "aeo-cross-model-reviewer":    ("APPROVE",  1, "Checks a draft against several models before it ships"),
    # SHIP
    "ai-crawler-fix":              ("SHIP",    2, "Produces robots.txt, sitemap and llms.txt fixes for a human to apply"),
    "topical-authority-linker":    ("SHIP",    2, "Proposes internal link changes as a diff"),
    "knowledge-graph-builder":     ("SHIP",    2, "Drafts entity submissions. Third party sites gate the publish."),
    "community-seeding":           ("SHIP",    2, "Drafts community contributions. Posting them is human."),
    "entity-authority-agent":      ("SHIP",    2, "Drafts entity and authority signals for external profiles"),
    "youtube-seo-agent":           ("SHIP",    2, "Drafts titles, descriptions and tags"),
    "youtube-publish-agent":       ("SHIP",    3, "Publishes on approval. The human is a gate, not an editor."),
    # IMPROVE
    "youtube-analytics-retro":     ("IMPROVE", 1, "Reports what performed and proposes what it means"),
    "youtube-competitor-research": ("IMPROVE", 1, "Reports competitor performance patterns"),
    "youtube-idea-validation":     ("IMPROVE", 1, "Validates an idea against observed demand"),
    # IMPROVE
    "compound":                    ("IMPROVE",    1, "Proposes how a lesson should change the system"),
}

STAGES = ["CAPTURE", "BUILD", "APPROVE", "SHIP", "IMPROVE"]
NAMES = {1: "Suggests", 2: "Drafts", 3: "Ships with approval", 4: "Autonomous"}

def main():
    total = len(SCORES)
    by_level = {l: sum(1 for v in SCORES.values() if v[1] == l) for l in (1, 2, 3, 4)}
    low = by_level[1] + by_level[2]
    pct = round(100 * low / total)

    print("# The Autonomy Ladder, scored\n")
    print(f"**{low} of {total} agents in this repo are L1 or L2.** That is {pct} percent")
    print("of the work still needing a human to decide or to ship.\n")
    print("Every vendor in this category implies L4. This is what a real production")
    print("system looks like when you score it honestly, one row at a time.\n")
    print("Regenerate this file yourself: `python3 scripts/score_autonomy.py > AUTONOMY.md`\n")
    print("## The distribution\n")
    print("| Level | Name | Count | Share |")
    print("|---|---|---|---|")
    for l in (1, 2, 3, 4):
        print(f"| **L{l}** | {NAMES[l]} | {by_level[l]} | {round(100*by_level[l]/total)}% |")
    print(f"\n## What this means\n")
    print("Sensing automates first. Making follows. **Deciding stays longest.**")
    print("Value migrates to whoever sets the bounds, which is the honest answer to")
    print("what a marketer is worth once software does the work: they move up the ladder.\n")
    print("Note where the L1s cluster. The judgment half of CAPTURE and the whole of")
    print("APPROVE are almost entirely L1, and those are the two places that")
    print("determine whether the output is worth anything.\n")
    print("## Every agent, scored\n")
    for stage in STAGES:
        units = sorted((n, v) for n, v in SCORES.items() if v[0] == stage)
        print(f"### {stage}\n")
        print("| Agent | Level | Why |")
        print("|---|---|---|")
        for name, (_, lvl, why) in units:
            print(f"| `{name}` | L{lvl} | {why} |")
        print()


if __name__ == "__main__":
    main()
