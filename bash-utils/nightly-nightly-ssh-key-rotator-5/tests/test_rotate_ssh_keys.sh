#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Use a temporary directory to simulate /etc/ssh without affecting the host.
TMPDIR=$(mktemp -d)
KEY_DIR="${TMPDIR}/ssh"
mkdir -p "$KEY_DIR"

# Create dummy existing keys
ssh-keygen -t ed25519 -f "$KEY_DIR/ssh_host_ed25519_key" -N "" -q >/dev/null
ssh-keygen -t rsa -b 4096 -f "$KEY_DIR/ssh_host_rsa_key" -N "" -q >/dev/null

# Locate the script relative to this test file
SCRIPT_PATH="$(dirname "$0")/../src/rotate_ssh_keys.sh"

# Run the rotator without restarting the service, requesting RSA keys
bash "$SCRIPT_PATH" -t rsa -d "$KEY_DIR"

# Verify that a backup directory was created
BACKUPS=("$KEY_DIR"/backup-*)
if [ ${#BACKUPS[@]} -ne 1 ]; then
  echo "Backup directory not created"
  exit 1
fi
BACKUP_DIR="${BACKUPS[0]}"

# Old keys should be moved to the backup directory
if [ -f "$BACKUP_DIR/ssh_host_ed25519_key" ] && [ -f "$BACKUP_DIR/ssh_host_rsa_key" ]; then
  echo "Old keys backed up"
else
  echo "Old keys not found in backup"
  exit 1
fi

# New RSA key should exist in the key directory
if [ -f "$KEY_DIR/ssh_host_rsa_key" ] && [ -f "$KEY_DIR/ssh_host_rsa_key.pub" ]; then
  echo "New RSA key generated"
else
  echo "New RSA key missing"
  exit 1
fi

# No new ed25519 key should be generated (we asked for RSA only)
if [ -f "$KEY_DIR/ssh_host_ed25519_key" ]; then
  echo "Unexpected ed25519 key generated"
  exit 1
fi

echo "All tests passed"
exit 0
