#!/usr/bin/env bash
set -euo pipefail

# Default values
THRESHOLD=80
CLEANUP=false

# Parse options
while getopts ":t:c" opt; do
  case $opt in
    t)
      THRESHOLD=$OPTARG
      ;;
    c)
      CLEANUP=true
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

# Determine which directory to treat as temporary storage (allows testing)
TMPDIR=${TMPDIR:-/tmp}

# Get root usage percentage
USAGE=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
if [[ -z "$USAGE" ]]; then
  echo "Failed to determine disk usage." >&2
  exit 1
fi

if (( USAGE > THRESHOLD )); then
  echo "⚠️  Disk usage is at ${USAGE}% (threshold ${THRESHOLD}%). Consider cleaning up."
  if $CLEANUP; then
    echo "🧹 Cleaning $TMPDIR files older than 1 day..."
    find "$TMPDIR" -type f -mtime +1 -print -delete || echo "Cleanup failed."
  fi
else
  echo "✅ Disk usage is at ${USAGE}% (below threshold ${THRESHOLD}%). All good."
fi
