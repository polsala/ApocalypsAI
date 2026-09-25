#!/usr/bin/env bash
set -euo pipefail

# Create temporary directory
TMPDIR=$(mktemp -d)
cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

# Create mock private keys (empty files)
touch "$TMPDIR/key_rsa_1024"
touch "$TMPDIR/key_rsa_4096"

# Create a mock ssh-keygen that returns predetermined sizes
MOCK_SSH_KEYGEN="$TMPDIR/mock_ssh_keygen.sh"
cat > "$MOCK_SSH_KEYGEN" <<'EOF'
#!/usr/bin/env bash
# Mock ssh-keygen -lf <file>
case "$1" in
  *key_rsa_1024) echo "1024 SHA256:AAAAB3NzaC1yc2EAAAADAQABAAABAQC... $1 (RSA)";;
  *key_rsa_4096) echo "4096 SHA256:BBBBB3NzaC1yc2EAAAADAQABAAABAQD... $1 (RSA)";;
  *) echo ""; exit 1;;
esac
EOF
chmod +x "$MOCK_SSH_KEYGEN"

# Prepend mock to PATH
export PATH="$TMPDIR:$PATH"

# Run the script, capture exit code (expect weak key detection -> exit 1)
if ./src/ssh_key_audit.sh "$TMPDIR"; then
  echo "Test failed: expected non-zero exit due to weak key"
  exit 1
else
  code=$?
  if [[ $code -ne 1 ]]; then
    echo "Test failed: expected exit code 1, got $code"
    exit 1
  fi
fi

# Now test with only strong key
rm "$TMPDIR/key_rsa_1024"
if ./src/ssh_key_audit.sh "$TMPDIR"; then
  echo "Strong key test passed"
else
  echo "Test failed: expected success exit"
  exit 1
fi

echo "All tests passed"
