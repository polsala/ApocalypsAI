#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: create a temporary directory with known file sizes to test the script deterministically.
TMPDIR=$(mktemp -d)
cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

# Create files totaling 5 MiB
# Mock rationale: using dd with /dev/zero ensures predictable size without external dependencies.
dd if=/dev/zero of="$TMPDIR/file1.bin" bs=1M count=3 status=none
dd if=/dev/zero of="$TMPDIR/file2.bin" bs=1M count=2 status=none

# Test case 1: limit 10 MiB (should be calm, ~50% usage)
OUTPUT=$(../src/main.sh "$TMPDIR" 10)
if [[ "$OUTPUT" != *"All is calm"* ]]; then
  echo "Test failed: expected calm message, got: $OUTPUT"
  exit 1
fi

# Test case 2: limit 5 MiB (should be overflowing, 100% usage)
OUTPUT=$(../src/main.sh "$TMPDIR" 5)
if [[ "$OUTPUT" != *"overflowing"* ]]; then
  echo "Test failed: expected overflow message, got: $OUTPUT"
  exit 1
fi

echo "All tests passed"
