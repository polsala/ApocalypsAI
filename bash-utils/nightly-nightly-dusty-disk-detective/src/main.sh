#!/usr/bin/env bash
set -euo pipefail

# Default threshold is 80% if not supplied
THRESHOLD=${1:-80}

# Get the usage percentage of the root filesystem
# The mock `df` used in tests prints a line like:
#   /dev/root 20G 10G 10G 50% /
usage=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')

if (( usage > THRESHOLD )); then
  cat <<'EOF'
   _____  _   _ _____ _____   ____ ___  _   _ _____ 
  |  __ \| \ | |_   _|  __ \ / __ \__ \| \ | |_   _|
  | |  | |  \| | | | | |__) | |  | | ) |  \| | | |  
  | |  | | . ` | | | |  ___/| |  | |/ /| . ` | | |  
  | |__| | |\  |_| |_| |    | |__| / /_| |\  |_| |_ 
  |_____/|_| \_|_____|_|     \____/____|_| \_|_____|
EOF
  echo "Warning: Disk usage at ${usage}% exceeds threshold of ${THRESHOLD}%."
else
  echo "Disk usage is ${usage}%, within safe limits."
fi
