#!/usr/bin/env bash

# nightly-disk-guardian
# Watches disk usage and prints a whimsical warning when usage exceeds a threshold.

# Default values
PATH_TO_CHECK="/"
THRESHOLD=80
MESSAGE_FILE=""

# Parse arguments
while getopts ":p:t:m:" opt; do
  case $opt in
    p) PATH_TO_CHECK="$OPTARG" ;;
    t) THRESHOLD="$OPTARG" ;;
    m) MESSAGE_FILE="$OPTARG" ;;
    \?) echo "Invalid option: -$OPTARG" >&2; exit 1 ;;
    :) echo "Option -$OPTARG requires an argument." >&2; exit 1 ;;
  esac
done

# Function to pick a random message
pick_message() {
  if [[ -n "$MESSAGE_FILE" && -f "$MESSAGE_FILE" ]]; then
    mapfile -t msgs < "$MESSAGE_FILE"
    if (( ${#msgs[@]} > 0 )); then
      echo "${msgs[RANDOM % ${#msgs[@]}]}"
      return
    fi
  fi
  # Default whimsical messages
  local defaults=(
    "Time to clean up those old memes!"
    "Your disk is feeling a little cramped."
    "Make space, make peace."
    "Your files are staging a rebellion!"
    "A tidy disk is a happy disk."
  )
  echo "${defaults[RANDOM % ${#defaults[@]}]}"
}

# Obtain df output – allow mock via DF_MOCK env var for testing
if [[ -n "$DF_MOCK" ]]; then
  df_output="$DF_MOCK"
else
  # Use -P for POSIX output, then grab the line for the requested path
  df_output=$(df -P "$PATH_TO_CHECK" 2>/dev/null | tail -1)
fi

# Extract the usage percentage (e.g., "85%")
usage_percent=$(echo "$df_output" | awk '{print $5}' | tr -d '%')

# Guard against parsing failures
if ! [[ "$usage_percent" =~ ^[0-9]+$ ]]; then
  echo "Unable to determine disk usage for $PATH_TO_CHECK" >&2
  exit 1
fi

if (( usage_percent >= THRESHOLD )); then
  msg=$(pick_message)
  echo "⚠️  Warning! Your $PATH_TO_CHECK is ${usage_percent}% full. $msg"
fi

exit 0
