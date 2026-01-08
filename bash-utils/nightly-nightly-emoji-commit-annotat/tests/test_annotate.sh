#!/usr/bin/env bash
set -euo pipefail

# Path to the script under test
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
SCRIPT="$SCRIPT_DIR/annotate.sh"

# Create a temporary input file
cat > /tmp/input.txt <<'EOF'
Fix bug in parser
Add new feature
Update docs
EOF

# Expected output (emojis cycle in order)
read -r -d '' EXPECTED <<'EOS'
🚀 Fix bug in parser
✨ Add new feature
🔥 Update docs
EOS

# Run the script
OUTPUT="$(bash "$SCRIPT" /tmp/input.txt)"

if [[ "$OUTPUT" != "$EXPECTED" ]]; then
  echo "Test failed"
  echo "Expected:"
  echo "$EXPECTED"
  echo "Got:"
  echo "$OUTPUT"
  exit 1
fi

echo "All tests passed"
