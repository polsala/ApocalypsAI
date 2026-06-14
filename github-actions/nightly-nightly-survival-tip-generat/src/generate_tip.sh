#!/usr/bin/env bash
set -euo pipefail

seed="${1:-0}"
# List of whimsical survival tips
tips=(
  "Always keep a spare bottle of water in your pocket."
  "Never trust a talking cactus."
  "Learn to start a fire with two sticks and a lot of optimism."
  "Map your shelter with chalk before the dust settles."
  "Carry a deck of cards; they double as morale boosters."
  "Remember: the best weapon is a well‑timed joke."
)

len=${#tips[@]}
index=$(( seed % len ))
selected="${tips[$index]}"

# Write the output in the format expected by GitHub Actions
echo "survival_tip=${selected}" >> "$GITHUB_OUTPUT"
