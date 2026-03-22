#!/usr/bin/env bash

# Disk Guardian – monitors root filesystem usage and warns with apocalyptic messages.

set -euo pipefail

THRESHOLD=80

print_help() {
  cat <<'EOF'
Usage: ./disk-guardian.sh [options]

Options:
  -t, --threshold PERCENT   Set warning threshold (default 80)
  -h, --help                Show this help
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -t|--threshold)
      if [[ -n "${2-}" && "$2" =~ ^[0-9]+$ ]]; then
        THRESHOLD=$2
        shift 2
      else
        echo "Error: --threshold requires a numeric argument"
        exit 1
      fi
      ;;
    -h|--help)
      print_help
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      print_help
      exit 1
      ;;
  esac
done

# Get root filesystem usage percent
USAGE=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')

if (( USAGE > THRESHOLD )); then
  # List of apocalyptic phrases
  PHRASES=(
    "The world is ending in $((100-USAGE))% free space!"
    "Doomsday approaches as disks fill up!"
    "Your storage is a ticking time bomb!"
    "Apocalypse now: only $((100-USAGE))% left!"
    "The void swallows ${USAGE}% of your disk!"
  )
  # Pick random phrase
  RANDOM_INDEX=$((RANDOM % ${#PHRASES[@]}))
  echo "⚠️  Disk usage at ${USAGE}% – ${PHRASES[$RANDOM_INDEX]}"
else
  echo "✅ Disk usage at ${USAGE}% – All is calm."
fi
