#!/usr/bin/env bash
set -euo pipefail

DIR="."
TOP=5
ARCHIVE_DAYS=""
ARCHIVE_THRESHOLD=$((10*1024*1024)) # 10 MiB in bytes
ARCHIVE_NAME="archive.tar.gz"

usage() {
  echo "Usage: $0 [-d DIR] [-n N] [-a DAYS]"
  exit 1
}

while getopts ":d:n:a:" opt; do
  case $opt in
    d) DIR="$OPTARG" ;;
    n) TOP="$OPTARG" ;;
    a) ARCHIVE_DAYS="$OPTARG" ;;
    *) usage ;;
  esac
done

if [[ ! -d "$DIR" ]]; then
  echo "Error: Directory $DIR does not exist."
  exit 1
fi

echo "Scanning directory: $DIR"
echo "Top $TOP largest entries:"
du -ah "$DIR" 2>/dev/null | sort -rh | head -n "$TOP"

if [[ -n "$ARCHIVE_DAYS" ]]; then
  echo "Archiving files older than $ARCHIVE_DAYS days and larger than 10MiB..."
  mapfile -t files < <(find "$DIR" -type f -size +$((ARCHIVE_THRESHOLD/1024))k -mtime +"$ARCHIVE_DAYS" 2>/dev/null)
  if [[ ${#files[@]} -eq 0 ]]; then
    echo "No files meet the criteria."
  else
    tar -czf "$ARCHIVE_NAME" "${files[@]}"
    echo "Created archive $ARCHIVE_NAME containing ${#files[@]} files."
  fi
fi
