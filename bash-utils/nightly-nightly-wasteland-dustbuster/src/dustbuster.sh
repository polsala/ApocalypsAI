#!/usr/bin/env bash
set -euo pipefail

# Default values
PATH_DIR="/var/log"
DAYS=7
DRY_RUN=false

usage() {
  cat <<'EOF'
Usage: dustbuster.sh [-p <path>] [-d <days>] [-n] [-h]

Options:
  -p <path>   Directory to scan (default: /var/log)
  -d <days>   Minimum file age in days (default: 7)
  -n          Dry‑run mode – only show what would be done
  -h          Show this help message
EOF
}

# Parse arguments
while getopts ":p:d:nh" opt; do
  case $opt in
    p) PATH_DIR="$OPTARG" ;;
    d) DAYS="$OPTARG" ;;
    n) DRY_RUN=true ;;
    h) usage; exit 0 ;;
    \?) echo "Invalid option: -$OPTARG" >&2; usage; exit 1 ;;
    :) echo "Option -$OPTARG requires an argument." >&2; usage; exit 1 ;;
  esac
done

# Verify directory exists
if [[ ! -d "$PATH_DIR" ]]; then
  echo "Error: Directory '$PATH_DIR' does not exist." >&2
  exit 1
fi

# Find and process files
find "$PATH_DIR" -type f -mtime +"$DAYS" -print0 |
while IFS= read -r -d '' file; do
  if $DRY_RUN; then
    echo "Would compress: $file"
  else
    gzip -9 "$file"
    echo "Compressed: $file"
  fi
done
