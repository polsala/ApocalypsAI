#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: create temporary directory with files of known sizes
TMPDIR=$(mktemp -d)
cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

# Create a small file (1 KB) and a large file (15 MB)
dd if=/dev/zero of="$TMPDIR/small.txt" bs=1024 count=1 status=none
dd if=/dev/zero of="$TMPDIR/large.txt" bs=1M count=15 status=none

# Resolve script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
SCRIPT="$SCRIPT_DIR/arcane-archive.sh"

# ---------- Dry‑run test ----------
output=$("$SCRIPT" -t 10M "$TMPDIR")
if [[ "$output" != *"large.txt"* ]]; then
  echo "FAIL: Expected large.txt to appear in dry‑run output"
  exit 1
fi
# Ensure the large file still exists
if [ ! -f "$TMPDIR/large.txt" ]; then
  echo "FAIL: large.txt should not be moved during dry‑run"
  exit 1
fi

# ---------- Move mode test ----------
"$SCRIPT" -t 10M -m "$TMPDIR"
# After moving, the large file should reside in the archive directory
if [ ! -f "$TMPDIR/archive/large.txt" ]; then
  echo "FAIL: large.txt was not moved to archive"
  exit 1
fi
# Small file must remain untouched
if [ ! -f "$TMPDIR/small.txt" ]; then
  echo "FAIL: small.txt disappeared unexpectedly"
  exit 1
fi

echo "All tests passed."
