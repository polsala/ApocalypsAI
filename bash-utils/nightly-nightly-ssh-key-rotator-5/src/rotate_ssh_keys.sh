#!/usr/bin/env bash

set -euo pipefail

# Generate a temporary RSA key pair
generate_key() {
  local key_dir="$1"
  mkdir -p "$key_dir"
  ssh-keygen -t rsa -b 4096 -N "" -f "$key_dir/id_rsa" >/dev/null
}

# Backup existing keys on remote host
backup_keys() {
  local host="$1"
  local user="$2"
  local timestamp=$(date +%s)
  ssh "$user@$host" "mkdir -p ~/.ssh && cp ~/.ssh/id_rsa* ~/.ssh/backup_$timestamp/ 2>/dev/null || true"
}

# Install new public key on remote host
install_new_key() {
  local host="$1"
  local user="$2"
  local pub_key_path="$3"
  scp "$pub_key_path" "$user@$host":/tmp/new_id_rsa.pub >/dev/null
  ssh "$user@$host" "mkdir -p ~/.ssh && cat /tmp/new_id_rsa.pub >> ~/.ssh/authorized_keys && rm /tmp/new_id_rsa.pub"
}

# Rotate keys for a single host
rotate_host() {
  local host="$1"
  local user="$2"
  local key_dir="$3"
  echo "Rotating keys on $host as $user..."
  backup_keys "$host" "$user"
  install_new_key "$host" "$user" "$key_dir/id_rsa.pub"
}

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <hosts_file> <remote_user>"
  exit 1
fi

HOSTS_FILE="$1"
REMOTE_USER="$2"

if [[ ! -f "$HOSTS_FILE" ]]; then
  echo "Hosts file not found: $HOSTS_FILE"
  exit 1
fi

TMP_KEY_DIR="/tmp/ssh_key_rotator_$$"
generate_key "$TMP_KEY_DIR"

while IFS= read -r host || [[ -n "$host" ]]; do
  # Skip empty lines or comments
  [[ -z "$host" ]] && continue
  [[ "$host" =~ ^# ]] && continue
  rotate_host "$host" "$REMOTE_USER" "$TMP_KEY_DIR"
done < "$HOSTS_FILE"

echo "Key rotation completed. Temporary keys are stored in $TMP_KEY_DIR (you may delete them)."
