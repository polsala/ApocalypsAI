#!/bin/sh
# whimsical messages array
messages=(
  "🌪️ The winds whisper: 'Remember to water your cactus.'"
  "☢️ Radiation level: low. Your coffee is safe."
  "🦖 Dino-saurus says: 'Don't forget to stretch.'"
  "🔋 Battery low? Charge your optimism."
)
# pick random
idx=$((RANDOM % ${#messages[@]}))
echo "${messages[$idx]}"
