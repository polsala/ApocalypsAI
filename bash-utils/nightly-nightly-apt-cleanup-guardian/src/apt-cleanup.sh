#!/usr/bin/env bash
# nightly-apt-cleanup-guardian
# Removes stale .deb files from the APT cache with optional dry‑run.
# Apocalypse‑themed messages for extra flavor.

set -euo pipefail

# Default values
KEEP_DAYS=30
DRY_RUN=false
CACHE_DIR="${APT_CACHE_DIR:-/var/cache/apt/archives}"

print_help() {
  cat <<'EOF'
Usage: apt-cleanup.sh [OPTIONS]

Options:
  --keep-days=N   Keep files newer than N days (default: 30)
  --dry-run       Show what would be deleted without removing anything
  -h, --help      Show this help message
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --keep-days=*)
      KEEP_DAYS="${1#*=}"
      ;;
    --dry-run)
      DRY_RUN=true
      ;;
    -h|--help)
      print_help
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      print_help
      exit 1
      ;;
  esac
  shift
done

if [[ ! -d "$CACHE_DIR" ]]; then
  echo "Cache directory not found: $CACHE_DIR" >&2
  exit 2
fi

# Find stale .deb files
STALE_FILES=$(find "$CACHE_DIR" -type f -name "*.deb" -mtime +"$KEEP_DAYS" -print)

if [[ -z "$STALE_FILES" ]]; then
  echo "🛡️  The cache is already pristine. No files older than $KEEP_DAYS days."
  exit 0
fi

if $DRY_RUN; then
  echo "🔮 Dry run – the following files would be purged (older than $KEEP_DAYS days):"
  echo "$STALE_FILES"
  exit 0
fi

echo "⚔️  Commencing purge of stale packages (older than $KEEP_DAYS days)..."
while IFS= read -r file; do
  echo "🗑️  Deleting $file"
  rm -f "$file"
 done <<< "$STALE_FILES"

echo "✅ Purge complete."
