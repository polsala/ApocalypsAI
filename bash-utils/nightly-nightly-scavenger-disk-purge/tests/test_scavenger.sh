#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: create temporary directory with files of varying ages
TMPDIR=$(mktemp -d)
cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

# Create a recent file (1 day old)
touch -t "$(date -d '1 day ago' +%Y%m%d%H%M.%S)" "$TMPDIR/recent.log"
# Create an old file (10 days old)
touch -t "$(date -d '10 days ago' +%Y%m%d%H%M.%S)" "$TMPDIR/old.log"

# Run script in dry‑run mode, age 7 days
output=$(bash ../../src/scavenger.sh -d "$TMPDIR" -a 7 -n)

# Expect that old.log is listed for deletion, recent.log is not
if [[ "$output" != *"Would delete $TMPDIR/old.log"* ]]; then
  echo "FAIL: old.log not identified for deletion"
  exit 1
fi
if [[ "$output" == *"recent.log"* ]]; then
  echo "FAIL: recent.log incorrectly identified as old"
  exit 1
fi

# Now run actual deletion (non‑dry run)
bash ../../src/scavenger.sh -d "$TMPDIR" -a 7

# Verify old.log removed, recent.log still exists
if [[ -e "$TMPDIR/old.log" ]]; then
  echo "FAIL: old.log still exists after deletion"
  exit 1
fi
if [[ ! -e "$TMPDIR/recent.log" ]]; then
  echo "FAIL: recent.log missing unexpectedly"
  exit 1
fi

echo "PASS"
exit 0
