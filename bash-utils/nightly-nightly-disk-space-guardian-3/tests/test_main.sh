#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: create a temporary directory with known file sizes
TMPDIR=$(mktemp -d)
cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

# Create files of specific sizes
dd if=/dev/zero of="$TMPDIR/file_small" bs=1K count=1 >/dev/null 2>&1
dd if=/dev/zero of="$TMPDIR/file_medium" bs=1K count=1024 >/dev/null 2>&1   # 1MiB
dd if=/dev/zero of="$TMPDIR/file_large" bs=1K count=20480 >/dev/null 2>&1   # 20MiB

# Make the large file appear old
touch -d "40 days ago" "$TMPDIR/file_large"

SCRIPT_PATH="$(dirname "$0")/../src/main.sh"

# Test 1: Verify top 2 entries include the large file
output=$("$SCRIPT_PATH" -d "$TMPDIR" -n 2)
if ! echo "$output" | grep -q "file_large"; then
  echo "Test 1 failed: file_large not reported as a top entry"
  exit 1
fi

# Test 2: Archive files older than 30 days
cd "$TMPDIR"
"$SCRIPT_PATH" -d "$TMPDIR" -a 30
if [[ ! -f "archive.tar.gz" ]]; then
  echo "Test 2 failed: archive.tar.gz not created"
  exit 1
fi
# Ensure the archive contains the large file
if ! tar -tzf "archive.tar.gz" | grep -q "file_large"; then
  echo "Test 2 failed: file_large not present in archive"
  exit 1
fi

echo "All tests passed."
