#!/usr/bin/env bash
set -euo pipefail

# Directory of this script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$DIR/.." && pwd)"

# Create mock nc
MOCK_BIN="$DIR/mock_bin"
mkdir -p "$MOCK_BIN"
cat > "$MOCK_BIN/nc" <<'EOF'
#!/usr/bin/env bash
# Mock nc: succeed if host contains "good", fail otherwise
HOST=$1
PORT=$2
if [[ "$HOST" == *good* ]]; then
  exit 0
else
  exit 1
fi
EOF
chmod +x "$MOCK_BIN/nc"

# Prepend mock to PATH
export PATH="$MOCK_BIN:$PATH"

# Test 1: mixed hosts
"$ROOT/src/main.sh" good.example.com bad.example.com
CODE=$?
if [[ $CODE -ne 1 ]]; then
  echo "Test 1 failed: expected exit 1, got $CODE"
  exit 1
fi

# Test 2: all good
"$ROOT/src/main.sh" good1.example.com good2.example.com
CODE=$?
if [[ $CODE -ne 0 ]]; then
  echo "Test 2 failed: expected exit 0, got $CODE"
  exit 1
fi

echo "All tests passed."
