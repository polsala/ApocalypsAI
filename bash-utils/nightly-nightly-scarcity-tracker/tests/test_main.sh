#!/usr/bin/env bash
# Test suite for nightly-scarcity-tracker

set -euo pipefail

# Create temporary directory
TMPDIR=$(mktemp -d)
# Mock rationale: isolate test environment to avoid affecting real files
cp "$(dirname "$0")/../src/main.sh" "$TMPDIR/main.sh"
chmod +x "$TMPDIR/main.sh"

cd "$TMPDIR"

# Test adding items
./main.sh add water 10 > /dev/null
./main.sh add food 5 > /dev/null

# Verify inventory content
expected="water: 10
food: 5"
actual=$(cat inventory.txt)
if [[ "$actual" != "$expected" ]]; then
  echo "FAIL: inventory after adds"
  echo "Expected:"
  echo "$expected"
  echo "Got:"
  echo "$actual"
  exit 1
fi

# Test removing some water
./main.sh remove water 3 > /dev/null

expected="water: 7
food: 5"
actual=$(cat inventory.txt)
if [[ "$actual" != "$expected" ]]; then
  echo "FAIL: inventory after remove"
  exit 1
fi

# Test listing
list_output=$(./main.sh list)
if [[ "$list_output" != "$expected" ]]; then
  echo "FAIL: list output mismatch"
  exit 1
fi

echo "All tests passed!"
