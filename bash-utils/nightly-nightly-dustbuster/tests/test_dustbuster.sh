#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: create isolated temporary directory for testing
TMPDIR=$(mktemp -d)
cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

# Create test files
touch "$TMPDIR/old.tmp"
touch "$TMPDIR/recent.tmp"
touch "$TMPDIR/old.log"
# Set modification times to simulate old files (Jan 1 2020)
touch -t 202001010000 "$TMPDIR/old.tmp"
touch -t 202001010000 "$TMPDIR/old.log"
# recent.tmp keeps current timestamp

# Run dustbuster in dry‑run mode
output=$(bash ../../src/dustbuster.sh -d "$TMPDIR" -r)

# Expect old files to be listed, recent file not listed
if ! echo "$output" | grep -q "old.tmp"; then
  echo "FAIL: old.tmp not detected in dry‑run output"
  exit 1
fi
if echo "$output" | grep -q "recent.tmp"; then
  echo "FAIL: recent.tmp should not appear in dry‑run output"
  exit 1
fi

# Run dustbuster in clean mode, automatically answer 'y'
printf 'y\n' | bash ../../src/dustbuster.sh -d "$TMPDIR" -c > /dev/null

# Verify that old files have been removed
if [[ -e "$TMPDIR/old.tmp" || -e "$TMPDIR/old.log" ]]; then
  echo "FAIL: old files were not deleted in clean mode"
  exit 1
fi

# recent.tmp should still exist
if [[ ! -e "$TMPDIR/recent.tmp" ]]; then
  echo "FAIL: recent.tmp was unexpectedly deleted"
  exit 1
fi

echo "PASS"
