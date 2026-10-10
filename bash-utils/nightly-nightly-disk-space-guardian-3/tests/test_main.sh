#!/usr/bin/env bash
set -euo pipefail

# Helper to run the utility and capture output
run_util() {
  ./src/main.sh "$@" 2>/dev/null || true
}

# Create a temporary workspace
TMP_ROOT=$(mktemp -d)
trap 'rm -rf "$TMP_ROOT"' EXIT

SCAN_DIR="$TMP_ROOT/scan"
TRASH_DIR="$TMP_ROOT/trash"
mkdir -p "$SCAN_DIR"

# Create test files (sizes are deterministic using truncate)
truncate -s 1M "$SCAN_DIR/small.txt"
truncate -s 5M "$SCAN_DIR/large.txt"

# ------------------------------------------------------------
# Test 1: No files exceed a high threshold (10 MiB)
output=$(run_util -d "$SCAN_DIR" -t 10 -r "$TRASH_DIR")
if [[ "$output" != *"No files larger than 10 MiB"* ]]; then
  echo "Test 1 failed: expected no‑large‑file message"
  exit 1
fi

echo "Test 1 passed"

# ------------------------------------------------------------
# Test 2: Detect and auto‑move a large file (threshold 2 MiB, -a flag)
output=$(run_util -d "$SCAN_DIR" -t 2 -r "$TRASH_DIR" -a)
# Verify the file was moved
if [[ ! -f "$TRASH_DIR/large.txt" ]]; then
  echo "Test 2 failed: large.txt was not moved to trash"
  exit 1
fi
# Verify the small file remains in place
if [[ ! -f "$SCAN_DIR/small.txt" ]]; then
  echo "Test 2 failed: small.txt should remain in the scan directory"
  exit 1
fi

echo "Test 2 passed"

echo "All tests passed"
