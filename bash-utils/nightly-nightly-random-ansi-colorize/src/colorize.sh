#!/usr/bin/env bash
# nightly-random-ansi-colorizer
# Prints input text in a random ANSI color.

# Read input
if [[ -n "$1" ]]; then
  text="$*"
else
  # Read from stdin
  text="$(cat)"
fi

# Define color codes
colors=(31 32 33 34 35 36)

# Select random color
idx=$((RANDOM % ${#colors[@]}))
color=${colors[$idx]}

# Output colored text
echo -e "\e[${color}m${text}\e[0m"
