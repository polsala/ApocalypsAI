#!/usr/bin/env bash
set -euo pipefail

# Mock ssh-keygen to avoid real key generation
mock_ssh_keygen() {
  local key_path="$1"
  # Create dummy private key
  echo "MOCK PRIVATE KEY" > "${key_path}"
  # Create dummy public key
  echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMockPublicKey" > "${key_path}.pub"
}
export -f mock_ssh_keygen

# Override ssh-keygen in PATH with a lightweight wrapper that calls the mock
MOCK_BIN_DIR="$(mktemp -d)"
cat > "${MOCK_BIN_DIR}/ssh-keygen" <<'EOF'
#!/usr/bin/env bash
# Simple wrapper that extracts the -f argument and forwards to mock_ssh_keygen
while [[ $# -gt 0 ]]; do
  case "$1" in
    -f) key_path="$2"; shift 2 ;;
    *) shift ;;
  esac
done
mock_ssh_keygen "$key_path"
EOF
chmod +x "${MOCK_BIN_DIR}/ssh-keygen"
export PATH="${MOCK_BIN_DIR}:$PATH"

# Create a temporary HOME with a .ssh directory
TMP_HOME="$(mktemp -d)"
export HOME="$TMP_HOME"
mkdir -p "$HOME/.ssh"

# Populate an existing authorized_keys file
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIoldkey old@example.com" > "$HOME/.ssh/authorized_keys"

# Locate the utility script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
bash "${SCRIPT_DIR}/rotate_ssh_keys.sh"

# Verify that authorized_keys now contains the mock public key
if ! grep -q "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMockPublicKey" "$HOME/.ssh/authorized_keys"; then
  echo "Test failed: new public key not installed" >&2
  exit 1
fi

# Verify that a backup file was created
BACKUP_FILE=$(ls "$HOME/.ssh"/authorized_keys.bak.* 2>/dev/null || true)
if [[ -z "$BACKUP_FILE" ]]; then
  echo "Test failed: backup file not created" >&2
  exit 1
fi

# Verify that the backup still contains the old key
if ! grep -q "old@example.com" "$BACKUP_FILE"; then
  echo "Test failed: backup does not contain old key" >&2
  exit 1
fi

echo "All tests passed."
