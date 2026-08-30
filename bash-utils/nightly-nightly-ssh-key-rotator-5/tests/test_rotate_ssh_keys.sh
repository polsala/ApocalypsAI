#!/usr/bin/env bash
set -euo pipefail

# Create temporary directory for isolation
TMPDIR=$(mktemp -d)
cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

# Prepare dummy old key files
OLD_KEY="$TMPDIR/id_rsa"
OLD_PUB="${OLD_KEY}.pub"
echo "dummy private key" > "$OLD_KEY"
chmod 600 "$OLD_KEY"
echo "dummy public key" > "$OLD_PUB"
chmod 644 "$OLD_PUB"

# Locate the rotator script relative to this test file
SCRIPT_DIR="$(cd "$(dirname "$0")/../src" && pwd)"
"$SCRIPT_DIR/rotate_ssh_keys.sh" "$OLD_KEY"

# Verify that timestamped backups were created
if ! ls "${OLD_KEY}.bak."* > /dev/null 2>&1; then
  echo "Backup private key not found"
  exit 1
fi
if ! ls "${OLD_KEY}.pub.bak."* > /dev/null 2>&1; then
  echo "Backup public key not found"
  exit 1
fi

# Verify that a new key was generated (content differs from dummy)
if grep -q "dummy private key" "$OLD_KEY"; then
  echo "New private key was not generated"
  exit 1
fi

echo "All tests passed"
