#!/usr/bin/env bash
set -euo pipefail

# Default threshold is 80% if not supplied
THRESHOLD="${1:-80}"

# Retrieve the usage percentage of the root filesystem
USAGE=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')

echo "Disk usage: ${USAGE}%"

if (( USAGE > THRESHOLD )); then
  cat <<'EOF'
⚔️  Guardian says: "Your disk is thirsty! Clean up soon!"
   /\_/\
  ( o.o )
   > ^ <
EOF
  exit 1
else
  echo "All is calm."
  exit 0
fi
