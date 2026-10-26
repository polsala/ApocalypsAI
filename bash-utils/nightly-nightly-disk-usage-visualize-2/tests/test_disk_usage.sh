#!/usr/bin/env bash
set -euo pipefail

# Locate the script under src/
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
SCRIPT="$SCRIPT_DIR/disk-usage.sh"

# Create a temporary workspace
TMP_DIR=$(mktemp -d)
cleanup() { rm -rf "$TMP_DIR"; }
trap cleanup EXIT

# Mock file system (deterministic sizes)
# tiny.txt – 5 bytes
echo "tiny" > "$TMP_DIR/tiny.txt"
# big.bin – 20 KiB
dd if=/dev/zero of="$TMP_DIR/big.bin" bs=1K count=20 status=none

# Run the utility (depth 1, human‑readable)
OUTPUT="$($SCRIPT -d 1 "$TMP_DIR")"

# Extract the first two lines for verification
FIRST_LINE=$(echo "$OUTPUT" | head -n1)
SECOND_LINE=$(echo "$OUTPUT" | head -n2 | tail -n1)

# Verify that the largest entry (big.bin) appears first with a size >=20K
if [[ "$FIRST_LINE" != *"20K"* && "$FIRST_LINE" != *"20.0K"* ]]; then
  echo "Test failed: expected first line to contain 20K, got '$FIRST_LINE'" >&2
  exit 1
fi

# Verify that the second entry corresponds to tiny.txt
if [[ "$SECOND_LINE" != *"tiny.txt"* ]]; then
  echo "Test failed: expected second line to reference tiny.txt, got '$SECOND_LINE'" >&2
  exit 1
fi

echo "All tests passed"
