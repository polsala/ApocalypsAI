#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<EOF
Usage: $0 -h <remote_host> -p <remote_port> -l <local_port> [-u <user>] [-k <key_file>] [-n <name>]
EOF
  exit 1
}

# Default values
USER="$(whoami)"
KEY=""
NAME=""

# Parse arguments
while getopts ":h:p:l:u:k:n:" opt; do
  case $opt in
    h) REMOTE_HOST="$OPTARG" ;;
    p) REMOTE_PORT="$OPTARG" ;;
    l) LOCAL_PORT="$OPTARG" ;;
    u) USER="$OPTARG" ;;
    k) KEY="$OPTARG" ;;
    n) NAME="$OPTARG" ;;
    *) usage ;;
  esac
done

# Validate required
if [[ -z "${REMOTE_HOST:-}" || -z "${REMOTE_PORT:-}" || -z "${LOCAL_PORT:-}" ]]; then
  echo "Error: remote host, remote port, and local port are required." >&2
  usage
fi

# Build ssh command
SSH_CMD=(ssh -N -L "${LOCAL_PORT}:localhost:${REMOTE_PORT}" "${USER}@${REMOTE_HOST}")

if [[ -n "$KEY" ]]; then
  SSH_CMD+=(-i "$KEY")
fi

# Add options for better behavior
SSH_CMD+=(-o ExitOnForwardFailure=yes)

# Start tunnel in background
"${SSH_CMD[@]}" &
TUNNEL_PID=$!

# Wait a bit to check if ssh started
sleep 1

# Check if process is still running
if kill -0 "$TUNNEL_PID" 2>/dev/null; then
  if [[ -n "$NAME" ]]; then
    echo "🚀 Tunnel '$NAME' started: ${LOCAL_PORT} -> ${REMOTE_HOST}:${REMOTE_PORT} (PID $TUNNEL_PID)"
  else
    echo "🚀 Tunnel started: ${LOCAL_PORT} -> ${REMOTE_HOST}:${REMOTE_PORT} (PID $TUNNEL_PID)"
  fi
else
  echo "❌ Failed to start SSH tunnel." >&2
  exit 1
fi

# Trap to kill tunnel on exit
trap 'echo "🛑 Stopping tunnel (PID $TUNNEL_PID)"; kill "$TUNNEL_PID" 2>/dev/null' EXIT

# Wait for tunnel process
wait "$TUNNEL_PID"
