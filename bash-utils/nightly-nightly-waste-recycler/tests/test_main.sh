#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: create a temporary directory with files of known ages
TMPDIR=$(mktemp -d)
cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

# Create a recent file (modified today)
touch "$TMPDIR/recent.txt"
# Create an old file (modified 10 days ago)
# Mock rationale: set its modification time to exactly 10 days ago
old_time=$(date -d '10 days ago' +%Y%m%d%H%M.%S)
touch -t "$old_time" "$TMPDIR/old.txt"

# ---------- Dry‑run test ----------
# Expect only old.txt to appear in the output when looking for files >5 days old
output=$(bash ../src/main.sh "$TMPDIR" 5)
if [[ "$output" != *"old.txt"* ]] || [[ "$output" == *"recent.txt"* ]]; then
  echo "Dry‑run test failed"
  exit 1
fi

# ---------- Delete test ----------
# Actually delete files older than 5 days
bash ../src/main.sh -d "$TMPDIR" 5
# old.txt should have been removed
if [[ -e "$TMPDIR/old.txt" ]]; then
  echo "Delete test failed: old.txt still exists"
  exit 1
fi

# recent.txt should still be present
if [[ ! -e "$TMPDIR/recent.txt" ]]; then
  echo "Delete test failed: recent.txt was unexpectedly removed"
  exit 1
fi

echo "All tests passed"
