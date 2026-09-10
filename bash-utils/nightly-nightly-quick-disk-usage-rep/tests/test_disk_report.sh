#!/usr/bin/env bash
set -euo pipefail

# Load the utility script (functions are sourced, not executed)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
source "$SCRIPT_DIR/disk_report.sh"

# Simple assertion helper
assert_eq() {
  local expected="$1"
  local actual="$2"
  local msg="${3:-}"
  if [[ "$expected" != "$actual" ]]; then
    echo "FAIL: $msg Expected '$expected' but got '$actual'" >&2
    exit 1
  fi
}

# Create a temporary workspace
TMPDIR=$(mktemp -d)
cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

# Populate with files of known size (1 KB and 2 KB)
dd if=/dev/zero of="$TMPDIR/file1.bin" bs=1 count=1024 status=none
dd if=/dev/zero of="$TMPDIR/file2.bin" bs=1 count=2048 status=none

# Expected total size = 3072 bytes
EXPECTED_SIZE=3072

# Run the script and capture its output
OUTPUT=$(bash "$SCRIPT_DIR/disk_report.sh" "$TMPDIR")
HUMAN_LINE=$(echo "$OUTPUT" | head -n1)
JSON_LINE=$(echo "$OUTPUT" | tail -n1)

# Verify the human‑readable line
assert_eq "Size: 3.00 KiB (3072 bytes)" "$HUMAN_LINE" "Human‑readable output"

# Extract size_bytes from the JSON line (simple grep/awk, no jq needed)
SIZE_BYTES=$(echo "$JSON_LINE" | grep -o '"size_bytes":[0-9]*' | cut -d: -f2)
assert_eq "$EXPECTED_SIZE" "$SIZE_BYTES" "JSON size_bytes field"

# Verify that the script respects the threshold argument (no output when below)
NO_OUTPUT=$(bash "$SCRIPT_DIR/disk_report.sh" "$TMPDIR" 5000 || true)
if [[ -n "$NO_OUTPUT" ]]; then
  echo "FAIL: Expected no output when size below threshold" >&2
  exit 1
fi

echo "All tests passed."
