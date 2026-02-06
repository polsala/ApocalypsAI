#!/usr/bin/env bash

set -euo pipefail

# Create a temporary workspace
TMPDIR=$(mktemp -d)
cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

# Helper to create a file of a given size (in bytes)
make_file() {
  local size=$1
  local name=$2
  truncate -s "$size" "$TMPDIR/$name"
}

# Create files of various sizes
make_file 500 small.txt               # 500 B  → 🧚
make_file $((2*1024*1024)) medium.txt  # 2 MiB → 🐉
make_file $((15*1024*1024)) large.txt  # 15 MiB → 🦖
make_file $((120*1024*1024)) huge.txt  # 120 MiB → 🐢

# Run the utility against the temporary directory
output=$(bash ../src/disk-elf-report.sh "$TMPDIR" 4)

# Verify that each expected emoji and filename appears in the output
check() {
  local pattern=$1
  if ! grep -q "$pattern" <<<"$output"; then
    echo "Test failure: expected pattern not found -> $pattern"
    exit 1
  fi
}

check "🧚"
check "🐉"
check "🦖"
check "🐢"
check "small.txt"
check "medium.txt"
check "large.txt"
check "huge.txt"

echo "All tests passed."
