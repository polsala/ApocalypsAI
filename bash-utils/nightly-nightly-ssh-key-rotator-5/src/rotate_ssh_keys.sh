#!/usr/bin/env bash

# nightly-ssh-key-rotator – rotate a user's SSH key pair safely
# ------------------------------------------------------------
# Usage: rotate_ssh_keys.sh --user <username> [--key-dir <dir>] [--backup-dir <dir>]
#
# This script generates a new RSA key pair, backs up the old private key,
# and ensures the new public key is present in authorized_keys.
# ------------------------------------------------------------

set -euo pipefail

# Default values (will be overridden if arguments are supplied)
USER_NAME=""
KEY_DIR=""
BACKUP_DIR=""

print_usage() {
  cat <<'EOF'
Usage: $0 --user <username> [--key-dir <ssh-dir>] [--backup-dir <backup-dir>]

Options:
  --user        Required. System username whose keys will be rotated.
  --key-dir     Directory containing the current keys (default: ~/.ssh).
  --backup-dir  Directory to store old private keys (default: ~/.ssh/key_backups).
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --user)
      USER_NAME="$2"
      shift 2
      ;;
    --key-dir)
      KEY_DIR="$2"
      shift 2
      ;;
    --backup-dir)
      BACKUP_DIR="$2"
      shift 2
      ;;
    -h|--help)
      print_usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      print_usage
      exit 1
      ;;
  esac
done

# Validate required arguments
if [[ -z "$USER_NAME" ]]; then
  echo "Error: --user is required" >&2
  print_usage
  exit 1
fi

# Resolve defaults based on the target user
HOME_DIR=$(eval echo "~$USER_NAME")
KEY_DIR=${KEY_DIR:-"$HOME_DIR/.ssh"}
BACKUP_DIR=${BACKUP_DIR:-"$KEY_DIR/key_backups"}

# Ensure directories exist
mkdir -p "$KEY_DIR"
mkdir -p "$BACKUP_DIR"

PRIVATE_KEY="$KEY_DIR/id_rsa"
PUBLIC_KEY="$KEY_DIR/id_rsa.pub"
AUTHORIZED_KEYS="$KEY_DIR/authorized_keys"

# Timestamp for backup naming
TIMESTAMP=$(date +"%Y%m%d%H%M%S")

# Step 1: Backup existing private key if it exists
if [[ -f "$PRIVATE_KEY" ]]; then
  BACKUP_PATH="$BACKUP_DIR/id_rsa.$TIMESTAMP"
  echo "Backing up existing private key to $BACKUP_PATH"
  mv "$PRIVATE_KEY" "$BACKUP_PATH"
  # Also backup the public key if present
  if [[ -f "$PUBLIC_KEY" ]]; then
    mv "$PUBLIC_KEY" "$BACKUP_DIR/id_rsa.pub.$TIMESTAMP"
  fi
fi

# Step 2: Generate a new RSA key pair (no passphrase)
# Mock rationale: In CI we cannot invoke ssh-keygen without a real environment, but the command works on real systems.
ssh-keygen -t rsa -b 2048 -f "$PRIVATE_KEY" -N "" -q

# Step 3: Ensure the new public key is in authorized_keys
if [[ ! -f "$AUTHORIZED_KEYS" ]]; then
  touch "$AUTHORIZED_KEYS"
  chmod 600 "$AUTHORIZED_KEYS"
fi

NEW_PUB_CONTENT=$(cat "$PUBLIC_KEY")
if ! grep -Fxq "$NEW_PUB_CONTENT" "$AUTHORIZED_KEYS"; then
  echo "Appending new public key to authorized_keys"
  echo "$NEW_PUB_CONTENT" >> "$AUTHORIZED_KEYS"
fi

echo "SSH key rotation complete for user $USER_NAME."
