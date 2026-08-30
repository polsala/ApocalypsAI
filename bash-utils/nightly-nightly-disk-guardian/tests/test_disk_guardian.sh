#!/usr/bin/env bash

# Tests for nightly-disk-guardian (disk_guardian.sh)
# These tests run offline and use a mocked df command to provide deterministic output.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.. && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/src/disk_guardian.sh"

# Helper to run the script and capture output and exit code
run_script() {
  local path="$1"
  local threshold="$2"
  local df_mock="$3"
  # Export DF_CMD as a function name that the script will call
  export DF_CMD="$df_mock"
  output=$(bash "$SCRIPT_PATH" "$path" "$threshold" 2>&1) || exit_code=$?
  exit_code=${exit_code:-0}
  echo "$output"
  return $exit_code
}

# Mock df functions
mock_df_low() {
  cat <<'EOF'
Filesystem     1024-blocks    Used Available Capacity Mounted on
/dev/sda1       1000000       200000 800000   20% /
EOF
}

mock_df_high() {
  cat <<'EOF'
Filesystem     1024-blocks    Used Available Capacity Mounted on
/dev/sda1       1000000       900000 100000   90% /
EOF
}

# Test 1: Usage below threshold (should report all clear)
output=$(run_script "/" "50" "mock_df_low")
if [[ "$output" != *"All clear"* ]]; then
  echo "Test 1 FAILED: Expected 'All clear' message, got: $output"
  exit 1
fi

echo "Test 1 passed"

# Test 2: Usage above threshold (should contain a whimsical warning)
output=$(run_script "/" "80" "mock_df_high")
# The warning messages all contain an emoji; check for one of them
if [[ "$output" != *"⚠️"* && "$output" != *"🚨"* && "$output" != *"🛑"* && "$output" != *"💥"* && "$output" != *"🔔"* ]]; then
  echo "Test 2 FAILED: Expected a whimsical warning, got: $output"
  exit 1
fi

echo "Test 2 passed"

# Clean up
unset DF_CMD

echo "All tests passed"
