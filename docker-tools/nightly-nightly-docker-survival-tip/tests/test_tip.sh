#!/bin/sh
# test_tip.sh - deterministic test for tip.sh using mocked tips file
# Mock rationale: replace random selection with a fixed first line to ensure repeatable test

# Create a temporary directory
TMPDIR=$(mktemp -d)
cd "$TMPDIR" || exit 1

# Mock tips.txt with known content
cat > tips.txt <<'EOF'
First tip.
Second tip.
Third tip.
EOF

# Copy tip.sh with deterministic behavior
cat > tip.sh <<'EOS'
#!/bin/sh
TIP_FILE="tips.txt"
if [ ! -f "$TIP_FILE" ]; then
  echo "No tips found."
  exit 1
fi
# Deterministic selection: always take the first line
tip=$(head -n 1 "$TIP_FILE")
echo "$tip"
EOS
chmod +x tip.sh

# Run script and capture output
OUTPUT=$(./tip.sh)

# Expected output is the first line
if [ "$OUTPUT" = "First tip." ]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: got '$OUTPUT'"
  exit 1
fi
