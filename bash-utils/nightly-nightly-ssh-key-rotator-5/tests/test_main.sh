#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------------------
# Test suite for nightly-ssh-key-rotator (bash-utils)
# ---------------------------------------------------------------------------
# This test does NOT invoke real ssh-keygen. Instead we mock it to create
# placeholder files, ensuring the script's logic works offline.
# ---------------------------------------------------------------------------

# Load the utility script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
source "${SCRIPT_DIR}/main.sh"

# ---------------------------------------------------------------------------
# Mock ssh-keygen – creates dummy key files instead of real cryptographic keys
# ---------------------------------------------------------------------------
mock_ssh_keygen() {
  local outfile=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -f) outfile="$2"; shift 2;;
      *) shift;;
    esac
  done
  # Create placeholder private and public key files
  echo "PRIVATE KEY" > "${outfile}"
  echo "PUBLIC KEY" > "${outfile}.pub"
}
export -f mock_ssh_keygen
SSH_KEYGEN_CMD=mock_ssh_keygen

# ---------------------------------------------------------------------------
# Prepare a temporary directory to act as the SSH key location
# ---------------------------------------------------------------------------
TMPDIR=$(mktemp -d)
export KEY_DIR="${TMPDIR}"

# Create existing dummy RSA key files to test backup behavior
echo "old private" > "${KEY_DIR}/ssh_host_rsa_key"
echo "old public" > "${KEY_DIR}/ssh_host_rsa_key.pub"

# ---------------------------------------------------------------------------
# Execute the rotation function (direct call, not via CLI)
# ---------------------------------------------------------------------------
rotate_ssh_key rsa

# ---------------------------------------------------------------------------
# Assertions – simple checks that files exist where expected
# ---------------------------------------------------------------------------
# New key files must exist
if [[ ! -f "${KEY_DIR}/ssh_host_rsa_key" ]]; then
  echo "FAIL: New private key not found"
  exit 1
fi
if [[ ! -f "${KEY_DIR}/ssh_host_rsa_key.pub" ]]; then
  echo "FAIL: New public key not found"
  exit 1
fi
# Backup files must exist with a timestamp suffix
backup_private=$(ls "${KEY_DIR}/ssh_host_rsa_key.bak_"* 2>/dev/null || true)
backup_public=$(ls "${KEY_DIR}/ssh_host_rsa_key.pub.bak_"* 2>/dev/null || true)
if [[ -z "$backup_private" ]]; then
  echo "FAIL: Backup of private key missing"
  exit 1
fi
if [[ -z "$backup_public" ]]; then
  echo "FAIL: Backup of public key missing"
  exit 1
fi

# Verify that the backup files contain the original content
if ! grep -q "old private" "$backup_private"; then
  echo "FAIL: Backup private key content mismatch"
  exit 1
fi
if ! grep -q "old public" "$backup_public"; then
  echo "FAIL: Backup public key content mismatch"
  exit 1
fi

# Verify that the new key files contain the mock content
if ! grep -q "PRIVATE KEY" "${KEY_DIR}/ssh_host_rsa_key"; then
  echo "FAIL: New private key content mismatch"
  exit 1
fi
if ! grep -q "PUBLIC KEY" "${KEY_DIR}/ssh_host_rsa_key.pub"; then
  echo "FAIL: New public key content mismatch"
  exit 1
fi

echo "All tests passed"
