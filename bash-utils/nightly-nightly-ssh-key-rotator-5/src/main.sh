#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------------------
# nightly-ssh-key-rotator – rotate SSH host keys with timestamped backups.
# ---------------------------------------------------------------------------
# Environment variables (can be overridden for testing):
#   SSH_KEYGEN_CMD – command used to generate keys (default: ssh-keygen)
#   KEY_DIR        – directory containing the host keys (default: /etc/ssh)
# ---------------------------------------------------------------------------

# Default command and key directory
SSH_KEYGEN_CMD="${SSH_KEYGEN_CMD:-ssh-keygen}"
KEY_DIR="${KEY_DIR:-/etc/ssh}"

# Generate a timestamp for backup filenames
TIMESTAMP=$(date +%Y%m%d%H%M%S)

rotate_ssh_key() {
  local key_type="${1:-rsa}"
  local key_path="${KEY_DIR}/ssh_host_${key_type}_key"
  local pub_path="${key_path}.pub"
  local backup_key="${key_path}.bak_${TIMESTAMP}"
  local backup_pub="${pub_path}.bak_${TIMESTAMP}"

  # -----------------------------------------------------------------------
  # Step 1: Backup existing keys if they exist
  # -----------------------------------------------------------------------
  if [[ -f "${key_path}" ]]; then
    mv "${key_path}" "${backup_key}"
    echo "Backed up existing private key to ${backup_key}"
  fi
  if [[ -f "${pub_path}" ]]; then
    mv "${pub_path}" "${backup_pub}"
    echo "Backed up existing public key to ${backup_pub}"
  fi

  # -----------------------------------------------------------------------
  # Step 2: Generate a new key pair (no passphrase)
  # -----------------------------------------------------------------------
  local new_key_tmp="${key_path}_new"
  "$SSH_KEYGEN_CMD" -q -N "" -t "${key_type}" -f "${new_key_tmp}"

  # -----------------------------------------------------------------------
  # Step 3: Move the newly generated keys into place
  # -----------------------------------------------------------------------
  mv "${new_key_tmp}" "${key_path}"
  mv "${new_key_tmp}.pub" "${pub_path}"

  echo "Rotated ${key_type} host key. New key is at ${key_path}"
}

# ---------------------------------------------------------------------------
# If the script is executed directly, run the rotation with provided args.
# ---------------------------------------------------------------------------
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  rotate_ssh_key "$@"
fi
