#!/usr/bin/env bash

# nightly-ssh-key-rotator
# Generates a new SSH key pair and distributes the public key to remote hosts.
#
# Usage: rotate_ssh_key.sh -u <user> -h "host1 host2" [-p <key_prefix>]

set -euo pipefail

# Default values
KEY_PREFIX="id_rsa_rotated"
USER=""
HOSTS=""

usage() {
  cat <<'EOF'
rotate_ssh_key.sh -u <remote_user> -h "host1 host2" [-p <key_prefix>]

  -u   Remote username (required)
  -h   Space‑separated list of hosts (required)
  -p   Prefix for generated key files (default: id_rsa_rotated)
EOF
  exit 1
}

# Parse arguments
while getopts ":u:h:p:" opt; do
  case $opt in
    u) USER="$OPTARG" ;;
    h) HOSTS="$OPTARG" ;;
    p) KEY_PREFIX="$OPTARG" ;;
    \?) echo "Invalid option: -$OPTARG" >&2; usage ;;
    :) echo "Option -$OPTARG requires an argument." >&2; usage ;;
  esac
done

# Validate required arguments
if [[ -z "$USER" || -z "$HOSTS" ]]; then
  echo "Error: -u and -h are required." >&2
  usage
fi

SSH_DIR="$HOME/.ssh"
KEY_PATH="$SSH_DIR/$KEY_PREFIX"
PUB_KEY_PATH="$KEY_PATH.pub"

rotate_key() {
  echo "Generating new SSH key pair at $KEY_PATH ..."
  # -q for quiet, -N '' for empty passphrase
  ssh-keygen -t rsa -b 2048 -f "$KEY_PATH" -N "" -q

  echo "Distributing public key to hosts..."
  for host in $HOSTS; do
    echo "  -> $USER@$host"
    ssh-copy-id -i "$PUB_KEY_PATH" "$USER@$host"
  done

  echo "Rotation complete. New key: $KEY_PATH"
}

rotate_key
