#!/usr/bin/env bash
set -euo pipefail

# Default values
DRY_RUN=false
DAYS=30
CACHE_DIR="${APT_CACHE_DIR:-/var/cache/apt/archives}"

usage() {
  echo "Usage: $0 [-d] [-n DAYS]"
  echo "  -d        Dry run (list files to be removed without deleting)"
  echo "  -n DAYS   Number of days to keep packages (default: 30)"
  exit 1
}

# Parse options
while getopts ":dn:" opt; do
  case $opt in
    d) DRY_RUN=true ;;
    n) DAYS=$OPTARG ;;
    *) usage ;;
  esac
done

# Validate DAYS is a positive integer
if ! [[ "$DAYS" =~ ^[0-9]+$ ]]; then
  echo "Error: DAYS must be a positive integer."
  usage
fi

# Find .deb files older than $DAYS
if ! command -v find >/dev/null; then
  echo "Error: 'find' command not available."
  exit 1
fi

OLD_FILES=$(find "$CACHE_DIR" -type f -name "*.deb" -mtime +"$DAYS" 2>/dev/null || true)

if [[ -z "$OLD_FILES" ]]; then
  echo "No .deb files older than $DAYS days found in $CACHE_DIR."
  exit 0
fi

if $DRY_RUN; then
  echo "Dry run: the following .deb files would be removed (older than $DAYS days):"
  echo "$OLD_FILES"
else
  echo "Removing .deb files older than $DAYS days from $CACHE_DIR:"
  echo "$OLD_FILES"
  # Delete files
  echo "$OLD_FILES" | xargs -d '\n' rm -f --
  echo "Deletion complete."
fi
