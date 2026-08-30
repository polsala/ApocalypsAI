#!/usr/bin/env bash
set -euo pipefail

usage() { echo "Usage: $0 [-u username] [-d ssh_dir]" >&2; exit 1; }

USER_NAME="$(whoami)"
SSH_DIR="${HOME}/.ssh"

while getopts ":u:d:" opt; do
  case $opt in
    u) USER_NAME="$OPTARG" ;;
    d) SSH_DIR="$OPTARG" ;;
    *) usage ;;
  esac
done

# Resolve absolute path
SSH_DIR="$(cd "$SSH_DIR" && pwd)"

KEY_NAME="id_ed25519_rotated"
PRIVATE_KEY="${SSH_DIR}/${KEY_NAME}"
PUBLIC_KEY="${PRIVATE_KEY}.pub"
TIMESTAMP="$(date +%s)"
BACKUP_AUTH="${SSH_DIR}/authorized_keys.bak.${TIMESTAMP}"

echo "Rotating SSH keys for user: $USER_NAME"
echo "SSH directory: $SSH_DIR"

# Generate new key pair (no passphrase)
ssh-keygen -t ed25519 -f "$PRIVATE_KEY" -N "" -q

# Backup existing authorized_keys if it exists
if [[ -f "${SSH_DIR}/authorized_keys" ]]; then
  cp "${SSH_DIR}/authorized_keys" "$BACKUP_AUTH"
  echo "Backed up existing authorized_keys to $BACKUP_AUTH"
fi

# Install new public key as authorized_keys
cat "$PUBLIC_KEY" > "${SSH_DIR}/authorized_keys"
chmod 600 "${SSH_DIR}/authorized_keys"
echo "Installed new public key."

echo "Rotation complete. Private key: $PRIVATE_KEY"
