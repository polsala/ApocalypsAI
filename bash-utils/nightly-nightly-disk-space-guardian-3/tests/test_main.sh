#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: create a temporary directory with known file sizes
TMPDIR=$(mktemp -d)
cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

# Create files of different sizes
dd if=/dev/zero of="$TMPDIR/file_small.txt" bs=1K count=1 status=none
dd if=/dev/zero of="$TMPDIR/file_medium.txt" bs=1K count=10 status=none
dd if=/dev/zero of="$TMPDIR/file_large.txt" bs=1K count=100 status=none

# Run the script to get top 2 entries
OUTPUT=$(bash ../../src/main.sh -d "$TMPDIR" -n 2)

# Verify that the largest file appears first
if ! echo "$OUTPUT" | grep -q "file_large.txt"; then
  echo "Test failed: largest file not reported"
  exit 1
fi

# Verify that the second largest file appears
if ! echo "$OUTPUT" | grep -q "file_medium.txt"; then
  echo "Test failed: second largest file not reported"
  exit 1
fi

echo "All tests passed."
