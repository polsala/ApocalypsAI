#!/usr/bin/env bash
set -e

# Create a temporary file to capture the action's output
TMP_OUTPUT=$(mktemp)
export GITHUB_OUTPUT="$TMP_OUTPUT"

# Set a known run number so the tip selection is predictable
export GITHUB_RUN_NUMBER=3

# Execute the action script (no token, so no network call)
bash src/run.sh

# Read the output produced by the script
OUTPUT=$(cat "$TMP_OUTPUT")

# Expected tip for run number 3 (0‑based indexing)
EXPECTED_TIP="Carry a flashlight, even in daylight."
EXPECTED_OUTPUT="tip=$EXPECTED_TIP"

if [[ "$OUTPUT" == "$EXPECTED_OUTPUT" ]]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: expected '$EXPECTED_OUTPUT' but got '$OUTPUT'"
  exit 1
fi
