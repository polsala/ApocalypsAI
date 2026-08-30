#!/usr/bin/env bash

# Test suite for nightly-ssh-key-rotator
# ------------------------------------------------------------
# This script creates a temporary HOME environment, runs the rotator,
# and checks that the expected files are created/moved.
# ------------------------------------------------------------

set -euo pipefail

# Locate the script under test
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)
ROTATE_SCRIPT="$SCRIPT_DIR/rotate_ssh_keys.sh"

# Create a temporary directory to act as a fake HOME
TMP_HOME=$(mktemp -d)
export HOME="$TMP_HOME"

# Mock user name (will resolve to $HOME)
USER_NAME="testuser"

# Create initial fake .ssh directory with an old key pair
SSH_DIR="$HOME/.ssh"
mkdir -p "$SSH_DIR"
# Create dummy old private key and public key
echo "OLD_PRIVATE_KEY" > "$SSH_DIR/id_rsa"
chmod 600 "$SSH_DIR/id_rsa"
echo "OLD_PUBLIC_KEY" > "$SSH_DIR/id_rsa.pub"
chmod 644 "$SSH_DIR/id_rsa.pub"
# Create an authorized_keys file containing the old public key
echo "OLD_PUBLIC_KEY" > "$SSH_DIR/authorized_keys"
chmod 600 "$SSH_DIR/authorized_keys"

# Run the rotator script
bash "$ROTATE_SCRIPT" --user "$USER_NAME"

# ---- Assertions ----
# 1. New private key should exist
if [[ ! -f "$SSH_DIR/id_rsa" ]]; then
  echo "FAIL: New private key not found" >&2
  exit 1
fi

# 2. New public key should exist
if [[ ! -f "$SSH_DIR/id_rsa.pub" ]]; then
  echo "FAIL: New public key not found" >&2
  exit 1
fi

# 3. Backup directory should contain the old private key
BACKUP_DIR="$SSH_DIR/key_backups"
if [[ ! -d "$BACKUP_DIR" ]]; then
  echo "FAIL: Backup directory not created" >&2
  exit 1
fi
# Find any backup file matching the pattern
OLD_BACKUP=$(ls "$BACKUP_DIR"/id_rsa.* 2>/dev/null || true)
if [[ -z "$OLD_BACKUP" ]]; then
  echo "FAIL: Old private key not backed up" >&2
  exit 1
fi
# Verify its contents are the old key
if ! grep -q "OLD_PRIVATE_KEY" "$OLD_BACKUP"; then
  echo "FAIL: Backup does not contain old private key" >&2
  exit 1
fi

# 4. authorized_keys should contain the new public key (and still contain the old one)
NEW_PUB=$(cat "$SSH_DIR/id_rsa.pub")
if ! grep -Fxq "$NEW_PUB" "$SSH_DIR/authorized_keys"; then
  echo "FAIL: New public key not appended to authorized_keys" >&2
  exit 1
fi

# 5. Ensure the script exited cleanly
echo "All tests passed for nightly-ssh-key-rotator."

# Cleanup temporary home
rm -rf "$TMP_HOME"
