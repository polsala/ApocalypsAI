#!/usr/bin/env bash
set -euo pipefail

# Locate the script under test
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
SCRIPT="$SCRIPT_DIR/main.sh"

# Create a temporary workspace
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

SMALL="$TMPDIR/small.txt"
LARGE="$TMPDIR/large.bin"

# Create a tiny file (1 KiB) and a large file (2 MiB)
# Mock rationale: using dd with /dev/zero ensures deterministic content without external network calls.
dd if=/dev/zero of="$SMALL" bs=1024 count=1 status=none
dd if=/dev/zero of="$LARGE" bs=1M count=2 status=none

# ------------------------------------------------------------
# Test 1: Listing mode – should report only the large file
# ------------------------------------------------------------
OUTPUT=$("$SCRIPT" -d "$TMPDIR" -s 1)
if [[ "$OUTPUT" != *"$LARGE"* ]]; then
  echo "FAIL: Large file not listed in output"
  exit 1
fi
if [[ "$OUTPUT" == *"$SMALL"* ]]; then
  echo "FAIL: Small file incorrectly listed"
  exit 1
fi

echo "Test 1 passed: listing works as expected"

# ------------------------------------------------------------
# Test 2: Compression mode – should create a .gz archive
# ------------------------------------------------------------
"$SCRIPT" -c -d "$TMPDIR" -s 1 >/dev/null
if [[ ! -f "${LARGE}.gz" ]]; then
  echo "FAIL: Compressed file ${LARGE}.gz not created"
  exit 1
fi

echo "Test 2 passed: compression creates .gz archive"

echo "All tests passed"
