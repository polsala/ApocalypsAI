#!/usr/bin/env bash
set -euo pipefail

# Arguments: hosts_file [key_path]
HOSTS_FILE="${1:-}"
KEY_PATH="${2:-${HOME}/.ssh/id_rsa_rotated}"

if [[ -z "$HOSTS_FILE" ]]; then
  echo "Usage: $0 <hosts_file> [key_path]"
  exit 1
fi

# Generate new key pair (overwrite if exists)
ssh-keygen -t rsa -b 4096 -N "" -f "$KEY_PATH" -q

PUB_KEY="${KEY_PATH}.pub"

# Distribute public key to each host
while IFS= read -r host; do
  [[ -z "$host" ]] && continue
  echo "Deploying key to $host"
  ssh-copy-id -i "$PUB_KEY" "$host"
done < "$HOSTS_FILE"

echo "Key rotation complete. Private key: $KEY_PATH"
