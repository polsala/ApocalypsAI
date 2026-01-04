#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: create a temporary cache with files of known ages
TMPDIR=$(mktemp -d)
export APT_CACHE_DIR="$TMPDIR"

# Create a fresh package (1 day old) – timestamp set to 2024-02-09 01:01
touch -t 202402090101 "$TMPDIR/fresh.deb"
# Create a stale package (40 days old) – timestamp set to 2023-12-31 01:01
touch -t 202312310101 "$TMPDIR/stale.deb"

# Run the script in dry‑run mode with a 30‑day threshold
OUTPUT=$("$PWD/../src/main.sh" -d 30)

# Verify that the stale file is listed and the fresh file is not
if [[ "$OUTPUT" != *"stale.deb"* ]]; then
  echo "Test failed: stale file not listed"
  exit 1
fi
if [[ "$OUTPUT" == *"fresh.deb"* ]]; then
  echo "Test failed: fresh file incorrectly listed"
  exit 1
fi
if [[ "$OUTPUT" != *"Dry run mode"* ]]; then
  echo "Test failed: dry‑run message missing"
  exit 1
fi

# Now run with the --delete flag to actually purge stale packages
"$PWD/../src/main.sh" -d 30 --delete > /dev/null

# The stale package should be gone, fresh should remain
if [[ -e "$TMPDIR/stale.deb" ]]; then
  echo "Test failed: stale file not deleted"
  exit 1
fi
if [[ ! -e "$TMPDIR/fresh.deb" ]]; then
  echo "Test failed: fresh file was incorrectly deleted"
  exit 1
fi

echo "All tests passed."
