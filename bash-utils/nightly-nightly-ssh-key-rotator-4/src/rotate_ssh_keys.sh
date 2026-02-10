#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 -u USER [-d DIR] [-b BACKUP_DAYS]"
  exit 1
}

while getopts "u:d:b:" opt; do
  case $opt in
    u) USER=$OPTARG ;;
    d) SSH_DIR=$OPTARG ;;
    b) BACKUP_DAYS=$OPTARG ;;
    *) usage ;;
  esac
done

if [[ -z "${USER:-}" ]]; then
  usage
fi

SSH_DIR=${SSH_DIR:-"$HOME/.ssh"}
BACKUP_DAYS=${BACKUP_DAYS:-30}
TIMESTAMP=$(date +%Y%m%d%H%M%S)
KEY_NAME="id_ed25519_$TIMESTAMP"
KEY_PATH="$SSH_DIR/$KEY_NAME"

# Ensure directory exists
mkdir -p "$SSH_DIR"
chmod 700 "$SSH_DIR"

# Generate key (mockable)
if [[ -n "${SSH_KEYGEN_MOCK:-}" ]]; then
  # Create dummy files for testing
  echo "mock private key" > "$KEY_PATH"
  echo "mock public key $USER@$HOSTNAME" > "${KEY_PATH}.pub"
else
  ssh-keygen -t ed25519 -f "$KEY_PATH" -N "" -C "$USER@$HOSTNAME"
fi
chmod 600 "$KEY_PATH"
chmod 644 "${KEY_PATH}.pub"

# Backup old authorized_keys
AUTH_KEYS="$SSH_DIR/authorized_keys"
if [[ -f "$AUTH_KEYS" ]]; then
  BACKUP="$SSH_DIR/authorized_keys.backup.$TIMESTAMP"
  cp "$AUTH_KEYS" "$BACKUP"
fi

# Append new public key
cat "${KEY_PATH}.pub" >> "$AUTH_KEYS"
chmod 600 "$AUTH_KEYS"

# Cleanup old private keys older than BACKUP_DAYS (excluding the newly created one)
find "$SSH_DIR" -maxdepth 1 -type f -name "id_ed25519_*" -mtime +"$BACKUP_DAYS" -not -name "*${TIMESTAMP}*" -exec rm -f {} +

echo "New SSH key $KEY_NAME generated and added to authorized_keys."
