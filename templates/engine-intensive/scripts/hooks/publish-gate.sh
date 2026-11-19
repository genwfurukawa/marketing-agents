#!/usr/bin/env bash
# PreToolUse hook. Blocks `scripts/publish.sh <draft>` unless gates 1-3 passed and the
# draft's front matter says approved: true. Exit 2 = deny (Claude Code hooks docs).
input=$(cat)
cmd=$(printf '%s' "$input" | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get("tool_input",{}).get("command",""))')
# Only gate when publish.sh is being run, not read (cat, grep, less are allowed).
printf '%s' "$cmd" | python3 -c 'import sys,re; sys.exit(0 if re.search(r"(^|[;&|]\s*|\b(bash|sh|zsh)\s+)(\./)?scripts/publish\.sh\b", sys.stdin.read()) else 1)' || exit 0
draft=$(printf '%s' "$cmd" | sed -E 's/.*scripts\/publish\.sh[[:space:]]+([^[:space:]]+).*/\1/')
bash "$(dirname "$0")/../gate-status.sh" "$draft"
exit $?
