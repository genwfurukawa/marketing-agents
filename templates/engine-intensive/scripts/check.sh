#!/usr/bin/env bash
# Setup check: one green or red line per item.
ok(){ printf "\033[32mPASS\033[0m %s\n" "$1"; }; bad(){ printf "\033[31mFAIL\033[0m %s\n" "$1"; FAILED=1; }
FAILED=0
command -v claude >/dev/null && ok "Claude Code installed ($(claude --version 2>/dev/null | head -1))" || bad "Claude Code not found: install it from code.claude.com"
command -v python3 >/dev/null && ok "python3 available" || bad "python3 not found"
[ -f .claude/settings.json ] && ok "publish hook present" || bad ".claude/settings.json missing"
python3 scripts/check_brain.py brain >/dev/null && ok "example Brain passes check-brain" || bad "check-brain fails on the Brain (run: make check-brain)"
echo '{"tool_name":"Bash","tool_input":{"command":"bash scripts/publish.sh drafts/_unapproved-example.md"}}' | bash scripts/hooks/publish-gate.sh >/dev/null 2>&1
[ $? -eq 2 ] && ok "publish hook blocks an unapproved draft" || bad "publish hook did not block the test draft"
if [ "${SKIP_MODEL:-0}" = "1" ]; then echo "SKIP model test (SKIP_MODEL=1)"; else
  out=$(claude -p "Reply with the word ready." --output-format json 2>/dev/null)
  echo "$out" | grep -q total_cost_usd && ok "headless run works and reports cost" || bad "claude -p failed: log in with 'claude' first"
fi
[ $FAILED -eq 0 ] && echo "All green. You're ready for Day 1." || { echo "Something is red. Book a 15-minute setup call."; exit 1; }
