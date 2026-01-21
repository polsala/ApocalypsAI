#!/usr/bin/env bash

# nightly-apt-cleanup-helper
# Whimsical APT cleanup script with apocalyptic messaging.

set -euo pipefail

# Default values
FILE="apt-autoremove-list.txt"
DRY_RUN=false
ACTION="list"

print_help() {
  cat <<'EOF'
Usage: cleanup.sh [OPTIONS]

Options:
  --list                 List packages that would be removed (default action).
  --clean                Actually purge the listed packages.
  --dry-run              Show commands without executing them.
  --file <path>          Path to a file containing package names (one per line).
  -h, --help             Show this help message.
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --list)
      ACTION="list"
      shift
      ;;
    --clean)
      ACTION="clean"
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --file)
      if [[ -z "${2-}" ]]; then
        echo "Error: --file requires a path argument" >&2
        exit 1
      fi
      FILE="$2"
      shift 2
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
done

if [[ ! -f "$FILE" ]]; then
  echo "Error: Package list file '$FILE' not found." >&2
  exit 1
fi

PACKAGES=$(tr '\n' ' ' < "$FILE" | xargs)

if [[ -z "$PACKAGES" ]]; then
  echo "No packages to process. The apocalypse can wait..."
  exit 0
fi

case "$ACTION" in
  list)
    echo "🗑️  The following packages are slated for removal (the end is near):"
    echo "$PACKAGES"
    ;;
  clean)
    if $DRY_RUN; then
      echo "🤖 Dry‑run mode: would execute -> sudo apt-get purge -y $PACKAGES"
    else
      echo "⚔️  Purging packages..."
      sudo apt-get purge -y $PACKAGES
      echo "✅  Purge complete. The system is a little cleaner for the coming doom."
    fi
    ;;
  *)
    echo "Invalid action: $ACTION" >&2
    exit 1
    ;;
esac
