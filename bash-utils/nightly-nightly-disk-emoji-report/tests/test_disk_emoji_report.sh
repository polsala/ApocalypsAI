#!/usr/bin/env bash

set -euo pipefail

# Create a temporary workspace
TMPDIR=$(mktemp -d)
cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

# Mock df to always report 42% usage
MOCK_BIN="$TMPDIR/mockbin"
mkdir -p "$MOCK_BIN"
cat > "$MOCK_BIN/df" <<'EOF'
#!/usr/bin/env bash
# Mock df: always report 42% usage regardless of arguments
echo "Filesystem 1K-blocks Used Available Use% Mounted on"
echo "/dev/mock 1000000 420000 580000 42% /mock"
EOF
chmod +x "$MOCK_BIN/df"

# Prepend mock bin to PATH so the utility picks it up
export PATH="$MOCK_BIN:$PATH"

# Run the utility on the mocked mount point
OUTPUT=$(bash ../src/disk-emoji-report.sh "/mock")

# Expected output (42% falls into the low‑usage 🟢 bucket)
EXPECTED="Disk usage for /mock: 42% 🟢"
if [[ "$OUTPUT" != "$EXPECTED" ]]; then
  echo "FAIL: expected '$EXPECTED' but got '$OUTPUT'"
  exit 1
fi

echo "PASS"
