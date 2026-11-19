#!/usr/bin/env bash
# Ship one approved draft and append a ledger row. Posting itself is by hand or your CMS:
# this script records it. Usage: scripts/publish.sh drafts/<file>.md <channel> <url> <minutes> [cost_usd]
f="$1"; ch="$2"; url="$3"; mins="$4"; cost="${5:-}"
[ -f "$f" ] && [ -n "$ch" ] && [ -n "$url" ] && [ -n "$mins" ] || { echo "usage: publish.sh drafts/<file>.md <channel> <url> <minutes> [cost_usd]"; exit 64; }
# Same check as the hook, so publishing outside Claude Code is gated too.
bash "$(dirname "$0")/gate-status.sh" "$f" || exit 2
ids=$(grep -o 'src:[A-Za-z0-9_-]*' "$f" | sort -u | tr '\n' ' ')
echo "$(date +%F),shipped,$ch,$url,$(basename "$f"),$mins,$cost,,${ids% }" >> ledger/ledger.csv
echo "logged: $(tail -1 ledger/ledger.csv)"
