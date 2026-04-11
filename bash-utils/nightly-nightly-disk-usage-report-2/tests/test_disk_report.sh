#!/usr/bin/env bash

# Test suite for nightly-disk-usage-report
# Uses a temporary directory with known file sizes.

set -euo pipefail

# Create temporary workspace
TMPDIR=$(mktemp -d)
cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

# Helper to create a file of given size (in bytes)
create_file() {
  local path=$1 size=$2
  dd if=/dev/zero of="$path" bs=1 count="$size" status=none
}

# Setup test files
create_file "$TMPDIR/file_a" 1024   # 1 KiB
create_file "$TMPDIR/file_b" 2048   # 2 KiB
create_file "$TMPDIR/file_c" 512    # 0.5 KiB

# Run the script
OUTPUT=$(bash ../src/disk_report.sh "$TMPDIR" 3)

# Extract the second column (path) from output lines after header
mapfile -t LINES <<<"$(echo "$OUTPUT" | tail -n +2)"
paths=()
for line in "${LINES[@]}"; do
  path=$(echo "$line" | awk -F'\t' '{print $2}')
  paths+=("$path")
done

# Assertions
if [[ "${paths[0]}" != "$TMPDIR/file_b" ]]; then
  echo "FAIL: Largest file should be file_b, got ${paths[0]}" >&2
  exit 1
fi
if [[ "${paths[1]}" != "$TMPDIR/file_a" ]]; then
  echo "FAIL: Second largest should be file_a, got ${paths[1]}" >&2
  exit 1
fi
if [[ "${paths[2]}" != "$TMPDIR/file_c" ]]; then
  echo "FAIL: Third largest should be file_c, got ${paths[2]}" >&2
  exit 1
fi

echo "PASS"
