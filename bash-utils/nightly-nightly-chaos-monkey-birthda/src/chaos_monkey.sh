#!/bin/bash

DIR_PATH="$1"

if [[ -z "$DIR_PATH" ]]; then
  echo "Usage: $0 <directory>"
  exit 1
fi

if [[ ! -d "$DIR_PATH" ]]; then
  echo "Error: Directory does not exist."
  exit 1
fi

# Simulate festive renaming
CHAOS_NAMES=(
  "🎉_party_hat.txt"
  "🎂_birthday_cake.log"
  "🎈_balloon_pop.sh"
  "🎊_confetti_burst.md"
  "🥳_celebration_notes.tmp"
  "🎁_surprise_box.cfg"
  "🎆_fireworks_display.yaml"
  "🍭_candy_rain.ini"
)

FILES=($(find "$DIR_PATH" -maxdepth 1 -type f | head -n 8))

for i in "${!FILES[@]}"; do
  FILE="${FILES[$i]}"
  BASE_DIR=$(dirname "$FILE")
  echo "Renaming $(basename "$FILE") to ${CHAOS_NAMES[$i]} (simulation only)"
  # Simulate rename - no actual change
  sleep 0.3
  echo "Restoring $(basename "$FILE")"
  sleep 0.2
done

echo "🎉 Chaos Monkey Birthday Prank complete! No files were harmed."
