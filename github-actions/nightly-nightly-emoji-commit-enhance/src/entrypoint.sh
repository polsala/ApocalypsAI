#!/usr/bin/env bash
set -euo pipefail

# Determine hour (0‑23) – use DATE_OVERRIDE if supplied (ISO‑8601), otherwise current UTC hour
if [[ -n "${DATE_OVERRIDE:-}" ]]; then
  # GNU date can parse ISO‑8601; fallback to default date if parsing fails
  hour=$(date -u -d "$DATE_OVERRIDE" +"%H" 2>/dev/null || date -u +"%H")
else
  hour=$(date -u +"%H")
fi

# Map hour to period of day
if (( hour < 12 )); then
  period="morning"
elif (( hour < 17 )); then
  period="afternoon"
elif (( hour < 21 )); then
  period="evening"
else
  period="night"
fi

# Emoji sets for each period (deterministic – first emoji is used for testing)
declare -A emojis
emojis[morning]="☀️ 🌅 🌞"
emojis[afternoon]="🌤️ 🍃 🌻"
emojis[evening]="🌆 🌙 ✨"
emojis[night]="🌌 🌟 🌙"

# Select the first emoji in the list for reproducibility
selected=$(echo "${emojis[$period]}" | awk '{print $1}')

# Output the emoji (both to stdout and to a temporary file for the composite action output)
echo "$selected"
echo "$selected" > /tmp/emoji_output
