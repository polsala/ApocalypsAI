#!/usr/bin/env bash

# nightly-disk-emoji-report
# Generates an emoji‑based disk usage summary.
# If the environment variable MOCK_DF is set, its value is used instead of calling df.

# Function to obtain df output (real or mocked)
get_df() {
  if [[ -n "$MOCK_DF" ]]; then
    echo -e "$MOCK_DF"
  else
    df -h "$1"
  fi
}

TARGET="${1:-.}"
# Capture the second line of df output (the line for the target filesystem)
output=$(get_df "$TARGET" | awk 'NR==2 {print $5,$6}')
usage=$(echo "$output" | awk '{print $1}' | tr -d '%')
mount=$(echo "$output" | awk '{print $2}')

if (( usage <= 50 )); then
  emoji="🟢"
elif (( usage <= 80 )); then
  emoji="🟡"
else
  emoji="🔴"
fi

echo "$emoji $usage% $mount"
