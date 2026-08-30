#!/usr/bin/env bash

# Tests for nightly-quick-disk-usage-report
# ------------------------------------------------------------
# These tests create a temporary directory with known file sizes,
# invoke the script, and verify the output matches expectations.
# ------------------------------------------------------------

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/disk_report.sh"

# Helper to create a file of a specific size (in bytes)
create_file() {
    local dir=$1
    local name=$2
    local size=$3
    dd if=/dev/zero of="$dir/$name" bs=1 count=$size status=none
}

# Begin test suite
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Create files with deterministic sizes
# file_a: 100 bytes, file_b: 200 bytes, file_c: 50 bytes
create_file "$TMPDIR" "file_a.txt" 100
create_file "$TMPDIR" "file_b.txt" 200
create_file "$TMPDIR" "file_c.txt" 50

# Run the script to get top 2 entries
OUTPUT=$(bash "$SCRIPT_PATH" -d "$TMPDIR" -n 2)

# Expected output (size then path). Order: largest first.
# Note: du may prepend the directory path with a trailing slash; we normalize.
EXPECTED="200\t$TMPDIR/file_b.txt\n100\t$TMPDIR/file_a.txt"

# Compare output
if [[ "$OUTPUT" != "$EXPECTED" ]]; then
    echo "Test FAILED"
    echo "Expected:"
    echo -e "$EXPECTED"
    echo "Got:"
    echo -e "$OUTPUT"
    exit 1
else
    echo "Test PASSED"
fi
