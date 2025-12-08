#!/usr/bin/env bash

# Path to the log file (must be mounted by the user)
LOG_FILE="/logs/input.log"

# If the log file does not exist, print a friendly message and exit
if [[ ! -f "$LOG_FILE" ]]; then
  echo "🚨 No log file found at $LOG_FILE. Mount a directory containing 'input.log' at /logs."
  exit 1
fi

# Function to map log level to emoji
map_emoji() {
  case "$1" in
    INFO*) echo "ℹ️" ;;
    WARN*) echo "⚠️" ;;
    ERROR*) echo "❌" ;;
    *) echo "🐞" ;;
  esac
}

# Read the log file line by line
while IFS= read -r line; do
  # Extract the first word (log level) for mapping
  level=$(echo "$line" | awk '{print $1}')
  emoji=$(map_emoji "$level")
  echo "$emoji $line"
done < "$LOG_FILE"
