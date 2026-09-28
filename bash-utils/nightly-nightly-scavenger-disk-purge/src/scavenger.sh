#!/usr/bin/env bash
set -euo pipefail

# Default parameters
DIR="/var/log"
AGE=7
DRY_RUN=0
COMPRESS=0

# Parse options
while getopts "d:a:nc" opt; do
  case $opt in
    d) DIR="$OPTARG" ;;
    a) AGE="$OPTARG" ;;
    n) DRY_RUN=1 ;;
    c) COMPRESS=1 ;;
    *) echo "Invalid option" >&2; exit 1 ;;
  esac
done

# Validate directory
if [[ ! -d "$DIR" ]]; then
  echo "Directory $DIR does not exist" >&2
  exit 1
fi

echo "🗑️ Scavenging relics older than $AGE days in $DIR..."

NOW=$(date +%s)
THRESHOLD=$((NOW - AGE*86400))

find "$DIR" -type f -not -path "*/.*" -printf "%T@ %p\n" | while read -r modtime path; do
  modint=${modtime%.*}
  if (( modint < THRESHOLD )); then
    if (( COMPRESS )); then
      if (( DRY_RUN )); then
        echo "[DRY‑RUN] Would compress $path"
      else
        gzip -9 "$path" && echo "📦 Compressed $path"
      fi
    else
      if (( DRY_RUN )); then
        echo "[DRY‑RUN] Would delete $path"
      else
        rm -f "$path" && echo "🗑️ Deleted $path"
      fi
    fi
  fi
done

exit 0
