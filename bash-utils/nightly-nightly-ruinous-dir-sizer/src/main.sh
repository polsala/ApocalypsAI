#!/usr/bin/env bash

# nightly-ruinous-dir-sizer
# Scans a directory and prints the largest entries.
# Author: ApocalypsAI Nightly Integrator
# License: MIT

set -euo pipefail

print_help() {
  cat <<'EOF'
Usage: ruinous-dir-sizer [-n <number>] [directory]

  -n <number>   Number of entries to display (default: 10). Use 0 for no limit.
  -h            Show this help message and exit.

If no directory is supplied, the current working directory is used.
EOF
}

# Default values
NUM=10
DIR="$(pwd)"

# Parse options
while getopts ":n:h" opt; do
  case $opt in
    n)
      if [[ "$OPTARG" =~ ^[0-9]+$ ]]; then
        NUM=$OPTARG
      else
        echo "Error: -n requires a non‑negative integer" >&2
        exit 1
      fi
      ;;
    h)
      print_help
      exit 0
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      print_help
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument" >&2
      print_help
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))

# Remaining argument, if any, is the directory
if [[ $# -gt 0 ]]; then
  DIR="$1"
fi

if [[ ! -d "$DIR" ]]; then
  echo "Error: '$DIR' is not a directory" >&2
  exit 1
fi

# Determine du flags based on availability (GNU coreutils vs BSD)
if du --help 2>&1 | grep -q "--bytes"; then
  DU_FLAGS="-b --max-depth=1"
else
  # BSD du does not have -b; use -k and convert later
  DU_FLAGS="-k --max-depth=1"
  CONVERT_TO_BYTES=true
fi

# Gather sizes
# shellcheck disable=SC2046
sizes=$(du $DU_FLAGS "$DIR" 2>/dev/null | sort -nr)

# If conversion needed, multiply by 1024 to get bytes
if [[ "${CONVERT_TO_BYTES:-false}" == true ]]; then
  sizes=$(echo "$sizes" | awk '{printf "%d %s\n", $1*1024, $2}')
fi

# Header
printf "Largest entries in %s:\n" "$DIR"

# Output limit handling
if [[ $NUM -eq 0 ]]; then
  limit=""
else
  limit="-n $NUM"
fi

# Print results
printf "%s\n" "$sizes" | head $limit | awk '{printf "%10d bytes\t%s\n", $1, $2}'
