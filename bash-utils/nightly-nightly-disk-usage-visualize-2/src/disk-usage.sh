#!/usr/bin/env bash
set -euo pipefail

# Default parameters
depth=2
human=true

# Parse options
while getopts ":d:h" opt; do
  case $opt in
    d)
      depth=$OPTARG
      ;;
    h)
      human=true
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done
shift $((OPTIND-1))

target="${1:-.}"

# Build du command based on human flag
if $human; then
  du_cmd="du -h --max-depth=$depth \"$target\""
else
  du_cmd="du -b --max-depth=$depth \"$target\""
fi

# Execute du, sort by size descending, and output
eval $du_cmd | sort -hr
