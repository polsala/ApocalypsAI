#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 -d <directory> -s <size_mb> [-m]"
  echo "  -d <directory>   Directory to scan (required)"
  echo "  -s <size_mb>     Size threshold in megabytes (required)"
  echo "  -m               Move oversized files to .trash (optional)"
  exit 1
}

# Default options
move=false

while getopts ":d:s:m" opt; do
  case $opt in
    d) dir="$OPTARG" ;;
    s) size_mb="$OPTARG" ;;
    m) move=true ;;
    *) usage ;;
  esac
done

# Validate required arguments
if [[ -z "${dir:-}" || -z "${size_mb:-}" ]]; then
  usage
fi

if [[ ! -d "$dir" ]]; then
  echo "Error: Directory '$dir' does not exist." >&2
  exit 1
fi

# Convert megabytes to bytes for comparison
threshold=$((size_mb * 1024 * 1024))
found=0

while IFS= read -r -d '' file; do
  filesize=$(stat -c%s "$file")
  if (( filesize > threshold )); then
    echo "Oversized: $file ($(numfmt --to=iec $filesize))"
    ((found++))
    if $move; then
      trash_dir="$dir/.trash"
      mkdir -p "$trash_dir"
      mv "$file" "$trash_dir/"
      echo "Moved to $trash_dir"
    fi
  fi
done < <(find "$dir" -type f -print0)

if (( found == 0 )); then
  echo "No files larger than ${size_mb}MB found in $dir."
fi
