#!/usr/bin/env bash
set -euo pipefail

# Create an isolated temporary environment
TMPDIR=$(mktemp -d)
USER="testuser"
HOME_DIR="${TMPDIR}/${USER}"
SSH_DIR="${HOME_DIR}/.ssh"
mkdir -p "$SSH_DIR"

# Mock an existing authorized_keys file
echo "ssh-ed25519 AAAAoldkey test@example.com" > "${SSH_DIR}/authorized_keys"

# Export a fixed timestamp so the script's output is deterministic
export DATE_NOW=1234567890

# Locate the script relative to this test file
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
bash "${SCRIPT_DIR}/rotate_ssh_keys.sh" -u "$USER" -d "$SSH_DIR"

# ---- Assertions ----
# 1. Backup file should exist with the deterministic timestamp
if [[ ! -f "${SSH_DIR}/authorized_keys.bak.1234567890" ]]; then
  echo "FAIL: Backup file missing"
  exit 1
fi

# 2. New key pair files should exist
if [[ ! -f "${SSH_DIR}/id_ed25519_rotated_1234567890" ]] || [[ ! -f "${SSH_DIR}/id_ed25519_rotated_1234567890.pub" ]]; then
  echo "FAIL: New key files missing"
  exit 1
fi

# 3. authorized_keys must contain the original key and the newly generated public key
if ! grep -q "AAAAoldkey" "${SSH_DIR}/authorized_keys"; then
  echo "FAIL: Original key not preserved in authorized_keys"
  exit 1
fi
if ! grep -q "ssh-ed25519" "${SSH_DIR}/authorized_keys"; then
  echo "FAIL: New public key not appended to authorized_keys"
  exit 1
fi

echo "All tests passed"
