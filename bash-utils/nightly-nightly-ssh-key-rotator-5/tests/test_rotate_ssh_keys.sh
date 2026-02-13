#!/usr/bin/env bash
set -euo pipefail

# Create temporary directory for mocks and test files
TMPDIR=$(mktemp -d)
cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

# Mock ssh-keygen
cat > "$TMPDIR/ssh-keygen" <<'EOF'
#!/usr/bin/env bash
# Mock ssh-keygen: create dummy private and public key files
while [[ $# -gt 0 ]]; do
  case "$1" in
    -f) KEYFILE="$2"; shift 2;;
    *) shift;;
  esac
done
echo "MOCK_PRIVATE_KEY" > "$KEYFILE"
echo "MOCK_PUBLIC_KEY" > "${KEYFILE}.pub"
EOF
chmod +x "$TMPDIR/ssh-keygen"

# Mock ssh-copy-id
cat > "$TMPDIR/ssh-copy-id" <<'EOF'
#!/usr/bin/env bash
# Mock ssh-copy-id: log host and key file
while [[ $# -gt 0 ]]; do
  case "$1" in
    -i) KEYFILE="$2"; shift 2;;
    *) HOST="$1"; shift;;
  esac
done
echo "$HOST $(cat \"$KEYFILE\")" >> "$HOME/ssh_copy_id_log.txt"
EOF
chmod +x "$TMPDIR/ssh-copy-id"

# Prepare mock hosts file
HOSTS_FILE="$TMPDIR/hosts.txt"
printf "host1.example.com\nhost2.example.com\n" > "$HOSTS_FILE"

# Ensure log file is empty
> "$HOME/ssh_copy_id_log.txt"

# Prepend mock bin to PATH
export PATH="$TMPDIR:$PATH"

# Run the script
bash "$(dirname \"$0\")/../src/rotate_ssh_keys.sh" "$HOSTS_FILE" "$TMPDIR/id_rsa_test"

# Verify that both hosts were logged with the mock public key
if grep -q "host1.example.com MOCK_PUBLIC_KEY" "$HOME/ssh_copy_id_log.txt" && \
   grep -q "host2.example.com MOCK_PUBLIC_KEY" "$HOME/ssh_copy_id_log.txt"; then
  echo "PASS"
else
  echo "FAIL"
  exit 1
fi
