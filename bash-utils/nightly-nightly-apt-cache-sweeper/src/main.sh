#!/usr/bin/env bash
set -euo pipefail

# Default number of days to consider a package stale
DAYS=30
# By default we only list (dry‑run)
DRY_RUN=true
# Allow overriding the cache directory for testing
CACHE_DIR="${APT_CACHE_DIR:-/var/cache/apt/archives}"

usage() {
  echo "Usage: $0 [-d days] [--delete]"
  exit 1
}

while (( "$#" )); do
  case "$1" in
    -d|--days)
      DAYS="$2"
      shift 2
      ;;
    --delete)
      DRY_RUN=false
      shift
      ;;
    -h|--help)
      usage
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      ;;
  esac
done

if [[ ! -d "$CACHE_DIR" ]]; then
  echo "Cache directory $CACHE_DIR does not exist." >&2
  exit 1
fi

NOW=$(date +%s)
THRESHOLD=$(( NOW - DAYS*24*60*60 ))

echo "Scanning $CACHE_DIR for .deb files older than $DAYS day(s)..."

OLD_FILES=()
while IFS= read -r -d '' file; do
  MOD=$(stat -c %Y "$file")
  if (( MOD < THRESHOLD )); then
    OLD_FILES+=("$file")
  fi
done < <(find "$CACHE_DIR" -type f -name "*.deb" -print0)

if (( ${#OLD_FILES[@]} == 0 )); then
  echo "No stale packages found. Your cache is as fresh as a desert sunrise."
  exit 0
fi

echo "Found ${#OLD_FILES[@]} stale package(s):"
for f in "${OLD_FILES[@]}"; do
  echo "  $f"
done

if $DRY_RUN; then
  echo "Dry run mode – no files were deleted. Use --delete to purge."
else
  echo "Deleting stale packages..."
  for f in "${OLD_FILES[@]}"; do
    rm -f "$f"
    echo "Deleted $f"
  done
  echo "Purge complete."
fi
