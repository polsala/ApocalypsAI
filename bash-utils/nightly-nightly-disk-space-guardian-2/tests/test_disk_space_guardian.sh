#!/usr/bin/env bash
set -euo pipefail

# Helper to create a file with a specific size (bytes)
make_file() {
  local path=$1
  local size=$2
  dd if=/dev/zero of="$path" bs=1 count="$size" status=none
}

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Create test files of known sizes
make_file "$TMPDIR/a.txt" 100
make_file "$TMPDIR/b.txt" 200
make_file "$TMPDIR/c.txt" 50

# Test that the script lists the top 2 largest files correctly
OUTPUT=$(bash ../src/disk_space_guardian.sh -d "$TMPDIR" -n 2)
if ! echo "$OUTPUT" | grep -q "200 $TMPDIR/b.txt"; then
  echo "FAIL: b.txt not listed as largest"
  exit 1
fi
if ! echo "$OUTPUT" | grep -q "100 $TMPDIR/a.txt"; then
  echo "FAIL: a.txt not listed as second largest"
  exit 1
fi

# Create a file that is older than 1 day
make_file "$TMPDIR/old.txt" 10
# Set its modification time to 2 days ago
touch -d "2 days ago" "$TMPDIR/old.txt"

# Run the script to delete files older than 1 day (with -y to actually delete)
bash ../src/disk_space_guardian.sh -d "$TMPDIR" -a 1 -y

if [[ -e "$TMPDIR/old.txt" ]]; then
  echo "FAIL: old.txt was not deleted"
  exit 1
fi

echo "All tests passed."
