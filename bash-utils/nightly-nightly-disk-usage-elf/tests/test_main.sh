#!/usr/bin/env bash
# Test suite for nightly-disk-usage-elf
set -e

# Create a temporary directory to hold the mock df binary.
TMPDIR=$(mktemp -d)

# Mock df that outputs a fixed table.
cat > "$TMPDIR/df" <<'EOF'
Filesystem     1K-blocks    Used Available Use% Mounted on
/dev/sda1       1000000  950000   50000  95% /
/dev/sda2        500000   10000  490000   2% /home
EOF
chmod +x "$TMPDIR/df"

# Prepend the mock directory to PATH so that the script picks it up.
export PATH="$TMPDIR:$PATH"

# Run the utility and capture its output.
OUTPUT=$(bash ../src/main.sh)

# Expected lines.
EXPECTED_WARNING="⚠️  / is at 95%"
EXPECTED_OK="✅  /home is at 2%"

# Verify that both expected lines appear.
if ! echo "$OUTPUT" | grep -q "$EXPECTED_WARNING"; then
  echo "Missing warning line: $EXPECTED_WARNING"
  exit 1
fi
if ! echo "$OUTPUT" | grep -q "$EXPECTED_OK"; then
  echo "Missing ok line: $EXPECTED_OK"
  exit 1
fi

# Verify that the ASCII elf is present (since a warning exists).
if ! echo "$OUTPUT" | grep -q "Time to clean up"; then
  echo "Elf not printed despite warning"
  exit 1
fi

echo "All tests passed."
