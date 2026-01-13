#!/usr/bin/env bash
set -euo pipefail

# Default values
COMMENT="nightly-key"
OUTPUT_DIR="."

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --comment)
      shift
      COMMENT="$1"
      ;;
    --output)
      shift
      OUTPUT_DIR="$1"
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
  shift
done

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Generate a unique key name based on timestamp
TIMESTAMP=$(date +%s%N)
KEY_PATH="$OUTPUT_DIR/nightly_key_$TIMESTAMP"

# Generate the key pair
ssh-keygen -t rsa -b 2048 -N "" -C "$COMMENT" -f "$KEY_PATH" -q

# Output paths
echo "Private key: $KEY_PATH"
echo "Public key: $KEY_PATH.pub"

# Print public key content
cat "$KEY_PATH.pub"
