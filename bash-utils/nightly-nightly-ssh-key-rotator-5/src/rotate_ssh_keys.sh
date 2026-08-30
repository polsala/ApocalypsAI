#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <private_key_path>"
  exit 1
fi

KEY_PATH="$1"
if [[ ! -f "$KEY_PATH" ]]; then
  echo "Error: Private key '$KEY_PATH' does not exist."
  exit 1
fi

TIMESTAMP=$(date +%Y%m%d%H%M%S)
BACKUP_PRIV="${KEY_PATH}.bak.${TIMESTAMP}"
BACKUP_PUB="${KEY_PATH}.pub.bak.${TIMESTAMP}"

# Backup existing keys
cp "$KEY_PATH" "$BACKUP_PRIV"
if [[ -f "${KEY_PATH}.pub" ]]; then
  cp "${KEY_PATH}.pub" "$BACKUP_PUB"
fi

# Generate new key pair
ssh-keygen -t rsa -b 2048 -f "$KEY_PATH" -N "" -q

echo "Old key backed up to: $BACKUP_PRIV"
if [[ -f "${KEY_PATH}.pub" ]]; then
  echo "Old public key backed up to: $BACKUP_PUB"
fi
echo "New key generated at: $KEY_PATH"
