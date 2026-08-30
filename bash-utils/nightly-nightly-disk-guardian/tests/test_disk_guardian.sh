#!/usr/bin/env bash
# Test suite for nightly-disk-guardian
set -e

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
SOURCE_DIR="$SCRIPT_DIR/../src"

# Load the script (functions only, no execution)
source "$SOURCE_DIR/disk_guardian.sh"

# --- Test high usage triggers warning ---
function get_df() {
  echo "85"
}
output=$(main 2>&1) || status=$?
if [[ "$status" -ne 1 ]]; then
  echo "FAIL: Expected exit code 1 for high usage, got $status"
  exit 1
fi
if [[ "$output" != *"bursting"* ]]; then
  echo "FAIL: Expected warning ASCII art in output"
  exit 1
fi

# --- Test low usage reports calm ---
function get_df() {
  echo "45"
}
output=$(main 2>&1) || status=$?
if [[ "$status" -ne 0 ]]; then
  echo "FAIL: Expected exit code 0 for low usage, got $status"
  exit 1
fi
if [[ "$output" != *"All is calm"* ]]; then
  echo "FAIL: Expected calm message in output"
  exit 1
fi

echo "All tests passed"
