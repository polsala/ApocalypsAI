#!/usr/bin/env bash
set -euo pipefail

# Helper: create a temporary directory and clean up on exit
TMPDIR=$(mktemp -d)
cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

# Create test files
# Small file: 1 KiB
dd if=/dev/zero of="$TMPDIR/small.txt" bs=1024 count=1 status=none
# Large file: 2 MiB
dd if=/dev/zero of="$TMPDIR/large.txt" bs=1M count=2 status=none

SCRIPT_PATH="$(dirname "${BASH_SOURCE[0]}")/../src/disk_guardian.sh"

# ------------------------------------------------------------
# Test 1: Detection without moving
# ------------------------------------------------------------
output=$($SCRIPT_PATH -d "$TMPDIR" -s 1)
# Expect the large file to be reported, small file not mentioned
if ! echo "$output" | grep -q "large.txt"; then
  echo "[FAIL] Large file not reported in detection test"
  exit 1
fi
if echo "$output" | grep -q "small.txt"; then
  echo "[FAIL] Small file incorrectly reported in detection test"
  exit 1
fi

echo "[PASS] Detection without moving"

# ------------------------------------------------------------
# Test 2: Detection with moving (-m flag)
# ------------------------------------------------------------
output=$($SCRIPT_PATH -d "$TMPDIR" -s 1 -m)
# After moving, the original large file should no longer exist
if [[ -e "$TMPDIR/large.txt" ]]; then
  echo "[FAIL] Large file still present after move"
  exit 1
fi
# It should now reside in .trash
if [[ ! -e "$TMPDIR/.trash/large.txt" ]]; then
  echo "[FAIL] Large file not found in .trash after move"
  exit 1
fi

echo "[PASS] Detection with moving"

# ------------------------------------------------------------
# Test 3: No oversized files scenario
# ------------------------------------------------------------
output=$($SCRIPT_PATH -d "$TMPDIR" -s 10)
if ! echo "$output" | grep -q "No files larger than 10MB"; then
  echo "[FAIL] Expected no‑oversized‑files message not shown"
  exit 1
fi

echo "[PASS] No oversized files scenario"

# All tests passed
exit 0
