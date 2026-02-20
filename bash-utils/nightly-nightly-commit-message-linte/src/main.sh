#!/usr/bin/env bash
set -euo pipefail

# Read commit message either from a file argument or stdin
input="${1:-}"
if [[ -n "$input" ]]; then
  mapfile -t lines < "$input"
else
  mapfile -t lines
fi

if (( ${#lines[@]} == 0 )); then
  echo "Empty commit message"
  exit 1
fi

subject="${lines[0]}"
subject_trimmed="$(echo "$subject" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"

errors=0

# Subject length (≤ 50 chars)
if (( ${#subject_trimmed} > 50 )); then
  echo "Subject line exceeds 50 characters"
  errors=$((errors+1))
fi

# Capital letter at start
first_char="${subject_trimmed:0:1}"
if [[ ! "$first_char" =~ [A-Z] ]]; then
  echo "Subject line must start with a capital letter"
  errors=$((errors+1))
fi

# No trailing period
if [[ "$subject_trimmed" =~ \.$ ]]; then
  echo "Subject line must not end with a period"
  errors=$((errors+1))
fi

# Body lines length (≤ 72 chars)
if (( ${#lines[@]} > 1 )); then
  for ((i=1; i<${#lines[@]}; i++)); do
    line="${lines[i]}"
    line_trimmed="$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
    if (( ${#line_trimmed} > 72 )); then
      echo "Body line $((i)) exceeds 72 characters"
      errors=$((errors+1))
    fi
  done
fi

# Issue reference detection (e.g., #123)
if ! grep -qE '#[0-9]+' <<< "${lines[*]}"; then
  echo "No issue reference (e.g., #123) found"
  errors=$((errors+1))
fi

exit $errors
