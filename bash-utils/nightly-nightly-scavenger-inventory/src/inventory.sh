#!/usr/bin/env bash
set -euo pipefail

# Read all non‑empty lines from stdin
declare -a lines
while IFS= read -r line; do
  [[ -z "$line" ]] && continue
  lines+=("$line")
done

total=0
output="Scavenger Inventory:"
for entry in "${lines[@]}"; do
  read -r name weight qty <<<"$entry"
  # Calculate weight contribution with two‑decimal precision
  contrib=$(awk "BEGIN {printf \"%.2f\", $weight * $qty}")
  total=$(awk "BEGIN {printf \"%.2f\", $total + $contrib}")
  output+=$'\n'"- $name x$qty ($weight each) = $contrib"
done

# Determine survival rating based on total weight
if (( $(awk "BEGIN {print ($total < 20)}") )); then
  rating="Feeble"
elif (( $(awk "BEGIN {print ($total <= 50)}") )); then
  rating="Sturdy"
else
  rating="Titanic"
fi

output+=$'\n'"Total weight: $total units"
output+=$'\n'"Survival rating: $rating"

printf "%s\n" "$output"
