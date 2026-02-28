#!/usr/bin/env bash
set -euo pipefail

# Locate the utility script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
SCRIPT="$SCRIPT_DIR/main.sh"

# Create a temporary workspace
TMPDIR=$(mktemp -d)
cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

# Create sample files
touch "$TMPDIR/hello.txt"
touch "$TMPDIR/data 1.csv"

# Run encode
"$SCRIPT" encode "$TMPDIR"

# Expected emoji filenames
EXPECTED1="🇭🇪🇱🇱🇴.txt"
EXPECTED2="🇩🇦🇹🇦␣1.csv"

if [[ ! -e "$TMPDIR/$EXPECTED1" ]]; then
  echo "Missing encoded file: $EXPECTED1"
  exit 1
fi
if [[ ! -e "$TMPDIR/$EXPECTED2" ]]; then
  echo "Missing encoded file: $EXPECTED2"
  exit 1
fi

# Run decode
"$SCRIPT" decode "$TMPDIR"

if [[ ! -e "$TMPDIR/hello.txt" ]]; then
  echo "Failed to restore original file: hello.txt"
  exit 1
fi
if [[ ! -e "$TMPDIR/data 1.csv" ]]; then
  echo "Failed to restore original file: data 1.csv"
  exit 1
fi

echo "All tests passed"
