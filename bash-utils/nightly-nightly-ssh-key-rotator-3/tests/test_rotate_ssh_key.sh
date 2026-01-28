#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------
# Test suite for nightly-ssh-key-rotator
# ------------------------------------------------------------

# Create a temporary sandbox
SANDBOX=$(mktemp -d)
export SANDBOX

# Mock ssh-keygen that creates deterministic key files
MOCK_BIN="${SANDBOX}/mock_bin"
mkdir -p "${MOCK_BIN}"
cat > "${MOCK_BIN}/ssh-keygen" <<'EOF'
#!/usr/bin/env bash
# Mock ssh-keygen: creates predictable private and public key files
# Expected args: -t rsa -b 2048 -f <key_path> -C <comment> -N ""
while [[ $# -gt 0 ]]; do
  case "$1" in
    -f) KEY_PATH="$2"; shift 2;;
    -C) COMMENT="$2"; shift 2;;
    *) shift;;
  esac
done
# Write deterministic private key
cat > "${KEY_PATH}" <<'PRIV'
-----BEGIN RSA PRIVATE KEY-----
MOCKPRIVATEKEY
-----END RSA PRIVATE KEY-----
PRIV
# Write deterministic public key (comment is included for realism)
cat > "${KEY_PATH}.pub" <<EOF
ssh-rsa MOCKPUBLICKEY ${COMMENT}
EOF
exit 0
EOF
chmod +x "${MOCK_BIN}/ssh-keygen"

# Prepend mock bin to PATH
export PATH="${MOCK_BIN}:$PATH"

# Set up a fake user home directory
FAKE_HOME="${SANDBOX}/home/testuser"
mkdir -p "${FAKE_HOME}/.ssh"
# Populate an existing authorized_keys file
cat > "${FAKE_HOME}/.ssh/authorized_keys" <<'OLDKEY'
ssh-rsa OLDKEY old@example.com
OLDKEY

# Run the rotator script (using the sandboxed home)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
chmod +x "${SCRIPT_DIR}/rotate_ssh_key.sh"
# Override HOME for the script to point to our sandbox (script uses /home/<user>)
# Create the expected /home path inside sandbox
mkdir -p "${SANDBOX}/home/testuser"
ln -s "${FAKE_HOME}" "${SANDBOX}/home/testuser"
# Execute
"${SCRIPT_DIR}/rotate_ssh_key.sh" "testuser" "test-comment"

# Assertions
AUTH_KEYS="${FAKE_HOME}/.ssh/authorized_keys"
BACKUP="${AUTH_KEYS}.bak"

# 1. Backup file exists and contains the old key
if ! grep -q "OLDKEY" "${BACKUP}"; then
  echo "FAIL: Backup does not contain original key"
  exit 1
fi

# 2. authorized_keys now contains the mock public key with the provided comment
if ! grep -q "MOCKPUBLICKEY test-comment" "${AUTH_KEYS}"; then
  echo "FAIL: authorized_keys does not contain new mock public key"
  exit 1
fi

# 3. No leftover old key in authorized_keys
if grep -q "OLDKEY" "${AUTH_KEYS}"; then
  echo "FAIL: Old key still present in authorized_keys"
  exit 1
fi

echo "PASS: All tests succeeded"
