#!/usr/bin/env bash
set -euo pipefail

# nightly-todo-prioritizer – sort a TODO list by [Px] priority tags.
# Usage: ./priority_sort.sh [path-to-todo]
# If no argument is given, defaults to ./TODO.txt in the current directory.

FILE="${1:-TODO.txt}"

if [[ ! -f "$FILE" ]]; then
  echo "Error: File not found: $FILE" >&2
  exit 1
fi

# awk prints a numeric priority (lower = higher) followed by a tab and the original line.
# Lines without a [Px] tag get priority 99 (effectively lowest).
awk '
  {
    line = $0
    if (match(line, /\[P([0-9]+)\]/, arr)) {
      pr = arr[1] + 0
    } else {
      pr = 99
    }
    print pr "\t" line
  }
' "$FILE" |
  sort -n -k1,1 |
  cut -f2-
