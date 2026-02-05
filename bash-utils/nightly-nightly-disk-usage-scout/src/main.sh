#!/usr/bin/env bash
set -euo pipefail

# Default parameters
depth=1
num=10
human=false

# Parse options
while getopts "d:n:h" opt; do
  case $opt in
    d) depth=$OPTARG ;;
    n) num=$OPTARG ;;
    h) human=true ;;
    *) ;;
  esac
done
shift $((OPTIND-1))

target="${1:-.}"

# Command to invoke du; can be overridden for testing via DU_CMD
du_cmd=${DU_CMD:-du}

# Run du with appropriate flags
if $human; then
  du_output=$($du_cmd -d "$depth" -h "$target" 2>/dev/null)
else
  du_output=$($du_cmd -d "$depth" -k "$target" 2>/dev/null)
fi

# Sort by size (numeric reverse) and limit to $num lines
output=$(echo "$du_output" | sort -nr | head -n "$num")

echo "$output"
