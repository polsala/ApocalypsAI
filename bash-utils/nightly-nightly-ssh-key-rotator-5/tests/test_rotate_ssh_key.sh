#!/usr/bin/env bash

# Test suite for nightly-ssh-key-rotator
# Uses mock ssh-keygen and ssh-copy-id to avoid side effects.

set -euo pipefail

# Create a temporary sandbox
SANDBOX=$(mktemp -d)
export HOME="$SANDBOX"
mkdir -p "$HOME/.ssh"

# Directory for mock binaries
MOCK_BIN="$SANDBOX/mock_bin"
mkdir -p "$MOCK_BIN"

# Mock ssh-keygen: creates empty key files and logs invocation
cat > "$MOCK_BIN/ssh-keygen" <<'EOF'
#!/usr/bin/env bash
# Log arguments
echo "ssh-keygen $@" >> "$HOME/mock_calls.log"
# Extract -f argument (output file path)
while [[ $# -gt 0 ]]; do
  case $1 in
    -f) KEYFILE=$2; shift 2;;
    *) shift;;
  esac
done
# Create dummy private and public key files
touch "$KEYFILE"
if [[ -n "${KEYFILE}" ]]; then
  echo "dummy-public-key" > "${KEYFILE}.pub"
fi
EOF
chmod +x "$MOCK_BIN/ssh-keygen"

# Mock ssh-copy-id: logs the host and key used
cat > "$MOCK_BIN/ssh-copy-id" <<'EOF'
#!/usr/bin/env bash
# Log arguments
echo "ssh-copy-id $@" >> "$HOME/mock_calls.log"
EOF
chmod +x "$MOCK_BIN/ssh-copy-id"

# Prepend mock bin to PATH
export PATH="$MOCK_BIN:$PATH"

# Path to the script under test
SCRIPT_PATH="$(dirname "$0")/../src/rotate_ssh_key.sh"

# Run the script with mock data
bash "$SCRIPT_PATH" -u testuser -h "hostA hostB" -p "test_key"

# Assertions
# 1. Verify that ssh-keygen was called with the correct -f argument
EXPECTED_KEY="$HOME/.ssh/test_key"
if ! grep -q "ssh-keygen -t rsa -b 2048 -f $EXPECTED_KEY -N \"\" -q" "$HOME/mock_calls.log"; then
  echo "FAIL: ssh-keygen not called with expected arguments" >&2
  exit 1
fi

# 2. Verify that ssh-copy-id was called for each host with the correct key
for host in hostA hostB; do
  if ! grep -q "ssh-copy-id -i $EXPECTED_KEY.pub testuser@$host" "$HOME/mock_calls.log"; then
    echo "FAIL: ssh-copy-id not called correctly for $host" >&2
    exit 1
  fi
done

# 3. Verify that key files exist
if [[ ! -f "$EXPECTED_KEY" || ! -f "$EXPECTED_KEY.pub" ]]; then
  echo "FAIL: Key files were not created" >&2
  exit 1
fi

echo "All tests passed."
