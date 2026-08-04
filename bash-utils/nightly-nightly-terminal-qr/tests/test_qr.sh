#!/usr/bin/env bash
# Test for nightly-terminal-qr

set -euo pipefail

# Create temporary directory for mock
TMPDIR=$(mktemp -d)
cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

# Mock qrencode
cat > "$TMPDIR/qrencode" <<'EOF'
#!/usr/bin/env bash
# Mock qrencode: ignore args, output fixed pattern
cat <<'MOCK'
██
██
MOCK
EOF
chmod +x "$TMPDIR/qrencode"

# Prepend mock to PATH
export PATH="$TMPDIR:$PATH"

# Run the script
OUTPUT=$(bash -c 'src/qr.sh "any text"' 2>/dev/null)

# Expected output
EXPECTED="██
██"

if [[ "$OUTPUT" != "$EXPECTED" ]]; then
  echo "Test failed: output did not match expected."
  echo "Got:"
  echo "$OUTPUT"
  echo "Expected:"
  echo "$EXPECTED"
  exit 1
fi

echo "Test passed."
