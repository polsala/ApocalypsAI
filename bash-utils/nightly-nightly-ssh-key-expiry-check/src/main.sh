#!/usr/bin/env bash
set -euo pipefail

KEY_FILE="${1:-$HOME/.ssh/authorized_keys}"
CURRENT_DATE="${CURRENT_DATE:-$(date +%Y-%m-%d)}"

# Convert current date to epoch
CURRENT_EPOCH=$(date -d "$CURRENT_DATE" +%s)

EXPIRED=0

while IFS= read -r line; do
  # Skip empty lines and comments not containing expires=
  if [[ -z "$line" || ! "$line" =~ expires= ]]; then
    continue
  fi
  # Extract expires date
  if [[ "$line" =~ expires=([0-9]{4}-[0-9]{2}-[0-9]{2}) ]]; then
    EXP_DATE="${BASH_REMATCH[1]}"
    EXP_EPOCH=$(date -d "$EXP_DATE" +%s 2>/dev/null || true)
    if [[ -z "$EXP_EPOCH" ]]; then
      continue
    fi
    if (( EXP_EPOCH < CURRENT_EPOCH )); then
      echo "Expired key: $(echo "$line" | awk '{print $NF}') (expires=$EXP_DATE)"
      EXPIRED=1
    fi
  fi
done < "$KEY_FILE"

if (( EXPIRED )); then
  exit 1
else
  echo "All keys valid."
  exit 0
fi
