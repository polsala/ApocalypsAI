#!/usr/bin/env bash
set -euo pipefail

# Load the script functions without triggering the automatic execution block
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
source "${SCRIPT_DIR}/rotate_ssh_keys.sh"

# Mock ssh-keygen to avoid real key generation
mock_ssh_keygen() {
  local keyfile=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -f)
        keyfile="$2"
        shift 2
        ;;
      -N| -q)
        shift
        ;;
      *)
        shift
        ;;
    esac
  done
  # Create dummy key files
  echo "MOCK PRIVATE KEY" > "${keyfile}"
  echo "MOCK PUBLIC KEY" > "${keyfile}.pub"
}
export -f mock_ssh_keygen
alias ssh-keygen=mock_ssh_keygen

# Create a temporary workspace
TMPDIR="$(mktemp -d)"
KEY_PATH="${TMPDIR}/ssh_host_test_key"

# Simulate an existing key pair
echo "OLD PRIVATE" > "${KEY_PATH}"
echo "OLD PUBLIC" > "${KEY_PATH}.pub"

# Invoke the rotation logic directly
rotate_key

# Verify that the new key files contain the mock content
if [[ "$(cat "${KEY_PATH}")" != "MOCK PRIVATE KEY" ]]; then
  echo "FAIL: New private key not generated correctly"
  exit 1
fi
if [[ "$(cat "${KEY_PATH}.pub")" != "MOCK PUBLIC KEY" ]]; then
  echo "FAIL: New public key not generated correctly"
  exit 1
fi

# Locate the backup directory (should be the only one matching the pattern)
BACKUP_DIR=$(ls -d "${TMPDIR}/backup_"*)
if [[ -z "${BACKUP_DIR}" || ! -d "${BACKUP_DIR}" ]]; then
  echo "FAIL: Backup directory was not created"
  exit 1
fi

# Verify that the old keys were backed up
if [[ "$(cat "${BACKUP_DIR}/$(basename "${KEY_PATH}")")" != "OLD PRIVATE" ]]; then
  echo "FAIL: Old private key not backed up"
  exit 1
fi
if [[ "$(cat "${BACKUP_DIR}/$(basename "${KEY_PATH}").pub")" != "OLD PUBLIC" ]]; then
  echo "FAIL: Old public key not backed up"
  exit 1
fi

echo "PASS"
