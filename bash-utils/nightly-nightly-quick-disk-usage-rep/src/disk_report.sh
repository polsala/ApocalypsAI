#!/usr/bin/env bash

# nightly-quick-disk-usage-report
# ------------------------------------------------------------
# Scan a directory and list the N largest files/directories.
# ------------------------------------------------------------

set -euo pipefail

usage() {
    cat <<'EOF'
Usage: quick-disk-report [-d <directory>] [-n <count>] [-h]

  -d <directory>  Directory to scan (default: current directory)
  -n <count>      Number of top entries to display (default: 10)
  -h              Show this help message and exit
EOF
}

# Default values
TARGET_DIR="$(pwd)"
COUNT=10

# Parse arguments
while getopts ":d:n:h" opt; do
    case $opt in
        d) TARGET_DIR="$OPTARG" ;;
        n) COUNT="$OPTARG" ;;
        h) usage ; exit 0 ;;
        \?) echo "Invalid option: -$OPTARG" >&2 ; usage ; exit 1 ;;
        :) echo "Option -$OPTARG requires an argument." >&2 ; usage ; exit 1 ;;
    esac
done

# Ensure target directory exists
if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Directory '$TARGET_DIR' does not exist." >&2
    exit 1
fi

# Use du to get sizes in bytes; fallback to kilobytes if -b not supported
if du --bytes /dev/null >/dev/null 2>&1; then
    DU_FLAGS="--bytes --max-depth=1"
else
    DU_FLAGS="-k --max-depth=1"
fi

# Gather sizes, sort, and output top N
# Suppress errors for entries we cannot access
du $DU_FLAGS "$TARGET_DIR"/* 2>/dev/null |
    sort -rn |
    head -n "$COUNT" |
    awk '{printf "%s\t%s\n", $1, $2}'
