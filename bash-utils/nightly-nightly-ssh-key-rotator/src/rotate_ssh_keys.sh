#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 -u USERNAME [-d SSH_DIR]" >&2
  exit 1
}

USER=""
SSH_DIR=""

while getopts ":u:d:" opt; do
  case $opt in
    u) USER=$OPTARG ;;
    d) SSH_DIR=$OPTARG ;;
    *) usage ;;
  esac
done

if [[ -z "$USER" ]]; then
  usage
fi

if [[ -z "$SSH_DIR" ]]; then
  SSH_DIR="/home/$USER/.ssh"
fi

if [[ ! -d "$SSH_DIR" ]]; then
  echo "SSH directory $SSH_DIR does not exist" >&2
  exit 1
fi

# Deterministic timestamp for testing; fallback to current epoch seconds
TIMESTAMP=${DATE_NOW:-$(date +%s)}

# Backup existing authorized_keys if present
if [[ -f "${SSH_DIR}/authorized_keys" ]]; then
  cp "${SSH_DIR}/authorized_keys" "${SSH_DIR}/authorized_keys.bak.${TIMESTAMP}"
fi

# Generate new ed25519 key pair (no passphrase)
KEY_PREFIX="${SSH_DIR}/id_ed25519_rotated_${TIMESTAMP}"
ssh-keygen -t ed25519 -f "$KEY_PREFIX" -N "" -q

# Append the new public key to authorized_keys
cat "${KEY_PREFIX}.pub" >> "${SSH_DIR}/authorized_keys"

echo "New SSH key generated: $KEY_PREFIX"
echo "Backup of old authorized_keys saved as: ${SSH_DIR}/authorized_keys.bak.${TIMESTAMP}"
