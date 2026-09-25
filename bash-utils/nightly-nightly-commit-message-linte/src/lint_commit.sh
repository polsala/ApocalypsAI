#!/usr/bin/env bash

set -euo pipefail

# Read commit message from stdin or a file argument
if [[ $# -gt 0 ]]; then
  msg_file="$1"
else
  msg_file="/dev/stdin"
fi

# Load the message into an array, one line per element
mapfile -t lines < "$msg_file"

subject="${lines[0]:-}"
errors=0

report() {
  echo "Error: $1" >&2
  errors=$((errors+1))
}

# ----- Subject checks -----
if [[ ${#subject} -gt 50 ]]; then
  report "Subject line exceeds 50 characters (${#subject})"
fi

if [[ ! "$subject" =~ ^[A-Z] ]]; then
  report "Subject line should start with a capital letter"
fi

if [[ "$subject" =~ \.$ ]]; then
  report "Subject line should not end with a period"
fi

# ----- Body checks -----
# Skip the blank line that usually separates subject from body
for ((i=1; i<${#lines[@]}; i++)); do
  line="${lines[i]}"
  if [[ $i -eq 1 && -z "$line" ]]; then
    continue
  fi
  # Trailing whitespace
  if [[ "$line" =~ [[:space:]]$ ]]; then
    report "Line $((i+1)) has trailing whitespace"
  fi
  # Length limit
  if [[ ${#line} -gt 72 ]]; then
    report "Line $((i+1)) exceeds 72 characters (${#line})"
  fi
done

if [[ $errors -eq 0 ]]; then
  echo "Commit message looks good."
  exit 0
else
  exit 1
fi
