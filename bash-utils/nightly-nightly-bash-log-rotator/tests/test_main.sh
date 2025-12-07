#!/usr/bin/env bash
set -euo pipefail

# Helper to create a file with a specific age (in days)
create_file() {
  local dir="$1"
  local name="$2"
  local age_days="$3"
  local path="$dir/$name"
  touch "$path"
  # Set modification time to "age_days" ago
  local timestamp=$(date -d "-$age_days days" +"%Y%m%d%H%M.%S")
  touch -t "$timestamp" "$path"
}

# Test 1: Normal operation (compress and delete)
TMPDIR=$(mktemp -d)
# Files: old enough to compress, recent, already compressed and old enough to delete
create_file "$TMPDIR" "old.log" 3   # >2 days old, should be compressed
create_file "$TMPDIR" "recent.log" 1   # <2 days old, should stay untouched
create_file "$TMPDIR" "very_old.log.gz" 6   # >5 days old compressed, should be deleted

# Run the rotator: compress files older than 2 days, delete compressed >5 days
bash ./src/main.sh -d "$TMPDIR" -a 2 -r 5

# Assertions
if [ ! -f "$TMPDIR/old.log.gz" ]; then
  echo "FAIL: old.log was not compressed"
  exit 1
fi
if [ -f "$TMPDIR/recent.log" ]; then
  echo "PASS: recent.log untouched"
else
  echo "FAIL: recent.log missing"
  exit 1
fi
if [ -e "$TMPDIR/very_old.log.gz" ]; then
  echo "FAIL: very_old.log.gz was not deleted"
  exit 1
else
  echo "PASS: very_old.log.gz correctly deleted"
fi

# Test 2: Dry‑run mode (no changes should happen)
TMPDIR2=$(mktemp -d)
create_file "$TMPDIR2" "dry.log" 4
bash ./src/main.sh -d "$TMPDIR2" -a 2 -r 5 -n
# In dry‑run, the original file must remain unchanged and not be compressed
if [ -f "$TMPDIR2/dry.log" ] && [ ! -f "$TMPDIR2/dry.log.gz" ]; then
  echo "PASS: dry‑run left files untouched"
else
  echo "FAIL: dry‑run modified files"
  exit 1
fi

# Cleanup
rm -rf "$TMPDIR" "$TMPDIR2"

echo "All tests passed."
