#!/usr/bin/env bash

# Array of whimsical quotes
quotes=(
"Keep calm and code on."
"The early bird gets the worm, but the second mouse gets the cheese."
"Debugging: Removing the needles from the haystack."
"Premature optimization is the root of all evil."
"Talk is cheap. Show me the code."
)

# Determine the seed – use SEED env var if set, otherwise current timestamp
if [[ -n "$SEED" ]]; then
  seed=$SEED
else
  seed=$(date +%s)
fi

# Compute index safely (modulo array length)
index=$(( seed % ${#quotes[@]} ))

echo "${quotes[$index]}"
