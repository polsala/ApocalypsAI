#!/usr/bin/env bash
set -euo pipefail

# Create a temporary directory
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

# Path to the script
SCRIPT="./src/main.sh"

# Run the script with a custom comment
COMMENT="test-comment"
"$SCRIPT" --comment "$COMMENT" --output "$TMP_DIR"

# Check that private key file exists
PRIVATE_KEY="$TMP_DIR/nightly_key_*"
PRIVATE_KEY=$(echo $PRIVATE_KEY | head -n 1)
if [[ ! -f "$PRIVATE_KEY" ]]; then
  echo "Private key file not found" >&2
  exit 1
fi

# Check that public key file exists
PUBLIC_KEY="${PRIVATE_KEY}.pub"
if [[ ! -f "$PUBLIC_KEY" ]]; then
  echo "Public key file not found" >&2
  exit 1
fi

# Check that public key contains the comment
if ! grep -q "$COMMENT" "$PUBLIC_KEY"; then
  echo "Public key does not contain the comment" >&2
  exit 1
fi

# Check that public key starts with ssh-rsa
if ! grep -q "^ssh-rsa" "$PUBLIC_KEY"; then
  echo "Public key does not start with ssh-rsa" >&2
  exit 1
fi

echo "All tests passed"
