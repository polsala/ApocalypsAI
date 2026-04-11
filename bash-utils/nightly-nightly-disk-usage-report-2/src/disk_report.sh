#!/usr/bin/env bash

# nightly-disk-usage-report
# Generates a report of the largest files/directories.

set -euo pipefail

# Determine OS for du options
if du --version >/dev/null 2>&1; then
  # GNU du (Linux)
  DU_OPTS="-b"
else
  # BSD du (macOS)
  DU_OPTS="-k"
fi

TARGET_DIR="${1:-.}"
COUNT="${2:-10}"

# Validate inputs
if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Error: '$TARGET_DIR' is not a directory" >&2
  exit 1
fi
if ! [[ "$COUNT" =~ ^[0-9]+$ ]]; then
  echo "Error: count must be a positive integer" >&2
  exit 1
fi

# Header
printf "%s\t%s\n" "Size" "Path"

# Find sizes, sort, and limit
# Use du to get size of each file/directory (non‑recursive for files, recursive for dirs)
# Exclude the report script itself to avoid self‑inflation
find "$TARGET_DIR" -mindepth 1 -maxdepth 1 ! -path "$(realpath "$0")" -print0 |
  xargs -0 du $DU_OPTS 2>/dev/null |
  sort -rn |
  head -n "$COUNT" |
  while IFS=$'\t' read -r size path; do
    # Convert size to human readable
    if [[ "$DU_OPTS" == "-b" ]]; then
      # size in bytes
      hr=$(numfmt --to=iec-i --suffix=B "$size" 2>/dev/null || echo "${size}B")
    else
      # size in kilobytes, convert to KiB
      hr=$(numfmt --to=iec-i --suffix=K "$((size*1024))" 2>/dev/null || echo "${size}K")
    fi
    printf "%s\t%s\n" "$hr" "$path"
  done
