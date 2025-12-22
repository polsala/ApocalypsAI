#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo 'Usage: $0 -h host -l local_port -r remote_port [-c command] [-t timeout]'
  exit 1
}

# Default values
timeout=0
cmd=""

# Parse options
while getopts ":h:l:r:c:t:" opt; do
  case $opt in
    h) host=$OPTARG ;;
    l) local_port=$OPTARG ;;
    r) remote_port=$OPTARG ;;
    c) cmd=$OPTARG ;;
    t) timeout=$OPTARG ;;
    *) usage ;;
  esac
done

# Validate required options
if [[ -z ${host:-} || -z ${local_port:-} || -z ${remote_port:-} ]]; then
  usage
fi

# Function to clean up SSH tunnel
cleanup() {
  if [[ -n ${ssh_pid:-} ]]; then
    kill \"$ssh_pid\" 2>/dev/null || true
  fi
}

trap cleanup EXIT

# Start SSH tunnel
ssh -N -L \"${local_port}:localhost:${remote_port}\" \"$host\" &
ssh_pid=$!

# Wait a moment to ensure tunnel is up
sleep 0.5

echo '🛡️ Tunnel established to ${host} on local port ${local_port}'

# Optional timeout
if [[ $timeout -gt 0 ]]; then
  (
    sleep \"$timeout\"
    cleanup
  ) &
  timeout_pid=$!
fi

# Run optional command
if [[ -n $cmd ]]; then
  eval \"$cmd\"
  cmd_status=$?
else
  cmd_status=0
fi

# Wait for SSH to finish (should be killed by cleanup)
wait \"$ssh_pid\" 2>/dev/null || true

# If timeout was set, kill its background process
if [[ -n ${timeout_pid:-} ]]; then
  kill \"$timeout_pid\" 2>/dev/null || true
fi

exit \"$cmd_status\"
