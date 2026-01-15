#!/usr/bin/env bash
set -euo pipefail

DIR="."
NUM=10
AGE=""
DELETE=false

usage() {
  echo "Usage: $0 [-d DIR] [-n NUM] [-a AGE_DAYS] [-y]"
  exit 1
}

while getopts ":d:n:a:y" opt; do
  case $opt in
    d) DIR="$OPTARG" ;;
    n) NUM="$OPTARG" ;;
    a) AGE="$OPTARG" ;;
    y) DELETE=true ;;
    *) usage ;;
  esac
done

if [[ ! -d "$DIR" ]]; then
  echo "Error: Directory $DIR does not exist."
  exit 1
fi

echo "Scanning directory: $DIR"
echo "Top $NUM largest files:"
find "$DIR" -type f -printf "%s %p\n" | sort -rn | head -n "$NUM" | while read -r size path; do
  echo "$size $path"
 done

if [[ -n "$AGE" ]]; then
  echo "Files older than $AGE days:"
  OLD_FILES=$(find "$DIR" -type f -mtime +"$AGE" -print)
  if [[ -z "$OLD_FILES" ]]; then
    echo "  (none)"
  else
    echo "$OLD_FILES"
    if $DELETE; then
      echo "Deleting..."
      echo "$OLD_FILES" | xargs rm -f
    fi
  fi
fi
