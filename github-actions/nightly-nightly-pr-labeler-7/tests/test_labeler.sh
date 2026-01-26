#!/usr/bin/env bash
set -euo pipefail

# Create a temporary directory for the mock event file
TMPDIR=$(mktemp -d)
cat > "$TMPDIR/event.json" <<'EOF'
{
  "files": [
    {"filename": "README.md"},
    {"filename": "src/app.py"},
    {"filename": "tests/test_example.py"}
  ]
}
EOF

# Export the path so the script can find it
export GITHUB_EVENT_PATH="$TMPDIR/event.json"
# Dummy token (not used in the script but required by the action metadata)
export GITHUB_TOKEN="dummy-token"

# Capture the script output
OUTPUT=$(bash src/labeler.sh)

# Expected deterministic output (labels are sorted alphabetically)
EXPECTED="Labels to add: 🐍 python‑whirl 🧪 test‑tornado 📚 docs‑drift"

if [[ "$OUTPUT" != "$EXPECTED" ]]; then
  echo "Test failed. Expected: '$EXPECTED' Got: '$OUTPUT'"
  exit 1
fi

echo "Test passed."
