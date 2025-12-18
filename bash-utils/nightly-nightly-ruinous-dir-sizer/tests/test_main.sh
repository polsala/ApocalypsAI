#!/usr/bin/env bash

# Test suite for nightly-ruinous-dir-sizer
# Mock rationale: we create a temporary directory with files of known sizes and verify the script's output.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
SCRIPT="$SCRIPT_DIR/main.sh"

# Create a temporary workspace
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Helper to create a file of a specific size (in bytes)
create_file() {
  local path=$1
  local size=$2
  # Use truncate to set exact size
  truncate -s "$size" "$path"
}

# Setup known files
create_file "$TMPDIR/file_small" 512      # 512 B
create_file "$TMPDIR/file_medium" 2048    # 2 KiB
create_file "$TMPDIR/file_large" 1048576  # 1 MiB

# Expected order for top 2 entries (largest first)
EXPECTED=$(printf "%10d bytes\t%s\n" 1048576 "$TMPDIR/file_large" 2048 "$TMPDIR/file_medium")

# Run the script with -n 2
OUTPUT=$(bash "$SCRIPT" -n 2 "$TMPDIR")

# Compare output (ignore the header line)
ACTUAL=$(echo "$OUTPUT" | tail -n +2)

if [[ "$ACTUAL" == "$EXPECTED" ]]; then
  echo "PASS: top 2 largest entries reported correctly"
  exit 0
else
  echo "FAIL: output did not match expected"
  echo "Expected:"
  echo "$EXPECTED"
  echo "Actual:"
  echo "$ACTUAL"
  exit 1
fi
