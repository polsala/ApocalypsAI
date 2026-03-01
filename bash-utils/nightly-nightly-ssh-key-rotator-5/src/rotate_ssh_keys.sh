#!/usr/bin/env bash
set -euo pipefail

# Default values
KEY_TYPE="ed25519"
KEY_DIR="/etc/ssh"
RESTART=false

usage() {
  echo "Usage: $0 [-t rsa|ed25519] [-d key_dir] [-r]"
  exit 1
}

while getopts ":t:d:r" opt; do
  case $opt in
    t) KEY_TYPE=$OPTARG ;;
    d) KEY_DIR=$OPTARG ;;
    r) RESTART=true ;;
    *) usage ;;
  esac
done

# Ensure ssh-keygen is available
command -v ssh-keygen >/dev/null 2>&1 || { echo "ssh-keygen not found"; exit 1; }

# Create backup directory with timestamp
TIMESTAMP=$(date +%s)
BACKUP_DIR="${KEY_DIR}/backup-${TIMESTAMP}"
mkdir -p "$BACKUP_DIR"

# Find existing host key files (exclude .pub)
shopt -s nullglob
HOST_KEYS=("$KEY_DIR"/ssh_host_*_key)
if [ ${#HOST_KEYS[@]} -eq 0 ]; then
  echo "No existing host keys found in $KEY_DIR"
else
  for key in "${HOST_KEYS[@]}"; do
    base=$(basename "$key")
    mv "$key" "$BACKUP_DIR/$base"
    pub="${key}.pub"
    if [ -f "$pub" ]; then
      mv "$pub" "$BACKUP_DIR/$(basename "$pub")"
    fi
  done
fi

# Generate new keys based on requested type
case "$KEY_TYPE" in
  rsa)
    ssh-keygen -t rsa -b 4096 -f "$KEY_DIR/ssh_host_rsa_key" -N "" -q
    ;;
  ed25519)
    ssh-keygen -t ed25519 -f "$KEY_DIR/ssh_host_ed25519_key" -N "" -q
    ;;
  *)
    echo "Unsupported key type: $KEY_TYPE"
    exit 1
    ;;
esac

echo "New SSH host keys generated in $KEY_DIR"

if $RESTART; then
  if command -v systemctl >/dev/null 2>&1; then
    systemctl restart sshd || systemctl restart ssh || echo "Failed to restart sshd"
  elif command -v service >/dev/null 2>&1; then
    service ssh restart || echo "Failed to restart ssh"
  else
    echo "No known service manager to restart sshd"
  fi
  echo "sshd service restarted"
fi

exit 0
