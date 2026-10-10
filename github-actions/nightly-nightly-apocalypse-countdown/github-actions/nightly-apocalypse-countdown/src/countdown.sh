#!/usr/bin/env bash
set -e

# Ensure TARGET_DATE is provided
if [[ -z "$TARGET_DATE" ]]; then
  echo "Error: TARGET_DATE not set"
  exit 1
fi

# Use CURRENT_DATE if supplied, otherwise today's date
CURRENT="${CURRENT_DATE:-$(date +%Y-%m-%d)}"

# Convert dates to epoch seconds (GNU date required)
TARGET_SEC=$(date -d "$TARGET_DATE" +%s)
CURRENT_SEC=$(date -d "$CURRENT" +%s)

DIFF_SEC=$(( TARGET_SEC - CURRENT_SEC ))

if (( DIFF_SEC < 0 )); then
  echo "The apocalypse has already occurred."
  exit 0
fi

# Compute days remaining, rounding up
DAYS=$(( (DIFF_SEC + 86400 - 1) / 86400 ))

if (( DAYS == 0 )); then
  echo "The apocalypse is today!"
else
  echo "${DAYS} days until the apocalypse!"
fi
