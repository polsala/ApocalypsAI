#!/usr/bin/env bash

# Test suite for nightly-ssh-key-rotator
# -------------------------------------------------------

set -euo pipefail

# Create a temporary workspace
WORKDIR=$(mktemp -d)
KEY_DIR="$WORKDIR/ssh_keys"
BACKUP_DIR="$WORKDIR/backup"
MOCK_BIN="$WORKDIR/mock_bin"

mkdir -p "$KEY_DIR" "$BACKUP_DIR" "$MOCK_BIN"

# Create dummy existing host keys
for name in rsa ecdsa ed25519; do
  touch "$KEY_DIR/ssh_host_${name}_key"
  touch "$KEY_DIR/ssh_host_${name}_key.pub"
done

# Mock ssh-keygen to avoid real key generation
cat > "$MOCK_BIN/ssh-keygen" <<'EOF'
#!/usr/bin/env bash
# Mock ssh-keygen: just create empty files matching the requested output name
while [[ $# -gt 0 ]]; do
  case "$1" in
    -f) shift; outfile="$1";;
    *) ;;
  esac
  shift
done
mkdir -p "$(dirname "$outfile")"
> "$outfile"
> "${outfile}.pub"
EOF
chmod +x "$MOCK_BIN/ssh-keygen"

# Mock systemctl and service to capture restart attempts
cat > "$MOCK_BIN/systemctl" <<'EOF'
#!/usr/bin/env bash
echo "[mock] systemctl $*"
EOF
chmod +x "$MOCK_BIN/systemctl"

cat > "$MOCK_BIN/service" <<'EOF'
#!/usr/bin/env bash
echo "[mock] service $*"
EOF
chmod +x "$MOCK_BIN/service"

# Prepend mock bin to PATH
export PATH="$MOCK_BIN:$PATH"

# Export a fixed timestamp for reproducible backup naming
export APOCALYPSE_TIMESTAMP="20230101120000"

# Run the script in dry‑run mode (so no real file changes)
SCRIPT_PATH="$(dirname "$0")/../src/rotate_ssh_keys.sh"
OUTPUT=$(bash "$SCRIPT_PATH" --key-dir "$KEY_DIR" --backup-dir "$BACKUP_DIR" --dry-run)

# Expected substrings in the output
expectations=(
  "[dry‑run] mkdir -p $BACKUP_DIR"
  "[dry‑run] mkdir -p $BACKUP_DIR/ssh_host_keys_20230101120000.bak"
  "[dry‑run] cp -a $KEY_DIR/ssh_host_* $BACKUP_DIR/ssh_host_keys_20230101120000.bak/"
  "[dry‑run] ssh-keygen -t rsa -f $KEY_DIR/ssh_host_rsa_key -N  -q"
  "[dry‑run] ssh-keygen -t ecdsa -f $KEY_DIR/ssh_host_ecdsa_key -N  -q"
  "[dry‑run] ssh-keygen -t ed25519 -f $KEY_DIR/ssh_host_ed25519_key -N  -q"
  "[dry‑run] systemctl restart sshd"
)

for exp in "${expectations[@]}"; do
  if ! grep -F "$exp" <<< "$OUTPUT"; then
    echo "Test failed: expected line not found -> $exp" >&2
    exit 1
  fi
done

echo "All tests passed."
