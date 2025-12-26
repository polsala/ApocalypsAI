#!/usr/bin/env bash
# Tests for nightly-survival-todo

set -euo pipefail

# Locate script (assume relative path)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
SCRIPT="$SCRIPT_DIR/main.sh"

# Create temporary todo file
TMP_TODO=$(mktemp)
export TODO_FILE="$TMP_TODO"

# Test adding tasks
"$SCRIPT" add "Gather water"
"$SCRIPT" add "Build shelter"

# Test listing
LIST_OUTPUT=$("$SCRIPT" list)
expected="1) Gather water\n2) Build shelter"
if [[ "$LIST_OUTPUT" != "$expected" ]]; then
  echo "List output mismatch"
  echo "Got:"
  echo "$LIST_OUTPUT"
  echo "Expected:"
  echo "$expected"
  exit 1
fi

# Test marking done
DONE_OUTPUT=$("$SCRIPT" done 1)
if [[ "$DONE_OUTPUT" != "Completed: Gather water" ]]; then
  echo "Done output mismatch"
  exit 1
fi

# Verify remaining task
LIST_AFTER=$("$SCRIPT" list)
expected_after="1) Build shelter"
if [[ "$LIST_AFTER" != "$expected_after" ]]; then
  echo "Post‑done list mismatch"
  exit 1
fi

echo "All tests passed."
