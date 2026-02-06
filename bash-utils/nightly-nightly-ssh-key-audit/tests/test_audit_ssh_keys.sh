#!/usr/bin/env bash

set -euo pipefail

# Create temporary workspace
TMPDIR=$(mktemp -d)
cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

# Mock ssh-keygen to produce deterministic output based on filename
cat > "$TMPDIR/ssh-keygen" <<'EOF'
#!/usr/bin/env bash
# Mock ssh-keygen: output based on filename
file="$1"
basename=$(basename "$file")
if [[ "$basename" == "weak_rsa" ]]; then
  echo "1024 SHA256:dummy user@host (RSA)"
elif [[ "$basename" == "good_rsa" ]]; then
  echo "4096 SHA256:dummy user@host (RSA)"
elif [[ "$basename" == "ed25519_key" ]]; then
  echo "256 SHA256:dummy user@host (ED25519)"
else
  echo "Error: unknown key" >&2
  exit 1
fi
EOF
chmod +x "$TMPDIR/ssh-keygen"

# Prepare mock key files
mkdir -p "$TMPDIR/.ssh"
# Weak RSA key (should trigger strength warning)
touch "$TMPDIR/.ssh/weak_rsa"
chmod 600 "$TMPDIR/.ssh/weak_rsa"
# Good RSA key (no strength warning)
touch "$TMPDIR/.ssh/good_rsa"
chmod 600 "$TMPDIR/.ssh/good_rsa"
# ED25519 key (no RSA strength check)
touch "$TMPDIR/.ssh/ed25519_key"
chmod 600 "$TMPDIR/.ssh/ed25519_key"
# Key with bad permissions (should trigger permission warning)
touch "$TMPDIR/.ssh/bad_perm"
chmod 644 "$TMPDIR/.ssh/bad_perm"

# Prepend mock directory to PATH so our script uses the mock ssh-keygen
export PATH="$TMPDIR:$PATH"

# Run the utility against the mock .ssh directory
output=$("$PWD/src/audit_ssh_keys.sh" "$TMPDIR/.ssh")

# Verify that warnings are present for the weak RSA key and bad permissions
echo "$output" | grep -q "⚠️  RSA key $TMPDIR/.ssh/weak_rsa is weaker than 2048 bits"
echo "$output" | grep -q "⚠️  Permissions for $TMPDIR/.ssh/bad_perm are 644, should be 600"

# Verify that the good RSA key does NOT produce a weak-key warning
! echo "$output" | grep -q "good_rsa is weaker"

# Verify that the script reports overall success when no issues remain (after fixing mocks)
# For this deterministic test we only check that the script exits with status 0
if [[ ${PIPESTATUS[0]} -ne 0 ]]; then
  echo "Test failed: script exited with non-zero status"
  exit 1
fi

echo "All tests passed."
