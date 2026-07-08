#!/usr/bin/env bash
set -euo pipefail

# Print usage information and exit
usage() {
  echo "Usage: $0 <ssh-key-path>"
  exit 1
}

# Ensure exactly one argument is supplied
if [[ $# -ne 1 ]]; then
  usage
fi

KEY_PATH="$1"
KEY_DIR="$(dirname "$KEY_PATH")"
KEY_BASE="$(basename "$KEY_PATH")"
TIMESTAMP="$(date +%Y%m%d%H%M%S)"
BACKUP_DIR="${KEY_DIR}/backup_${TIMESTAMP}"

rotate_key() {
  mkdir -p "$BACKUP_DIR"
  # Backup existing private key if present
  if [[ -f "${KEY_PATH}" ]]; then
    cp "${KEY_PATH}" "${BACKUP_DIR}/${KEY_BASE}"
  fi
  # Backup existing public key if present
  if [[ -f "${KEY_PATH}.pub" ]]; then
    cp "${KEY_PATH}.pub" "${BACKUP_DIR}/${KEY_BASE}.pub"
  fi
  # Generate a new key pair (no passphrase)
  ssh-keygen -q -N "" -f "${KEY_PATH}"
}

# If the script is executed directly, perform rotation and report
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  rotate_key
  echo "Key rotated. New key: ${KEY_PATH}"
  echo "Backup stored in: ${BACKUP_DIR}"
fi
