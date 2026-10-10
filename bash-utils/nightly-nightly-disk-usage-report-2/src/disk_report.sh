#!/usr/bin/env bash
set -euo pipefail

# Default values
COUNT=10
TARGET="."

# Parse options
while getopts ":n:" opt; do
  case $opt in
    n) COUNT=$OPTARG ;;
    \?) echo "Invalid option: -$OPTARG" >&2; exit 1 ;;
    :) echo "Option -$OPTARG requires an argument." >&2; exit 1 ;;
  esac
done
shift $((OPTIND-1))

if [[ $# -gt 0 ]]; then
  TARGET="$1"
fi

# Validate count
if ! [[ "$COUNT" =~ ^[0-9]+$ ]]; then
  echo "Count must be a positive integer" >&2
  exit 1
fi

# Generate size report, sort, and limit output
du -ah "$TARGET" 2>/dev/null | sort -rh | head -n "$COUNT"
