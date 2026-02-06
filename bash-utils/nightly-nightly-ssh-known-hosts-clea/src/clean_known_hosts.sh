#!/usr/bin/env bash
set -euo pipefail

# Default values
dry_run=false
file="${HOME}/.ssh/known_hosts"

# Parse arguments
while (( "$#" )); do
  case "$1" in
    --dry-run)
      dry_run=true
      shift
      ;;
    *)
      file="$1"
      shift
      ;;
  esac
done

if [[ ! -f "$file" ]]; then
  echo "File not found: $file" >&2
  exit 1
fi

# Count total lines
total=$(wc -l < "$file")
# Create a temporary file with unique lines preserving order
tmp=$(mktemp)
awk '!seen[$0]++' "$file" > "$tmp"
unique=$(wc -l < "$tmp")
removed=$((total - unique))

if (( removed == 0 )); then
  echo "No duplicate entries found in $file."
  rm "$tmp"
  exit 0
fi

if $dry_run; then
  echo "Dry run: $removed duplicate entries would be removed from $file."
  rm "$tmp"
  exit 0
fi

# Replace original file with deduped version
mv "$tmp" "$file"
echo "Removed $removed duplicate entries from $file."
