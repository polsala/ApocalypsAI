#!/usr/bin/env bash
set -e
ACTION_FILE="$(dirname "$0")/../action.yml"
# Verify required top‑level keys exist
grep -q "^name:" "$ACTION_FILE"
grep -q "^description:" "$ACTION_FILE"
grep -q "^runs:" "$ACTION_FILE"
# Verify the composite runner is declared
grep -q "using: \"composite\"" "$ACTION_FILE"
# Verify the emojis input is defined
grep -q "emojis:" -A2 "$ACTION_FILE"
echo "All checks passed"
