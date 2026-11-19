#!/usr/bin/env python3
"""Fail if any fact line in brain/*.md lacks a `source:`. Lines under a
'## Needs a human' heading are allowed without one. Headings, blank lines and
lines starting with '>' (notes) are skipped."""
import sys, pathlib, re
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "brain")
bad = 0
for f in sorted(root.glob("*.md")):
    section = ""
    for n, line in enumerate(f.read_text().splitlines(), 1):
        s = line.strip()
        if s.startswith("#"):
            section = s.lower(); continue
        if not s or s.startswith(">") or "needs a human" in section:
            continue
        if s.startswith(("-", "*")) or re.match(r"^\d+\.", s):
            if "source:" not in s.lower():
                print(f"{f}:{n}: no source: {s[:80]}"); bad += 1
print("check-brain: PASS" if not bad else f"check-brain: FAIL ({bad} unsourced lines)")
sys.exit(1 if bad else 0)
