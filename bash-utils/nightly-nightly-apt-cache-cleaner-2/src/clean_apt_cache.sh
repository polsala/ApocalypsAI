#!/usr/bin/env bash
set -euo pipefail

# Default configuration
DAYS=30
DRY_RUN=true
CACHE_DIR="${APT_CACHE_DIR:-/var/cache/apt/archives}"

# Argument parsing
while [[ $# -gt 0 ]]; do
  case "$1" in
    --days)
      DAYS="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --no-dry-run)
      DRY_RUN=false
      shift
      ;;
    --cache-dir)
      CACHE_DIR="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

if [[ ! -d "$CACHE_DIR" ]]; then
  echo "Cache directory $CACHE_DIR does not exist." >&2
  exit 1
fi

# Find .deb files older than the specified number of days
OLD_FILES=$(find "$CACHE_DIR" -type f -name "*.deb" -mtime +"$DAYS")
if [[ -z "$OLD_FILES" ]]; then
  echo "No .deb files older than $DAYS days found in $CACHE_DIR."
  exit 0
fi

echo "Found $(echo "$OLD_FILES" | wc -l) old .deb file(s) in $CACHE_DIR:"
printf "%s\n" $OLD_FILES

if $DRY_RUN; then
  echo "Dry run enabled – no files will be deleted."
else
  echo "Deleting files..."
  # Mock rationale: In a real environment we would delete; here we simply remove them.
  rm -f $OLD_FILES
  echo "Deletion complete."
fi
