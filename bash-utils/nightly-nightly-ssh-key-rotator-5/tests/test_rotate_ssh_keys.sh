#!/usr/bin/env bash
set -euo pipefail

# Directory for temporary test artifacts
TMPDIR=$(mktemp -d)
cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

# Create mock bin directory and prepend to PATH
MOCKBIN="$TMPDIR/mockbin"
mkdir -p "$MOCKBIN"
export PATH="$MOCKBIN:$PATH"

# Mock ssh-keygen: creates dummy key files with predictable content
cat > "$MOCKBIN/ssh-keygen" <<'EOF'
#!/usr/bin/env bash
# Mock rationale: simulate ssh-keygen without cryptographic operations
while [[ $# -gt 0 ]]; do
  case $1 in
    -f) KEYFILE="$2"; shift 2;;
    -N) shift;;
    -t) shift;;
    -q) shift;;
    *) shift;;
  esac
done
# Write placeholder private and public keys
printf 'MOCK_PRIVATE_KEY' > "$KEYFILE"
printf 'MOCK_PUBLIC_KEY' > "${KEYFILE}.pub"
EOF
chmod +x "$MOCKBIN/ssh-keygen"

# Mock ssh-copy-id: record calls to a log file
LOGFILE="$TMPDIR/ssh_copy_id.log"
cat > "$MOCKBIN/ssh-copy-id" <<'EOF'
#!/usr/bin/env bash
# Mock rationale: capture arguments for verification
printf '%s\n' "$@" >> "${LOGFILE}"
EOF
chmod +x "$MOCKBIN/ssh-copy-id"

# Prepare test inputs
KEYDIR="$TMPDIR/ssh"
mkdir -p "$KEYDIR"
# Simulate an existing key to test backup logic
printf 'OLD_PRIVATE' > "$KEYDIR/id_ed25519"
printf 'OLD_PUBLIC' > "$KEYDIR/id_ed25519.pub"

HOSTFILE="$TMPDIR/hosts.txt"
cat > "$HOSTFILE" <<'EOF'
host1.example.com
host2.example.com
# comment line should be ignored

EOF

# Run the utility
bash ./src/rotate_ssh_keys.sh -u testuser -h "$HOSTFILE" -d "$KEYDIR"

# Assertions
# 1. Old key should be backed up with timestamp suffix
BACKUP_COUNT=$(ls "$KEYDIR"/id_ed25519_old_* 2>/dev/null | wc -l)
if [[ $BACKUP_COUNT -ne 1 ]]; then
  echo "FAIL: Expected exactly one backup file, found $BACKUP_COUNT" >&2
  exit 1
fi

# 2. New key files should exist and contain mock data
if [[ $(cat "$KEYDIR/id_ed25519") != "MOCK_PRIVATE_KEY" ]]; then
  echo "FAIL: New private key content mismatch" >&2
  exit 1
fi
if [[ $(cat "$KEYDIR/id_ed25519.pub") != "MOCK_PUBLIC_KEY" ]]; then
  echo "FAIL: New public key content mismatch" >&2
  exit 1
fi

# 3. ssh-copy-id should have been called for each non‑comment host
EXPECTED_CALLS=2
ACTUAL_CALLS=$(wc -l < "$LOGFILE")
if [[ $ACTUAL_CALLS -ne $EXPECTED_CALLS ]]; then
  echo "FAIL: Expected $EXPECTED_CALLS ssh-copy-id calls, got $ACTUAL_CALLS" >&2
  exit 1
fi

# Verify that the arguments contain the correct user and host
grep -q "-i $KEYDIR/id_ed25519.pub" "$LOGFILE"
grep -q "testuser@host1.example.com" "$LOGFILE"
grep -q "testuser@host2.example.com" "$LOGFILE"

echo "All tests passed."
