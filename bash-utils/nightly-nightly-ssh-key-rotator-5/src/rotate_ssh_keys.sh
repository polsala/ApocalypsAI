#!/usr/bin/env bash

# nightly-ssh-key-rotator
# Rotates a user's SSH key pair, backing up the old keys.

set -euo pipefail

# Allow caller to specify a custom .ssh directory; default to $HOME/.ssh
SSH_DIR="${SSH_DIR:-$HOME/.ssh}"

# Ensure the directory exists
if [[ ! -d "$SSH_DIR" ]]; then
  echo "Error: SSH directory '$SSH_DIR' does not exist." >&2
  exit 1
fi

# Timestamp for backup filenames
TS=$(date +"%Y%m%d%H%M%S")

# Function to backup a file if it exists
backup_if_exists() {
  local file="$1"
  if [[ -f "$file" ]]; then
    local backup="${file}.bak.$TS"
    mv "$file" "$backup"
    echo "Backed up $file -> $backup"
  fi
}

# Backup existing private and public keys
backup_if_exists "$SSH_DIR/id_rsa"
backup_if_exists "$SSH_DIR/id_rsa.pub"

# Generate a new RSA key pair (no passphrase)
# Mock rationale: In tests we replace ssh-keygen with a stub that creates placeholder files.
ssh-keygen -t rsa -b 2048 -f "$SSH_DIR/id_rsa" -N "" -q

echo "Generated new SSH key pair at $SSH_DIR/id_rsa"

# Optional: restart sshd if running (non‑blocking, ignore errors)
if command -v systemctl >/dev/null 2>&1; then
  if systemctl is-active --quiet sshd; then
    echo "Restarting sshd..."
    sudo systemctl restart sshd || echo "Warning: failed to restart sshd (you may need to do it manually)"
  fi
fi

exit 0
