#!/usr/bin/env bash

# test_rotate_ssh_keys.sh
# Offline test suite for nightly-ssh-key-rotator.
# Uses a mock ssh-keygen to avoid external dependencies.

set -euo pipefail

# Create a temporary working directory
WORKDIR=$(mktemp -d)
SSH_DIR="$WORKDIR/ssh_dir"
BACKUP_DIR="$WORKDIR/backup_dir"
MOCK_BIN="$WORKDIR/mock_bin"

mkdir -p "$SSH_DIR" "$BACKUP_DIR" "$MOCK_BIN"

# ----- Mock ssh-keygen -----------------------------------------------------
# The mock writes deterministic dummy key files.
cat > "$MOCK_BIN/ssh-keygen" <<'EOF'
#!/usr/bin/env bash
# Mock ssh-keygen: arguments are ignored except for -f <private_key_path>
# It creates a dummy private key and a matching public key.
while [[ $# -gt 0 ]]; do
  case $1 in
    -f) PRIVATE="$2"; shift 2;;
    *) shift;;
  esac
done
# Write dummy private key
printf "MOCK PRIVATE KEY\n" > "$PRIVATE"
# Write dummy public key (same base name with .pub)
printf "MOCK PUBLIC KEY\n" > "${PRIVATE}.pub"
EOF
chmod +x "$MOCK_BIN/ssh-keygen"
# Ensure the mock is found before the real binary
export PATH="$MOCK_BIN:$PATH"

# ----- Prepare existing keys to be backed up -------------------------------
# Create placeholder old keys (they can be empty; the script only copies them)
printf "OLD PRIVATE KEY\n" > "$SSH_DIR/ssh_host_ed25519_key"
printf "OLD PUBLIC KEY\n" > "$SSH_DIR/ssh_host_ed25519_key.pub"

# ----- Run the utility -----------------------------------------------------
SCRIPT_PATH="../src/rotate_ssh_keys.sh"
# Change to workdir to avoid path issues
pushd "$WORKDIR" > /dev/null
bash "$SCRIPT_PATH" -d "$SSH_DIR" -b "$BACKUP_DIR"
popd > /dev/null

# ----- Assertions ----------------------------------------------------------
# 1. Backup directory should contain a subdirectory with the old keys
BACKUP_SUBDIR=$(find "$BACKUP_DIR" -mindepth 1 -maxdepth 1 -type d | head -n1)
if [[ -z "$BACKUP_SUBDIR" ]]; then
  echo "FAIL: No backup subdirectory created" >&2
  exit 1
fi
if [[ ! -f "$BACKUP_SUBDIR/ssh_host_ed25519_key" || ! -f "$BACKUP_SUBDIR/ssh_host_ed25519_key.pub" ]]; then
  echo "FAIL: Old keys not found in backup" >&2
  exit 1
fi

# 2. New keys should exist in the SSH directory and contain the mock content
if [[ ! -f "$SSH_DIR/ssh_host_ed25519_key" || ! -f "$SSH_DIR/ssh_host_ed25519_key.pub" ]]; then
  echo "FAIL: New keys not generated" >&2
  exit 1
fi
if ! grep -q "MOCK PRIVATE KEY" "$SSH_DIR/ssh_host_ed25519_key"; then
  echo "FAIL: New private key does not contain mock data" >&2
  exit 1
fi
if ! grep -q "MOCK PUBLIC KEY" "$SSH_DIR/ssh_host_ed25519_key.pub"; then
  echo "FAIL: New public key does not contain mock data" >&2
  exit 1
fi

# 3. Fingerprint output should be printed (the mock fingerprint will be empty but the script should still output a line)
# Capture the script output for verification
OUTPUT=$(bash "$SCRIPT_PATH" -d "$SSH_DIR" -b "$BACKUP_DIR" 2>/dev/null)
if ! echo "$OUTPUT" | grep -q "New host key fingerprint"; then
  echo "FAIL: Fingerprint line not printed" >&2
  exit 1
fi

echo "All tests passed."
