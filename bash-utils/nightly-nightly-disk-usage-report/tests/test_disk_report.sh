#!/usr/bin/env bash

set -euo pipefail

# Create a temporary directory for the test
TMPDIR=$(mktemp -d)
cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

# Populate the directory with known file sizes
# file1: 1 KiB, file2: 2 KiB, subdir/file3: 512 B
dd if=/dev/zero of="$TMPDIR/file1" bs=1024 count=1 status=none
dd if=/dev/zero of="$TMPDIR/file2" bs=1024 count=2 status=none
mkdir "$TMPDIR/subdir"
dd if=/dev/zero of="$TMPDIR/subdir/file3" bs=512 count=1 status=none

# Expected output: du on the temporary directory, limited to depth 1, sorted
EXPECTED=$(du -h --max-depth=1 "$TMPDIR"/* 2>/dev/null | sort -hr)

# Path to the script under test (relative to the test file)
SCRIPT_PATH="../src/disk_report.sh"

# Run the script and capture its output
OUTPUT=$($SCRIPT_PATH "$TMPDIR")

# Compare the actual output to the expected output
if [[ "$OUTPUT" == "$EXPECTED" ]]; then
  echo "PASS"
  exit 0
else
  echo "FAIL"
  echo "--- Expected ---"
  echo "$EXPECTED"
  echo "--- Got ---"
  echo "$OUTPUT"
  exit 1
fi
