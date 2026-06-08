#!/usr/bin/env bash
# Tests for nightly-dusty-disk-watcher
# These tests are deterministic and do not touch the real filesystem.

set -euo pipefail

SCRIPT_PATH="../src/disk_watcher.sh"

# Helper to run the script and capture output and exit code
run_watcher() {
  local dir="$1"
  local threshold="$2"
  local mock_du="$3"
  MOCK_DU_OUTPUT="$mock_du" "$SCRIPT_PATH" "$dir" "$threshold"
  echo $?
}

# Test 1: Size below threshold – expect exit code 0 and a success message
test_below_threshold() {
  local exit_code
  exit_code=$(run_watcher "/tmp" 100 50000) # 50,000KB = ~48MiB < 100MiB
  if [[ $exit_code -ne 0 ]]; then
    echo "FAIL: Expected exit code 0 for below‑threshold case, got $exit_code"
    exit 1
  fi
  echo "PASS: below‑threshold case"
}

# Test 2: Size above threshold – expect exit code 1 and a warning line containing ⚠️
test_above_threshold() {
  local output
  output=$(MOCK_DU_OUTPUT=200000 "$SCRIPT_PATH" "/var/log" 150 2>&1) || true
  local exit_code=$?
  if [[ $exit_code -ne 1 ]]; then
    echo "FAIL: Expected exit code 1 for above‑threshold case, got $exit_code"
    exit 1
  fi
  if ! echo "$output" | grep -q "⚠️"; then
    echo "FAIL: Expected warning symbol in output, got:"
    echo "$output"
    exit 1
  fi
  echo "PASS: above‑threshold case"
}

# Run tests
test_below_threshold
test_above_threshold

echo "All tests passed."
