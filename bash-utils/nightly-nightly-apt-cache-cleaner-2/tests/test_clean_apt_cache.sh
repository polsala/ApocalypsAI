#!/usr/bin/env bash
set -euo pipefail

# Create a temporary directory to act as the mock APT cache
TMPDIR=$(mktemp -d)
export APT_CACHE_DIR="$TMPDIR"

# Create mock .deb files with controlled modification times
touch "$TMPDIR/old1.deb"
touch "$TMPDIR/old2.deb"
touch "$TMPDIR/new1.deb"

# Set timestamps: old files 40 days ago, new file 5 days ago
# Mock rationale: using touch with a specific date string
touch -d "40 days ago" "$TMPDIR/old1.deb"
touch -d "40 days ago" "$TMPDIR/old2.deb"
touch -d "5 days ago" "$TMPDIR/new1.deb"

# Run the script in dry‑run mode and capture output
OUTPUT=$(bash ../../src/clean_apt_cache.sh --days 30 --dry-run)

# Verify that only the old files are listed
if ! echo "$OUTPUT" | grep -q "old1.deb"; then
  echo "Test failed: old1.deb not listed in dry‑run output"
  exit 1
fi
if ! echo "$OUTPUT" | grep -q "old2.deb"; then
  echo "Test failed: old2.deb not listed in dry‑run output"
  exit 1
fi
if echo "$OUTPUT" | grep -q "new1.deb"; then
  echo "Test failed: new1.deb should not appear in dry‑run output"
  exit 1
fi

# Run the script to actually delete the old files
bash ../../src/clean_apt_cache.sh --days 30 --no-dry-run

# Confirm that old files have been removed and the new file remains
if [[ -e "$TMPDIR/old1.deb" ]] || [[ -e "$TMPDIR/old2.deb" ]]; then
  echo "Test failed: old files were not deleted"
  exit 1
fi
if [[ ! -e "$TMPDIR/new1.deb" ]]; then
  echo "Test failed: new file was incorrectly deleted"
  exit 1
fi

echo "All tests passed."
