#!/usr/bin/env bash

# Mock rationale: We invoke the script with explicit hour arguments to avoid dependence on the system clock.
# The script should output the correct clock emoji for each hour.

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
SCRIPT="$SCRIPT_DIR/src/emoji_clock.sh"

declare -A expected=(
  [1]="🕐"
  [2]="🕑"
  [3]="🕒"
  [4]="🕓"
  [5]="🕔"
  [6]="🕕"
  [7]="🕖"
  [8]="🕗"
  [9]="🕘"
  [10]="🕙"
  [11]="🕚"
  [12]="🕛"
)

for hour in "${!expected[@]}"; do
  output=$($SCRIPT $hour)
  if [[ "$output" != "${expected[$hour]}" ]]; then
    echo "Test failed for hour $hour: expected ${expected[$hour]}, got $output"
    exit 1
  fi
done

echo "All tests passed."
