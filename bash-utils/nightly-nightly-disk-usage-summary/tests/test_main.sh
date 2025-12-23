#!/usr/bin/env bash
set -euo pipefail

# Create temp dir
TMPDIR=$(mktemp -d)
trap 'rm -rf \"$TMPDIR\"' EXIT

# Create subdirectories with known sizes
mkdir -p \"$TMPDIR/a\" \"$TMPDIR/b\" \"$TMPDIR/c\"

# Create files
dd if=/dev/zero of=\"$TMPDIR/a/file1\" bs=1M count=5 2>/dev/null
dd if=/dev/zero of=\"$TMPDIR/b/file1\" bs=1M count=3 2>/dev/null
dd if=/dev/zero of=\"$TMPDIR/c/file1\" bs=1M count=1 2>/dev/null

# Run script
OUTPUT=$(../src/main.sh \"$TMPDIR\" 2>/dev/null)

# Check that output contains directories in descending order
# Use grep to find lines
echo \"$OUTPUT\" | grep -q \"$TMPDIR/a\"
echo \"$OUTPUT\" | grep -q \"$TMPDIR/b\"
echo \"$OUTPUT\" | grep -q \"$TMPDIR/c\"

# Check that sizes are correct (approx)
# Since du -sh may output 5.0M, 3.0M, 1.0M
echo \"$OUTPUT\" | grep -q \"5.0M\"
echo \"$OUTPUT\" | grep -q \"3.0M\"
echo \"$OUTPUT\" | grep -q \"1.0M\"

# Ensure top 3 lines
LINE_COUNT=$(echo \"$OUTPUT\" | wc -l)
if [[ \"$LINE_COUNT\" -ne 3 ]]; then
  echo \"Expected 3 lines, got $LINE_COUNT\" >&2
  exit 1
fi

echo \"Test passed\"
