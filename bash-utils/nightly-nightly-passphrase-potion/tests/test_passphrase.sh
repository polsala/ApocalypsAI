#!/usr/bin/env bash

# test_passphrase.sh – tests for nightly-passphrase-potion
# -------------------------------------------------------
# This test creates a temporary word list, runs the script with a fixed seed,
# and verifies that the output matches the expected deterministic passphrase.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
SCRIPT="$SCRIPT_DIR/passphrase.sh"

# Create a temporary word list
TMP_WORDS=$(mktemp)
cat > "$TMP_WORDS" <<'EOF'
alpha
bravo
charlie
delta
echo
EOF

# Expected deterministic output with seed=0 and the above list
# Words selected (indices 0,1,2,3) -> Alpha Bravo Charlie Delta
# Symbols selected (indices 0,1,2) -> ! @ #
EXPECTED="Alpha!Bravo@Charlie#Delta"

# Run the script
OUTPUT=$(bash "$SCRIPT" --list "$TMP_WORDS" --seed 0)

# Clean up temporary file
rm -f "$TMP_WORDS"

# Assertion
if [[ "$OUTPUT" == "$EXPECTED" ]]; then
  echo "PASS: deterministic output matches expected"
  exit 0
else
  echo "FAIL: expected '$EXPECTED' but got '$OUTPUT'" >&2
  exit 1
fi
