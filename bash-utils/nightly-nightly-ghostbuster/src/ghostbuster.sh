#!/usr/bin/env bash
set -euo pipefail

DRY_RUN=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=true; shift ;;
    *) echo "Usage: $0 [--dry-run]"; exit 1 ;;
  esac
done

# Find zombie processes (state Z)
zombies=$(ps -eo pid,ppid,state,cmd | awk '$3=="Z"{print $1,$2,$4}')
if [[ -z "$zombies" ]]; then
  echo "No zombie processes found."
  exit 0
fi

echo "Found zombie processes (PID PPID CMD):"
echo "$zombies"

if $DRY_RUN; then
  exit 0
fi

# Attempt to kill parent processes (except init PID 1)
while read -r pid ppid cmd; do
  if [[ "$ppid" -ne 1 ]]; then
    echo "Killing parent process $ppid of zombie $pid..."
    kill -9 "$ppid" 2>/dev/null || echo "Failed to kill $ppid"
  else
    echo "Parent of zombie $pid is init (PID 1); cannot kill."
  fi
done <<< "$zombies"

exit 0
