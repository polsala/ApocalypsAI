#!/usr/bin/env bash
set -euo pipefail

# Default values
USER_NAME="${USER}"
SSH_DIR="${HOME}/.ssh"

# Parse options
while getopts "u:d:" opt; do
  case "$opt" in
    u) USER_NAME="$OPTARG" ;;
    d) SSH_DIR="$OPTARG" ;;
    *) echo "Usage: $0 [-u username] [-d ssh_dir]" >&2; exit 1 ;;
  esac
done

# Resolve absolute path
SSH_DIR="$(cd "$SSH_DIR" && pwd)"

if [[ ! -d "$SSH_DIR" ]]; then
  echo "Error: SSH directory '$SSH_DIR' does not exist." >&2
  exit 1
fi

BACKUP_DIR="${SSH_DIR}/backup"
mkdir -p "$BACKUP_DIR"

# Move existing id_* keys to backup
shopt -s nullglob
for key in "$SSH_DIR"/id_*; do
  mv "$key" "$BACKUP_DIR"/
 done
shopt -u nullglob

# Generate new ed25519 key pair
NEW_KEY="${SSH_DIR}/id_ed25519"
ssh-keygen -t ed25519 -f "$NEW_KEY" -N "" -q

# Replace authorized_keys with the new public key
AUTH_KEYS="${SSH_DIR}/authorized_keys"
cat "${NEW_KEY}.pub" > "$AUTH_KEYS"

echo "SSH keys rotated for user '$USER_NAME'. New key: $NEW_KEY"
