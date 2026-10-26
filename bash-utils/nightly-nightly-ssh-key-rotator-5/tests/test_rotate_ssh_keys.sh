#!/usr/bin/env bash

# test_rotate_ssh_keys.sh – validates the behavior of rotate_ssh_keys.sh
# This test runs in a temporary directory and uses a mock `ssh-keygen`
# to avoid generating real cryptographic material.

set -euo pipefail

# Create a temporary workspace
WORKDIR=$(mktemp -d)
cleanup() {
  rm -rf "${WORKDIR}"
}
trap cleanup EXIT

# Directory layout
TARGET="${WORKDIR}/ssh_dir"
BACKUP="${WORKDIR}/backup_dir"
mkdir -p "${TARGET}"

# Place dummy existing keys
echo "old private key" > "${TARGET}/ssh_host_rsa_key"
chmod 600 "${TARGET}/ssh_host_rsa_key"
echo "old public key" > "${TARGET}/ssh_host_rsa_key.pub"
chmod 644 "${TARGET}/ssh_host_rsa_key.pub"

# Mock ssh-keygen – creates placeholder files instead of real keys
MOCK_BIN="${WORKDIR}/mock_bin"
mkdir -p "${MOCK_BIN}"
cat > "${MOCK_BIN}/ssh-keygen" <<'EOF'
#!/usr/bin/env bash
# Simple mock that respects -f <path> and creates two files with dummy content
while (( "$#" )); do
  case "$1" in
    -f) KEY_PATH="$2"; shift 2;;
    *) shift;;
  esac
done
# Create private key placeholder
printf "MOCK PRIVATE KEY" > "${KEY_PATH}"
# Create public key placeholder
printf "MOCK PUBLIC KEY" > "${KEY_PATH}.pub"
EOF
chmod +x "${MOCK_BIN}/ssh-keygen"

# Prepend mock bin to PATH
export PATH="${MOCK_BIN}:$PATH"

# Run the utility
bash "$(pwd)/src/rotate_ssh_keys.sh" -d "${TARGET}" -b "${BACKUP}"

# Assertions
# 1. Backup directory should contain the original files with timestamp subfolder
backup_subdirs=("${BACKUP}"/*)
if (( ${#backup_subdirs[@]} != 1 )); then
  echo "FAIL: Expected exactly one timestamped backup directory" >&2
  exit 1
fi
TIMESTAMP_DIR="${backup_subdirs[0]}"
if [[ ! -f "${TIMESTAMP_DIR}/ssh_host_rsa_key" ]] || [[ ! -f "${TIMESTAMP_DIR}/ssh_host_rsa_key.pub" ]]; then
  echo "FAIL: Original key files not found in backup" >&2
  exit 1
fi
# 2. New key files should exist in the target directory and contain mock data
if [[ ! -f "${TARGET}/ssh_host_rsa_key" ]] || [[ ! -f "${TARGET}/ssh_host_rsa_key.pub" ]]; then
  echo "FAIL: New key files not generated" >&2
  exit 1
fi
if ! grep -q "MOCK PRIVATE KEY" "${TARGET}/ssh_host_rsa_key"; then
  echo "FAIL: New private key does not contain mock content" >&2
  exit 1
fi
if ! grep -q "MOCK PUBLIC KEY" "${TARGET}/ssh_host_rsa_key.pub"; then
  echo "FAIL: New public key does not contain mock content" >&2
  exit 1
fi

echo "All tests passed."
