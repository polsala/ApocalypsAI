#!/usr/bin/env bash

# nightly-uptime-emoji-report
# Prints system uptime with an emoji reflecting load per CPU core.

# Function to obtain the 1‑minute load average
get_load_average() {
  if [[ -n "$MOCK_LOAD" ]]; then
    echo "$MOCK_LOAD"
    return
  fi
  # Read the first field from /proc/loadavg
  if [[ -r /proc/loadavg ]]; then
    awk '{print $1}' /proc/loadavg
  else
    # Fallback to uptime command parsing (unlikely on modern Linux)
    uptime | awk -F'load average:' '{print $2}' | cut -d',' -f1 | tr -d ' '
  fi
}

# Function to obtain the number of CPU cores
get_cpu_cores() {
  if [[ -n "$MOCK_CORES" ]]; then
    echo "$MOCK_CORES"
    return
  fi
  if command -v nproc >/dev/null 2>&1; then
    nproc
  else
    # Portable fallback using getconf
    getconf _NPROCESSORS_ONLN
  fi
}

# Determine the appropriate emoji based on load per core
choose_emoji() {
  local load_per_core=$1
  # Use bc for floating point comparison (bc is standard on most distros)
  if (( $(echo "$load_per_core <= 0.5" | bc -l) )); then
    echo "😊"
  elif (( $(echo "$load_per_core <= 1.0" | bc -l) )); then
    echo "😐"
  else
    echo "😫"
  fi
}

main() {
  local load=$(get_load_average)
  local cores=$(get_cpu_cores)
  # Guard against division by zero
  if [[ "$cores" -eq 0 ]]; then
    cores=1
  fi
  # Compute load per core with bc for floating point division
  local load_per_core=$(echo "scale=3; $load / $cores" | bc -l)
  local emoji=$(choose_emoji "$load_per_core")
  # Get human‑readable uptime (e.g., "up 3 days, 4:12")
  local uptime_str=$(uptime -p 2>/dev/null || uptime | sed -E 's/.*up //;s/, .*//')
  echo "System uptime: $uptime_str $emoji"
}

# Execute only if script is run directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
