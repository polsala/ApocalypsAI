#!/usr/bin/env bash
set -euo pipefail

# Create a temporary workspace
TMPDIR=$(mktemp -d)
cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

# Populate the workspace with files of known sizes
# 1 KB, 2 KB, 5 KB files
dd if=/dev/zero of="$TMPDIR/file1" bs=1024 count=1 status=none
dd if=/dev/zero of="$TMPDIR/file2" bs=1024 count=2 status=none
dd if=/dev/zero of="$TMPDIR/file3" bs=1024 count=5 status=none

# Subdirectory containing a larger file (10 KB)
mkdir "$TMPDIR/sub"
dd if=/dev/zero of="$TMPDIR/sub/bigfile" bs=1024 count=10 status=none

# Execute the utility to retrieve the top 3 entries
OUTPUT=$(bash ../../src/disk_report.sh -n 3 "$TMPDIR")

# Expected lines (du prints size followed by a tab and the path)
expected1="10K\t$TMPDIR/sub/bigfile"
expected2="5K\t$TMPDIR/file3"
expected3="2K\t$TMPDIR/file2"

# Helper to assert a line is present in the output
assert_contains() {
  local line="$1"
  if ! echo "$OUTPUT" | grep -F "$line" >/dev/null; then
    echo "Missing expected line: $line"
    echo "Actual output:"
    echo "$OUTPUT"
    exit 1
  fi
}

assert_contains "$expected1"
assert_contains "$expected2"
assert_contains "$expected3"

echo "All tests passed."
