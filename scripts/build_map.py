#!/usr/bin/env python3
"""Emit MAP.md: stage and loop for every agent, pointing at its real path.

Reads the same SCORES table as score_autonomy.py so the two can never drift.

Usage:  python3 scripts/build_map.py > MAP.md
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score_autonomy import SCORES, STAGES

# Which loop each agent belongs to. An agent can serve more than one loop; it is
# listed under the one that owns its clock.
LOOP = {
    "sm-aeo": {"aeo-checker","aeo-engine-scan","aeo-injector","aeo-page-generator",
               "ai-crawler-fix","ai-crawler-audit-agent","schema-generator",
               "cited-page-teardown","topical-authority-linker","knowledge-graph-builder",
               "community-seeding","entity-authority-agent","aeo-cross-model-reviewer",
               "ai-content-architect-agent","gap-to-content-mapper-agent"},
    "sm-content": {"blog-writer","ideate-content-ideas","topic-deep-dive","storyboard-builder",
                   "original-research-designer","insight-object-builder","insight-scorer",
                   "insight-capture-agent","compound","case-study-agent","hook-writer-agent",
                   "content-refresh-agent","email-agent","voice-validator",
                   "brand-consistency-reviewer","conversion-reviewer"},
    "sm-social": {"linkedin-post-writer","carousel-agent","youtube-script-agent",
                  "youtube-thumbnail-agent","youtube-seo-agent","youtube-publish-agent",
                  "youtube-analytics-retro","youtube-competitor-research",
                  "youtube-idea-validation","youtube-packaging-first"},
    "sm-demand": {"prospect-scorecard-agent","icp-definition-agent","positioning-agent",
                  "competitor-analysis-agent","audience-question-miner-agent"},
}
OWNER = {a: l for l, s in LOOP.items() for a in s}

def path_for(name):
    for cand in (f".claude/skills/{name}/SKILL.md", f".claude/agents/{name}.md"):
        if os.path.exists(cand):
            return cand
    return f".claude/skills/{name}/SKILL.md" if not name.endswith("-agent") else f".claude/agents/{name}.md"

unmapped = sorted(n for n in SCORES if n not in OWNER)

print("# The map\n")
print("Every agent in this repo, by loop and by stage, with the path to the file.\n")
print("The directories `brain/`, `loops/`, `gates/` and `ports/` explain the system.")
print("The agents themselves live in `.claude/`, because that is where Claude Code")
print("looks for them. This file connects the two.\n")
print("Levels are from the Autonomy Ladder. See [`AUTONOMY.md`](AUTONOMY.md).\n")

for loop in ("sm-content", "sm-aeo", "sm-social", "sm-demand"):
    members = [(n, v) for n, v in SCORES.items() if OWNER.get(n) == loop]
    print(f"## `{loop}`  ({len(members)} agents)\n")
    for stage in STAGES:
        rows = sorted((n, v) for n, v in members if v[0] == stage)
        if not rows:
            continue
        print(f"**{stage}**\n")
        print("| Agent | Level | Path |")
        print("|---|---|---|")
        for name, (_, lvl, _why) in rows:
            print(f"| `{name}` | L{lvl} | [`{path_for(name)}`]({path_for(name)}) |")
        print()

if unmapped:
    print("## Unassigned\n")
    print("Agents scored but not yet placed in a loop. Assign or remove them.\n")
    for n in unmapped:
        print(f"- `{n}`")
    print()
