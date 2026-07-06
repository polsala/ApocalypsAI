#!/usr/bin/env bash

# nightly-ramen-recipe-suggester test suite
# ------------------------------------------------------------
# These tests invoke the script with explicit load values to avoid
# dependence on the host's actual load. They verify that the correct
# ramen level (Mild, Medium, Spicy) is selected.
# ------------------------------------------------------------

set -e

SCRIPT="../src/ramen_suggester.sh"

run() {
  "$SCRIPT" "$1"
}

# Test low load → Mild
output=$(run "0.3")
if [[ "$output" != *"Mild"* ]]; then
  echo "FAIL: Expected Mild for load 0.3"
  exit 1
fi

# Test medium load → Medium
output=$(run "1.0")
if [[ "$output" != *"Medium"* ]]; then
  echo "FAIL: Expected Medium for load 1.0"
  exit 1
fi

# Test high load → Spicy
output=$(run "2.5")
if [[ "$output" != *"Spicy"* ]]; then
  echo "FAIL: Expected Spicy for load 2.5"
  exit 1
fi

echo "All tests passed."
