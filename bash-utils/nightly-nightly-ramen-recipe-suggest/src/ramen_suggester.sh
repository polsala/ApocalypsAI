#!/usr/bin/env bash

# nightly-ramen-recipe-suggester
# ------------------------------------------------------------
# Determines a ramen recipe based on system load.
# If a numeric argument is supplied, it is used as the load value
# (useful for testing). Otherwise the script reads /proc/loadavg.
# ------------------------------------------------------------

# Exit on any error
set -e

# Function to obtain load average
get_load() {
  if [[ -n "$1" ]]; then
    echo "$1"
  else
    if [[ -f /proc/loadavg ]]; then
      awk '{print $1}' /proc/loadavg
    else
      echo "Cannot determine load average (no /proc/loadavg)." >&2
      exit 1
    fi
  fi
}

raw_load=$(get_load "$1")
# Ensure we have a numeric value
if ! [[ "$raw_load" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
  echo "Invalid load value: $raw_load" >&2
  exit 1
fi

# Determine spice level using bc for floating‑point comparison
if (( $(echo "$raw_load < 0.5" | bc -l) )); then
  level="Mild"
elif (( $(echo "$raw_load < 1.5" | bc -l) )); then
  level="Medium"
else
  level="Spicy"
fi

# Associate recipes with each level (requires Bash 4+)
declare -A recipes
recipes["Mild"]="Shoyu Ramen – classic soy sauce broth with chicken, bamboo shoots, and soft boiled egg."
recipes["Medium"]="Miso Ramen – hearty miso broth with pork belly, corn, and butter."
recipes["Spicy"]="Spicy Tantanmen – creamy sesame broth with chili oil, ground pork, and bok choy."

# Output
echo "Current load: $raw_load"
echo "Suggested ramen level: $level"
echo "Recipe: ${recipes[$level]}"
