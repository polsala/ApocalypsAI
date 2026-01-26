#!/usr/bin/env bash
# Emoji Uptime Reporter

# Get uptime seconds
if [[ -n "$FAKE_UPTIME" ]]; then
  uptime_seconds=$FAKE_UPTIME
else
  # /proc/uptime first field is seconds with decimals
  if [[ -r /proc/uptime ]]; then
    uptime_seconds=$(awk '{print int($1)}' /proc/uptime)
  else
    echo "Cannot read /proc/uptime"
    exit 1
  fi
fi

days=$(( uptime_seconds / 86400 ))
hours=$(( (uptime_seconds % 86400) / 3600 ))
minutes=$(( (uptime_seconds % 3600) / 60 ))

echo "Uptime: ${days}🌞 ${hours}⏰ ${minutes}🕒"
