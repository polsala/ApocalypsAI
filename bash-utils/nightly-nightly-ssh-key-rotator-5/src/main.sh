#!/usr/bin/env bash
set -euo pipefail

# Default values
USER_NAME=""
HOSTS=""

# Parse arguments
while getopts "u:h:" opt; do
  case $opt in
    u) USER_NAME="$OPTARG" ;;
    h) HOSTS="$OPTARG" ;;
    *) echo "Usage: $0 -u <user> -h <host_dir1,host_dir2,...>" >&2; exit 1 ;;
  esac
done

if [[ -z "$HOSTS" ]]; then
  echo "Error: host list required (-h)" >&2
  exit 1
fi

# Generate new RSA key pair if not already present
KEY_PRIV="$HOME/.ssh/id_rsa_rotated"
KEY_PUB="${KEY_PRIV}.pub"
if [[ ! -f "$KEY_PRIV" ]]; then
  mkdir -p "$(dirname "$KEY_PRIV")"
  ssh-keygen -t rsa -b 2048 -f "$KEY_PRIV" -N "" -C "rotated-key" >/dev/null
fi

# Distribute public key and purge old key
IFS=',' read -ra HOST_ARR <<< "$HOSTS"
for HOST_DIR in "${HOST_ARR[@]}"; do
  AUTH_FILE="${HOST_DIR}/.ssh/authorized_keys"
  mkdir -p "$(dirname "$AUTH_FILE")"
  # Ensure file exists
  touch "$AUTH_FILE"
  # Append new public key
  cat "$KEY_PUB" >> "$AUTH_FILE"
  # Remove any line containing the marker OLDKEY
  grep -v "OLDKEY" "$AUTH_FILE" > "${AUTH_FILE}.tmp"
  mv "${AUTH_FILE}.tmp" "$AUTH_FILE"
done

echo "SSH key rotation complete for user $USER_NAME on ${#HOST_ARR[@]} host(s)."
