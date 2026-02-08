#!/usr/bin/env bash
set -e
# Mock input date
export INPUT_DATE="2023-10-31"
# Create temporary output file
TMP_OUTPUT=$(mktemp)
export GITHUB_OUTPUT="$TMP_OUTPUT"
# Run the script
bash "$(dirname "$0")/../src/determine_weekday.sh"
# Source the output to get the variable
source "$TMP_OUTPUT"
# Verify the result
if [ "$weekday" = "Tuesday" ]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: expected Tuesday, got $weekday"
  exit 1
fi
