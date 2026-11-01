#!/usr/bin/env bash

# nightly-ssh-key-rotator
# Rotates the SSH host Ed25519 key, backs up the old key, and prints the new fingerprint.
#
# Options:
#   -d <dir>   Directory containing the host keys (default: /etc/ssh)
#   -b <dir>   Backup directory (optional). If omitted, a temporary backup dir is created.

set -euo pipefail

# Default values
SSH_DIR="/etc/ssh"
BACKUP_DIR=""

usage() {
  echo "Usage: $0 -d <ssh_dir> [-b <backup_dir>]"
  exit 1
}

while getopts ":d:b:h" opt; do
  case $opt in
    d) SSH_DIR="$OPTARG" ;;
    b) BACKUP_DIR="$OPTARG" ;;
    h) usage ;;
    \?) echo "Invalid option: -$OPTARG" >&2; usage ;;
    :) echo "Option -$OPTARG requires an argument." >&2; usage ;;
  esac
done

# Verify SSH directory exists
if [[ ! -d "$SSH_DIR" ]]; then
  echo "Error: SSH directory '$SSH_DIR' does not exist." >&2
  exit 1
fi

# Determine key file names (Ed25519 only for simplicity)
PRIVATE_KEY="$SSH_DIR/ssh_host_ed25519_key"
PUBLIC_KEY="$SSH_DIR/ssh_host_ed25519_key.pub"

# Create backup directory if needed
if [[ -z "$BACKUP_DIR" ]]; then
  TIMESTAMP=$(date +%Y%m%d_%H%M%S)
  BACKUP_DIR="/tmp/ssh_key_backup_$TIMESTAMP"
fi
mkdir -p "$BACKUP_DIR"

# Backup existing keys if they exist
if [[ -f "$PRIVATE_KEY" || -f "$PUBLIC_KEY" ]]; then
  TIMESTAMP=$(date +%Y%m%d_%H%M%S)
  BACKUP_SUBDIR="$BACKUP_DIR/backup_$TIMESTAMP"
  mkdir -p "$BACKUP_SUBDIR"
  echo "Backing up existing keys to $BACKUP_SUBDIR"
  [[ -f "$PRIVATE_KEY" ]] && cp -p "$PRIVATE_KEY" "$BACKUP_SUBDIR/"
  [[ -f "$PUBLIC_KEY" ]] && cp -p "$PUBLIC_KEY" "$BACKUP_SUBDIR/"
else
  echo "No existing Ed25519 host keys found; proceeding to generate new ones."
fi

# Generate new Ed25519 host key
# -q: quiet, -N "": empty passphrase, -t ed25519
ssh-keygen -q -N "" -t ed25519 -f "$PRIVATE_KEY"

# Compute fingerprint of the new public key
FINGERPRINT=$(ssh-keygen -lf "$PUBLIC_KEY" | awk '{print $2}')

echo "New host key fingerprint (SHA256): $FINGERPRINT"

exit 0
