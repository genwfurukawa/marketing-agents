#!/usr/bin/env bash
# Prints what a draft is missing before it can ship. Exit 0 = ready, 2 = blocked.
# A gate pass counts only if it was written after the draft's last edit.
draft="$1"; base=$(basename "$draft"); missing=""
for g in grep source voice; do
  m=".gates/$base.$g"
  if [ ! -f "$m" ]; then missing="$missing $g"
  elif python3 -c 'import os,sys; sys.exit(0 if os.path.getmtime(sys.argv[1]) >= os.path.getmtime(sys.argv[2]) else 1)' "$m" "$draft"; then :
  else missing="$missing $g(stale: draft edited after it passed)"; fi
done
grep -q '^approved: true' "$draft" 2>/dev/null || missing="$missing approval"
if [ -n "$missing" ]; then echo "Blocked: $draft is missing:$missing. Run the gates, then set approved: true." >&2; exit 2; fi
exit 0
