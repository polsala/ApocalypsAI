#!/bin/sh
# List of whimsical mixed quotes
quotes=(
"Rise like the sun, even if the world ends in ash."
"Hope is a candle in the storm of oblivion."
"Dream big, because the apocalypse loves ambition."
"Stay calm and carry a spare bunker."
"Embrace the chaos; it makes the coffee taste better."
)

# Determine index
if [ -n "$QUOTE_INDEX" ]; then
  idx=$QUOTE_INDEX
else
  idx=$(( RANDOM % ${#quotes[@]} ))
fi

echo "${quotes[$idx]}"
