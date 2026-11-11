#!/usr/bin/env bash
set -euo pipefail

# --- Setup temporary environment ---
TMPDIR=$(mktemp -d)
# Ensure cleanup on exit
trap 'rm -rf "$TMPDIR"' EXIT

# Create a mix of files
touch "$TMPDIR/file1.txt"                # non‑empty placeholder (still zero‑byte but will be filled)
> "$TMPDIR/file1.txt"                    # make it non‑empty
touch "$TMPDIR/empty1"                    # ghost
touch "$TMPDIR/empty2"                    # ghost
> "$TMPDIR/empty2"                        # keep empty (no content)

# --- Dry‑run test (no deletion) ---
OUTPUT=$(bash ../src/ghost_buster.sh -d "$TMPDIR")
# Expected JSON contains ghost_count 2 and action "found"
if [[ "$OUTPUT" != *'"ghost_count":2'* ]]; then
  echo "FAIL: Dry‑run reported wrong ghost count: $OUTPUT" >&2
  exit 1
fi
if [[ "$OUTPUT" != *'"action":"found"'* ]]; then
  echo "FAIL: Dry‑run reported wrong action: $OUTPUT" >&2
  exit 1
fi

# Verify that ghost files still exist
if [[ ! -e "$TMPDIR/empty1" || ! -e "$TMPDIR/empty2" ]]; then
  echo "FAIL: Ghost files were unexpectedly removed in dry‑run" >&2
  exit 1
fi

# --- Delete mode test ---
OUTPUT_DEL=$(bash ../src/ghost_buster.sh -d "$TMPDIR" --delete)
if [[ "$OUTPUT_DEL" != *'"ghost_count":2'* ]]; then
  echo "FAIL: Delete mode reported wrong ghost count: $OUTPUT_DEL" >&2
  exit 1
fi
if [[ "$OUTPUT_DEL" != *'"action":"deleted"'* ]]; then
  echo "FAIL: Delete mode reported wrong action: $OUTPUT_DEL" >&2
  exit 1
fi

# Verify that ghost files have been removed
if [[ -e "$TMPDIR/empty1" || -e "$TMPDIR/empty2" ]]; then
  echo "FAIL: Ghost files were not deleted in delete mode" >&2
  exit 1
fi

# Verify non‑ghost file remains untouched
if [[ ! -e "$TMPDIR/file1.txt" ]]; then
  echo "FAIL: Non‑ghost file was incorrectly removed" >&2
  exit 1
fi

echo "All tests passed"
