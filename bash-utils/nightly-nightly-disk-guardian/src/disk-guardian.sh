#!/usr/bin/env bash

# nightly-disk-guardian
# Checks disk usage and prints whimsical warnings when usage exceeds a threshold.

set -euo pipefail

# Default threshold (percentage)
THRESHOLD=80

# Whimsical messages (feel free to add more)
PHRASES=(
  "Time to summon more storage spirits!"
  "Your disks are getting greedy!"
  "Consider feeding them some cleanup crumbs."
  "The void is expanding—make space!"
  "Your storage is on a diet, but it's starving."
)

print_help() {
  cat <<'EOF'
Usage: ./src/disk-guardian.sh [options] [mount1 mount2 ...]

Options:
  -t <percent>   Threshold percentage (default: 80)
  -h             Show this help message

If no mount points are supplied, '/' is checked.
EOF
}

# Parse options
while getopts ":t:h" opt; do
  case $opt in
    t)
      THRESHOLD=$OPTARG
      ;;
    h)
      print_help
      exit 0
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      print_help
      exit 1
      ;;
    :) 
      echo "Option -$OPTARG requires an argument." >&2
      print_help
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))

# Remaining arguments are mount points; default to '/' if none provided
MOUNTS=(${@:-/})

# Function to check a single mount point
check_mount() {
  local mount=$1
  # Use df -h to get human‑readable output; fallback to df if -h not supported
  if df_output=$(df -h "$mount" 2>/dev/null); then
    :
  else
    df_output=$(df "$mount" 2>/dev/null)
  fi
  # Extract the Use% column from the second line
  usage_percent=$(echo "$df_output" | awk 'NR==2 {print $5}' | tr -d '%')
  if [[ -z $usage_percent ]]; then
    echo "⚠️  Could not determine usage for $mount"
    return
  fi
  if (( usage_percent >= THRESHOLD )); then
    # Pick a random whimsical phrase
    phrase=${PHRASES[$RANDOM % ${#PHRASES[@]}]}
    echo "⚠️  Warning! $mount is at ${usage_percent}% full. $phrase"
  fi
}

for m in "${MOUNTS[@]}"; do
  check_mount "$m"
done
