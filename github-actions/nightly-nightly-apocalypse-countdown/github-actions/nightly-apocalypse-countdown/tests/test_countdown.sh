#!/usr/bin/env bash
set -e

# Mock environment variables for a deterministic run
export TARGET_DATE="2099-01-01"
export CURRENT_DATE="2098-12-30"

# Capture the script output
OUTPUT=$(bash "$(dirname "$0")/../src/countdown.sh")

EXPECTED="2 days until the apocalypse!"

if [[ "$OUTPUT" == "$EXPECTED" ]]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: expected '$EXPECTED', got '$OUTPUT'"
  exit 1
fi
