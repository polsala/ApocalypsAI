#!/usr/bin/env bash

# Array of whimsical quotes
quotes=(
"Keep calm and code on."
"The only bug is the one you didn't fix."
"May your commits be small and your merges be clean."
"Debugging: where you become a detective in your own code."
"Version control: because time travel is hard."
)

# Determine which index to use
if [[ -n "$QUOTE_INDEX" ]]; then
  idx=$QUOTE_INDEX
else
  idx=$((RANDOM % ${#quotes[@]}))
fi

# Guard against out‑of‑range values
if (( idx < 0 || idx >= ${#quotes[@]} )); then
  idx=0
fi

# Output the selected quote
echo "${quotes[$idx]}"
