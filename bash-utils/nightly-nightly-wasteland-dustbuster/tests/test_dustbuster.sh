#!/usr/bin/env bash
set -euo pipefail

# --- Setup temporary environment ---
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Create an old file (timestamp set to Jan 1, 2020)
OLD_FILE="$TMPDIR/old.log"
touch -t 202001010000 "$OLD_FILE"

# Create a recent file (timestamp set to now)
NEW_FILE="$TMPDIR/new.log"
touch "$NEW_FILE"

# --- Test dry‑run mode ---
DRY_OUTPUT=$(bash ../src/dustbuster.sh -p "$TMPDIR" -d 30 -n)
if [[ "$DRY_OUTPUT" != *"Would compress: $OLD_FILE"* ]]; then
  echo "[FAIL] Dry‑run did not list the expected old file"
  exit 1
fi

# Ensure no compression happened in dry‑run
if [[ -f "$OLD_FILE.gz" ]]; then
  echo "[FAIL] Dry‑run unexpectedly created a compressed file"
  exit 1
fi

# --- Test actual compression ---
# Use -d 0 to target all files (including the recent one)
bash ../src/dustbuster.sh -p "$TMPDIR" -d 0

# Verify that the old file is now compressed
if [[ ! -f "$OLD_FILE.gz" ]]; then
  echo "[FAIL] Expected $OLD_FILE.gz to exist after compression"
  exit 1
fi

# Verify that the original old file has been removed
if [[ -f "$OLD_FILE" ]]; then
  echo "[FAIL] Original file $OLD_FILE still exists after compression"
  exit 1
fi

# Verify that the recent file was also compressed (since -d 0 targets all)
if [[ ! -f "$NEW_FILE.gz" ]]; then
  echo "[FAIL] Expected $NEW_FILE.gz to exist after compression"
  exit 1
fi

echo "All tests passed."
