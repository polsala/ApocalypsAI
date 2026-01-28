#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------
# nightly-ssh-key-rotator
# Rotates a user's SSH authorized_keys by generating a new RSA key pair.
# ------------------------------------------------------------

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <username> [key_comment]"
  exit 1
fi

USER_NAME="$1"
KEY_COMMENT="${2:-rotated-key}"

SSH_DIR="/home/${USER_NAME}/.ssh"
if [[ ! -d "${SSH_DIR}" ]]; then
  echo "Error: SSH directory ${SSH_DIR} does not exist."
  exit 1
fi

AUTH_KEYS="${SSH_DIR}/authorized_keys"
BACKUP="${AUTH_KEYS}.bak"

# Backup existing authorized_keys if present
if [[ -f "${AUTH_KEYS}" ]]; then
  cp "${AUTH_KEYS}" "${BACKUP}"
fi

# Generate a new RSA key pair (private key is left on disk)
TIMESTAMP=$(date +%s)
KEY_PATH="${SSH_DIR}/id_rsa_rotated_${TIMESTAMP}"
ssh-keygen -t rsa -b 2048 -f "${KEY_PATH}" -C "${KEY_COMMENT}" -N "" > /dev/null 2>&1

# Replace authorized_keys with the newly generated public key
cat "${KEY_PATH}.pub" > "${AUTH_KEYS}"

echo "Rotated SSH key for ${USER_NAME}. New public key installed in authorized_keys."
