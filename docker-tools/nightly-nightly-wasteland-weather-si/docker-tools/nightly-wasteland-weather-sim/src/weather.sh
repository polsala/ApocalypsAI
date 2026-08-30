#!/usr/bin/env bash
set -euo pipefail

location="${1:-Unknown}"
offset="${2:-0}"

input="${location}:${offset}"
# calculate sum of ASCII codes
sum=0
for (( i=0; i<${#input}; i++ )); do
  char="${input:i:1}"
  ascii=$(printf "%d" "'$char")
  sum=$((sum + ascii))
done

weather_options=(
  "Acid rain"
  "Radiation fog"
  "Mutant sandstorm"
  "Glowing ash"
  "Toxic thunder"
  "Cold nuclear wind"
  "Scorching plasma heat"
  "Silent dust"
)

index=$((sum % ${#weather_options[@]}))
weather="${weather_options[$index]}"

echo "Forecast for ${location} (day ${offset}): ${weather}."
