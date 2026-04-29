#!/usr/bin/env bash

# Tests for nightly-env-var-diff
# --------------------------------
# These tests are self‑contained and do not require any external resources.
# They create temporary .env files, invoke the script, and compare the output
# against expected strings.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="$SCRIPT_DIR/src/env_diff.sh"

# Helper to run a test case
run_test() {
  local name="$1"
  local old_content="$2"
  local new_content="$3"
  local expected_output="$4"

  local old_file new_file
  old_file=$(mktemp)
  new_file=$(mktemp)

  # Write contents
  printf "%s" "$old_content" > "$old_file"
  printf "%s" "$new_content" > "$new_file"

  # Capture script output
  local actual_output
  actual_output=$(bash "$SCRIPT" "$old_file" "$new_file" || true)

  # Normalise whitespace for comparison
  actual_output=$(echo "$actual_output" | sed '/^$/d')
  expected_output=$(echo "$expected_output" | sed '/^$/d')

  if [[ "$actual_output" == "$expected_output" ]]; then
    echo "[PASS] $name"
  else
    echo "[FAIL] $name"
    echo "--- Expected ---"
    echo "$expected_output"
    echo "--- Got ---"
    echo "$actual_output"
    exit 1
  fi

  rm -f "$old_file" "$new_file"
}

# Test 1: identical files → no output
run_test "identical files" \
  "FOO=bar\nBAZ=qux" \
  "FOO=bar\nBAZ=qux" \
  ""

# Test 2: added, removed, and modified variables
run_test "added/removed/modified" \
  "FOO=apple\nBAR=banana\nBAZ=qux" \
  "FOO=apple\nBAR=blueberry\nNEWVAR=hello" \
  "Added:\n  NEWVAR=hello\nRemoved:\n  BAZ=qux\nModified:\n  BAR=banana -> blueberry"

# Test 3: all variables removed (new file empty)
run_test "all removed" \
  "ONE=1\nTWO=2" \
  "" \
  "Removed:\n  ONE=1\n  TWO=2"

# If we reach this point, all tests passed
exit 0
