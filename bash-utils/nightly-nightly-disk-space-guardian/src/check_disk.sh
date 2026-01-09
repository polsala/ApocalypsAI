#!/usr/bin/env bash

# nightly-disk-space-guardian
# Checks root filesystem disk usage and alerts if usage exceeds a threshold.
# Default threshold is 80%.

set -euo pipefail

print_usage() {
  echo "Usage: $0 [-t THRESHOLD]"
  echo "  -t THRESHOLD   Disk usage percentage threshold (default: 80)"
  exit 2
}

# Parse command‑line arguments
THRESHOLD=80
while getopts ":t:h" opt; do
  case $opt in
    t) THRESHOLD=$OPTARG ;;
    h) print_usage ;;
    \?) echo "Invalid option: -$OPTARG" >&2; print_usage ;;
    :) echo "Option -$OPTARG requires an argument." >&2; print_usage ;;
  esac
done
shift $((OPTIND -1))

check_disk_usage() {
  local threshold=$1
  # Allow the df command to be overridden (useful for testing)
  local df_output
  df_output=$(df -h / 2>/dev/null || true)
  # Extract the usage percentage from the second line (NR==2) and strip the % sign
  local usage
  usage=$(echo "$df_output" | awk 'NR==2 {print $5}' | tr -d '%')
  if [[ -z $usage ]]; then
    echo "❓ Unable to determine disk usage."
    return 2
  fi
  if (( usage >= threshold )); then
    echo "⚠️ Disk usage is at ${usage}%, exceeds threshold ${threshold}%!"
    return 1
  else
    echo "✅ Disk usage is at ${usage}%, below threshold ${threshold}%."
    return 0
  fi
}

# If the script is executed directly, run the check with the parsed threshold
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  check_disk_usage "$THRESHOLD"
fi
