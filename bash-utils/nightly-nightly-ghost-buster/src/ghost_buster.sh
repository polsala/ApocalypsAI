#!/usr/bin/env bash
set -euo pipefail

# Default values
DIR="."
DELETE=false

# Argument parsing
while [[ $# -gt 0 ]]; do
  case "$1" in
    -d|--directory)
      if [[ -z "${2-}" ]]; then
        echo "Error: --directory requires a path" >&2
        exit 1
      fi
      DIR="$2"
      shift 2
      ;;
    --delete)
      DELETE=true
      shift
      ;;
    -h|--help)
      echo "Usage: $0 [-d DIRECTORY] [--delete]"
      echo "  -d, --directory PATH   Directory to scan (default: .)"
      echo "  --delete               Delete discovered zero‑byte files"
      echo "  -h, --help             Show this help message"
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

# Validate directory
if [[ ! -d "$DIR" ]]; then
  echo "Error: Directory not found: $DIR" >&2
  exit 1
fi

# Find zero‑byte regular files (ghosts)
mapfile -t GHOSTS < <(find "$DIR" -type f -size 0 2>/dev/null || true)
COUNT=${#GHOSTS[@]}

if $DELETE; then
  for f in "${GHOSTS[@]}"; do
    rm -f "$f"
  done
  ACTION="deleted"
else
  ACTION="found"
fi

# Emit JSON summary (single line)
printf '{"directory":"%s","action":"%s","ghost_count":%d}\n' "$DIR" "$ACTION" "$COUNT"
