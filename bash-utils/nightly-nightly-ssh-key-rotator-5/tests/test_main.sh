#!/usr/bin/env bash
set -euo pipefail

# Create temporary host directories
TMP_ROOT=$(mktemp -d)
HOST1="${TMP_ROOT}/host1"
HOST2="${TMP_ROOT}/host2"
mkdir -p "${HOST1}/.ssh" "${HOST2}/.ssh"

# Initialize authorized_keys with old key marker
echo "OLDKEY" > "${HOST1}/.ssh/authorized_keys"
echo "OLDKEY" > "${HOST2}/.ssh/authorized_keys"

# Run the rotator
bash ../../src/main.sh -u testuser -h "${HOST1},${HOST2}"

# Verify new key files exist
if [[ ! -f "$HOME/.ssh/id_rsa_rotated" ]]; then
  echo "FAIL: private key not created"
  exit 1
fi
if [[ ! -f "$HOME/.ssh/id_rsa_rotated.pub" ]]; then
  echo "FAIL: public key not created"
  exit 1
fi

# Verify authorized_keys updated
for HOST in "${HOST1}" "${HOST2}"; do
  if grep -q "OLDKEY" "${HOST}/.ssh/authorized_keys"; then
    echo "FAIL: OLDKEY still present in ${HOST}"
    exit 1
  fi
  if ! grep -q "^ssh-rsa " "${HOST}/.ssh/authorized_keys"; then
    echo "FAIL: new public key missing in ${HOST}"
    exit 1
  fi
done

echo "All tests passed."
