#!/usr/bin/env bash
# uptime_lyricizer.sh - prints a whimsical description of system uptime

# Allow overriding the uptime source for testing via UPTIME_FILE env var
if [[ -n "$UPTIME_FILE" ]]; then
  uptime_source="$UPTIME_FILE"
else
  uptime_source="/proc/uptime"
fi

if [[ ! -r "$uptime_source" ]]; then
  echo "Error: cannot read $uptime_source" >&2
  exit 1
fi

# Read the first field (seconds) from the uptime source
read -r uptime_seconds _ < "$uptime_source"

# Strip fractional part to get integer seconds
uptime_seconds=${uptime_seconds%.*}

# Compute days, hours, minutes
days=$(( uptime_seconds / 86400 ))
hours=$(( (uptime_seconds % 86400) / 3600 ))
minutes=$(( (uptime_seconds % 3600) / 60 ))

echo "The system has been alive for $days days, $hours hours, $minutes minutes. Time flies!"
