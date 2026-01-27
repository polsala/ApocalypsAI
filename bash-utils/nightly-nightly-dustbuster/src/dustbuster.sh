#!/usr/bin/env bash
set -euo pipefail

# Default values
DIR="."
DRY_RUN=true

while getopts ":d:cr" opt; do
  case $opt in
    d) DIR="$OPTARG" ;;
    c) DRY_RUN=false ;;
    r) DRY_RUN=true ;;
    *) echo "Invalid option: -$OPTARG" >&2; exit 1 ;;
  esac
done

# Find junk files and directories
mapfile -d '' -t MATCHES < <(find "$DIR" \( -name "*.tmp" -o -name "*.log" -o -name "__pycache__" -o -name ".cache" -o -name "node_modules" \) -print0)

if [[ ${#MATCHES[@]} -eq 0 ]]; then
  echo "No junk files or directories found in $DIR."
  exit 0
fi

TOTAL_SIZE=0
for p in "${MATCHES[@]}"; do
  if [[ -d "$p" ]]; then
    size=$(du -sh "$p" | cut -f1)
    echo "DIR  $size  $p"
    bytes=$(du -sb "$p" | cut -f1)
  else
    size=$(du -h "$p" | cut -f1)
    echo "FILE $size  $p"
    bytes=$(du -b "$p" | cut -f1)
  fi
  TOTAL_SIZE=$((TOTAL_SIZE + bytes))
 done

human=$(numfmt --to=iec-i --suffix=B "$TOTAL_SIZE" 2>/dev/null || echo "${TOTAL_SIZE}B")
echo "Total junk size: $human"

if $DRY_RUN; then
  echo "Dry‑run mode: no files were deleted."
  exit 0
fi

read -p "Delete all listed items? [y/N] " answer
if [[ "$answer" != "y" && "$answer" != "Y" ]]; then
  echo "Aborted."
  exit 0
fi

for p in "${MATCHES[@]}"; do
  rm -rf "$p"
 done
echo "Deleted ${#MATCHES[@]} items."
