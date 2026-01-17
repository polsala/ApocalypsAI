#!/usr/bin/env bash
set -euo pipefail

# Test script for nightly-todo-prioritizer
# Creates a temporary TODO file, runs the sorter, and checks the output.

SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
UTIL="../src/priority_sort.sh"

# Create a temporary input file
TMP_INPUT=$(mktemp)
cat > "$TMP_INPUT" <<'EOF'
Buy milk [P2]
Fix critical bug [P1]
Read book
Write documentation [P3]
EOF

# Expected sorted output
read -r -d '' EXPECTED <<'EOE'
Fix critical bug [P1]
Buy milk [P2]
Write documentation [P3]
Read book
EOE

# Run the utility
OUTPUT=$("$UTIL" "$TMP_INPUT")

if [[ "$OUTPUT" != "$EXPECTED" ]]; then
  echo "Test FAILED"
  echo "--- Expected ---"
  echo "$EXPECTED"
  echo "--- Got ---"
  echo "$OUTPUT"
  exit 1
fi

echo "All tests passed"
