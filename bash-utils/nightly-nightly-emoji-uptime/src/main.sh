#!/usr/bin/env bash
# nightly-emoji-uptime: display uptime with emojis

# Format a number of seconds into a string with emojis for days, hours, minutes.
# Arguments:
#   $1 - total seconds (integer)
# Output:
#   Echoes the formatted string without a trailing newline.
function format_uptime() {
  local total_seconds=$1
  local days=$(( total_seconds / 86400 ))
  local hours=$(( (total_seconds % 86400) / 3600 ))
  local minutes=$(( (total_seconds % 3600) / 60 ))

  local result=""
  if (( days > 0 )); then
    result+="${days}📅 "
  fi
  if (( hours > 0 )); then
    result+="${hours}🕒 "
  fi
  if (( minutes > 0 )); then
    result+="${minutes}⏱️"
  fi
  echo -n "${result}"
}

# Retrieve the system uptime in seconds.
# Tries to read /proc/uptime; falls back to parsing `uptime -s` if unavailable.
function get_uptime_seconds() {
  if [[ -r /proc/uptime ]]; then
    awk '{print int($1)}' /proc/uptime
  else
    # Fallback (unlikely on modern Linux) – compute difference between now and boot time.
    local boot_time=$(uptime -s 2>/dev/null || echo "")
    if [[ -n $boot_time ]]; then
      local boot_epoch=$(date -d "$boot_time" +%s)
      local now_epoch=$(date +%s)
      echo $(( now_epoch - boot_epoch ))
    else
      echo 0
    fi
  fi
}

# Main entry point.
# If an argument is supplied, it is interpreted as the uptime in seconds (useful for testing).
# Otherwise the script reads the actual system uptime.
function main() {
  local seconds
  if [[ -n $1 ]]; then
    seconds=$1
  else
    seconds=$(get_uptime_seconds)
  fi
  local formatted=$(format_uptime "$seconds")
  echo "Uptime: $formatted"
}

# Execute main when the script is run directly.
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
