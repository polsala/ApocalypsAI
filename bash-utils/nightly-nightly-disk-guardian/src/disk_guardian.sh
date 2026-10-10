#!/usr/bin/env bash
set -euo pipefail

# List of apocalyptic warnings
warnings=(
  "⚠️ The end is nigh! Disk space dwindles to %s%%."
  "🔥 Your storage is ablaze at %s%% usage!"
  "☢️ Radiation levels rising: %s%% of disk consumed."
  "❄️ Frostbite incoming! %s%% of space vanished."
  "🌪️ A whirlwind of files swallows %s%% of your disk."
)

# Function to get usage percent (integer)
get_usage() {
  if [[ -n "${DF_OUTPUT:-}" ]]; then
    echo "$DF_OUTPUT"
  else
    df -h / | awk 'NR==2 {print $5}'
  fi
}

# Main
threshold=${1:-80}
usage=$(get_usage)
usage_num=${usage%\%}
if (( usage_num > threshold )); then
  idx=$(( RANDOM % ${#warnings[@]} ))
  printf "${warnings[$idx]}\n" "$usage_num"
  exit 1
else
  echo "✅ Disk usage at $usage_num% is within safe limits."
  exit 0
fi
