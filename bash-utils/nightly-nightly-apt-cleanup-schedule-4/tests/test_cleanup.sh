#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: using a temporary directory to avoid modifying the real system apt cache.
TMPDIR=$(mktemp -d)
export APT_CACHE_DIR="$TMPDIR"
export MAX_DAYS=7

# Create test .deb files with specific ages
# Old file – 10 days old (should be removed)
old_file="$TMPDIR/old-package.deb"
 touch "$old_file"
 touch -d "10 days ago" "$old_file"

# New file – 2 days old (should stay)
new_file="$TMPDIR/new-package.deb"
 touch "$new_file"
 touch -d "2 days ago" "$new_file"

# Run the cleanup script
bash ../src/cleanup.sh

# Verify outcomes
if [ -e "$old_file" ]; then
  echo "FAIL: old file was not removed"
  exit 1
fi
if [ ! -e "$new_file" ]; then
  echo "FAIL: new file was incorrectly removed"
  exit 1
fi

echo "PASS: old files removed, new files preserved"
