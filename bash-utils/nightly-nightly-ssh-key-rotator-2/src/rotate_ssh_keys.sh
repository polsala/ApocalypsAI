#!/usr/bin/env bash
set -euo pipefail

# nightly-ssh-key-rotator
# Rotates SSH keys for a given .ssh directory.
# Backups existing keys (if any) and creates new placeholder keys.
# In production replace the placeholder generation with `ssh-keygen`.

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <ssh_dir>"
  exit 1
fi

SSH_DIR="$1"

if [[ ! -d "$SSH_DIR" ]]; then
  echo "Directory $SSH_DIR does not exist"
  exit 1
fi

# Backup existing keys
if [[ -f "$SSH_DIR/id_rsa" ]]; then
  mv "$SSH_DIR/id_rsa" "$SSH_DIR/id_rsa.old"
fi
if [[ -f "$SSH_DIR/id_rsa.pub" ]]; then
  mv "$SSH_DIR/id_rsa.pub" "$SSH_DIR/id_rsa.pub.old"
fi

# Generate new dummy keys (replace with ssh-keygen in real use)
echo "new_private_key" > "$SSH_DIR/id_rsa"
chmod 600 "$SSH_DIR/id_rsa"

echo "new_public_key" > "$SSH_DIR/id_rsa.pub"
chmod 644 "$SSH_DIR/id_rsa.pub"

echo "SSH keys rotated successfully in $SSH_DIR"
