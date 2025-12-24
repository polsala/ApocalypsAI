#!/usr/bin/env bash
set -euo pipefail

# Default configuration
DAYS=30
DRY_RUN=false
CACHE_DIR="${APT_CACHE_DIR:-/var/cache/apt/archives}"

usage() {
  echo "Usage: $0 [-d DAYS] [-n] [--cache-dir DIR]"
  echo "  -d DAYS        Delete .deb files older than DAYS (default: $DAYS)"
  echo "  -n            Dry run – only show what would be deleted"
  echo "  --cache-dir DIR  Override cache directory (default: $CACHE_DIR)"
  exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -d)
      DAYS="$2"
      shift 2
      ;;
    -n)
      DRY_RUN=true
      shift
      ;;
    --cache-dir)
      CACHE_DIR="$2"
      shift 2
      ;;
    -h|--help)
      usage
      ;;
    *)
      echo "Unknown option: $1"
      usage
      ;;
  esac
done

if [[ ! -d "$CACHE_DIR" ]]; then
  echo "Error: cache directory '$CACHE_DIR' does not exist."
  exit 1
fi

# Compute cutoff timestamp
NOW=$(date +%s)
THRESHOLD=$((NOW - DAYS * 86400))

# Find .deb files and decide whether to delete
find "$CACHE_DIR" -type f -name "*.deb" -printf "%T@ %p\n" |
while read -r modtime path; do
  # modtime is seconds since epoch with fractional part; strip fraction
  modint=${modtime%.*}
  if (( modint < THRESHOLD )); then
    if $DRY_RUN; then
      echo "Would delete: $path"
    else
      echo "Deleting: $path"
      rm -f "$path"
    fi
  fi
done
