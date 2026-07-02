#!/usr/bin/env bash
# nightly-uptime-emoji-report
# If an argument is given, treat it as uptime seconds (for testing).
# Otherwise read from /proc/uptime.

get_uptime_seconds() {
  if [[ -n "$1" ]]; then
    echo "$1"
  else
    # /proc/uptime: first field is seconds with decimals
    awk '{print int($1)}' /proc/uptime
  fi
}

format_uptime() {
  local secs=$1
  local mins=$(( secs / 60 ))
  local hrs=$(( secs / 3600 ))
  if (( secs < 3600 )); then
    echo "$mins minutes"
  else
    echo "$hrs hours"
  fi
}

choose_emoji() {
  local secs=$1
  if (( secs < 3600 )); then
    echo "🚀"
  elif (( secs < 86400 )); then
    echo "😊"
  else
    echo "💤"
  fi
}

main() {
  local secs
  secs=$(get_uptime_seconds "$1")
  local uptime_str
  uptime_str=$(format_uptime "$secs")
  local emoji
  emoji=$(choose_emoji "$secs")
  echo "Uptime: $uptime_str $emoji"
}

main "$@"
