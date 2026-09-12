#!/usr/bin/env bash

# nightly-ssh-key-rotator – rotate SSH host keys with backup
# ----------------------------------------------------------
# This script is deliberately lightweight and POSIX‑compatible.
# It expects `ssh-keygen` to be available in $PATH.

set -euo pipefail

# Default values
TARGET_DIR="${HOME}/.ssh"
BACKUP_DIR=""

print_usage() {
  cat <<'EOF'
Usage: rotate_ssh_keys.sh [-d <target_dir>] [-b <backup_dir>] [-h]

Options:
  -d <target_dir>   Directory containing ssh_host_* keys (default: $HOME/.ssh)
  -b <backup_dir>   Directory to store backups (default: <target_dir>/backup)
  -h                Show this help message and exit
EOF
}

# Parse arguments
while getopts ":d:b:h" opt; do
  case $opt in
    d) TARGET_DIR="${OPTARG}" ;;
    b) BACKUP_DIR="${OPTARG}" ;;
    h) print_usage; exit 0 ;;
    \?) echo "Error: Invalid option -${OPTARG}" >&2; print_usage; exit 1 ;;
    :) echo "Error: Option -${OPTARG} requires an argument" >&2; print_usage; exit 1 ;;
  esac
done

# Resolve absolute paths
TARGET_DIR="$(cd "${TARGET_DIR}" && pwd)"
if [[ -z "${BACKUP_DIR}" ]]; then
  BACKUP_DIR="${TARGET_DIR}/backup"
fi
BACKUP_DIR="$(cd "${BACKUP_DIR}" && pwd)"

# Timestamp for this run
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
CURRENT_BACKUP="${BACKUP_DIR}/${TIMESTAMP}"

mkdir -p "${CURRENT_BACKUP}"

# Find existing host keys (private keys only)
shopt -s nullglob
existing_keys=("${TARGET_DIR}"/ssh_host_*_key)
shopt -u nullglob

if (( ${#existing_keys[@]} )); then
  echo "Found ${#existing_keys[@]} existing host key(s). Backing up to ${CURRENT_BACKUP}..."
  for key_path in "${existing_keys[@]}"; do
    base_name="$(basename "${key_path}")"
    mv "${key_path}" "${CURRENT_BACKUP}/${base_name}"
    # Also move the public counterpart if it exists
    if [[ -f "${key_path}.pub" ]]; then
      mv "${key_path}.pub" "${CURRENT_BACKUP}/${base_name}.pub"
    fi
  done
else
  echo "No existing host keys found in ${TARGET_DIR}. Proceeding to generate new keys."
fi

# Generate new RSA host key (you can extend to other types)
NEW_KEY_PATH="${TARGET_DIR}/ssh_host_rsa_key"
echo "Generating new 4096‑bit RSA host key at ${NEW_KEY_PATH}..."
ssh-keygen -t rsa -b 4096 -f "${NEW_KEY_PATH}" -N "" -q

# Ensure proper permissions
chmod 600 "${NEW_KEY_PATH}"
chmod 644 "${NEW_KEY_PATH}.pub"

echo "SSH host key rotation complete."
