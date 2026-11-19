#!/usr/bin/env bash
# Gate 1: deterministic checks before any model reads the draft. Writes a pass mark to .gates/.
f="$1"; [ -f "$f" ] || { echo "usage: grep-gate.sh drafts/<file>.md"; exit 64; }
fail=0
if grep -n $'—' "$f"; then echo "FAIL em dash"; fail=1; fi
if grep -n "\[NEEDS SOURCE\]" "$f"; then echo "FAIL unsourced claim left in"; fail=1; fi
while IFS= read -r phrase; do
  [ -z "$phrase" ] && continue; case "$phrase" in \#*) continue;; esac
  if grep -n -i -F -- "$phrase" "$f"; then echo "FAIL banned phrase: $phrase"; fail=1; fi
done < voice/banned.txt
mkdir -p .gates; base=$(basename "$f")
if [ $fail -eq 0 ]; then echo pass > ".gates/$base.grep"; echo "gate 1: PASS"; else rm -f ".gates/$base.grep"; echo "gate 1: FAIL"; exit 1; fi
