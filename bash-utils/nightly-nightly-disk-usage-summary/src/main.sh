#!/usr/bin/env bash
set -euo pipefail

# Default values
DIR=\"${1:-.}\"
TOP=\"${2:-10}\"

# Check if directory exists
if [[ ! -d \"$DIR\" ]]; then
  echo \"Error: Directory '$DIR' does not exist.\" >&2
  exit 1
fi

# Use du to get sizes, sort, and output top N
du -sh \"$DIR\"/* 2>/dev/null | sort -hr | head -n \"$TOP\"
