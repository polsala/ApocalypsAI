#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 [-c] -d DIRECTORY -s SIZE_MB"
  echo "  -c  Compress found files (default: just list)"
  echo "  -d  Target directory to scan"
  echo "  -s  Size threshold in megabytes"
  exit 1
}

compress=false
while getopts ":cd:s:" opt; do
  case $opt in
    c) compress=true ;;
    d) dir=$OPTARG ;;
    s) size=$OPTARG ;;
    *) usage ;;
  esac
done

if [[ -z "${dir:-}" || -z "${size:-}" ]]; then
  usage
fi

if [[ ! -d "$dir" ]]; then
  echo "Error: $dir is not a directory" >&2
  exit 1
fi

# Find files larger than the specified size (in MiB)
mapfile -t files < <(find "$dir" -type f -size "+${size}M" 2>/dev/null)

if [[ ${#files[@]} -eq 0 ]]; then
  echo "No files larger than ${size}M found in $dir."
  exit 0
fi

if $compress; then
  for f in "${files[@]}"; do
    gzip -c "$f" > "${f}.gz"
    echo "Compressed $f -> ${f}.gz"
  done
else
  echo "Found ${#files[@]} file(s) larger than ${size}M:"
  for f in "${files[@]}"; do
    echo "$f"
  done
fi
