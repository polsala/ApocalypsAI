#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Override curl to return fixture JSON without network calls.
MOCK_DIR=$(mktemp -d)
cat > "$MOCK_DIR/curl" <<'EOF'
#!/usr/bin/env bash
# Simple mock curl that ignores arguments and prints fixture JSON
cat "$(dirname "$0")/issues_fixture.json"
EOF
chmod +x "$MOCK_DIR/curl"
export PATH="$MOCK_DIR:$PATH"

# Provide required env vars
export GITHUB_TOKEN="dummy"
export GITHUB_REPOSITORY="owner/repo"

# Create fixture JSON
cat > "$MOCK_DIR/issues_fixture.json" <<'EOF'
[
  {
    "number": 1,
    "title": "Fix login bug",
    "labels": [{"name": "bug"}]
  },
  {
    "number": 2,
    "title": "Add dark mode",
    "labels": [{"name": "enhancement"}]
  },
  {
    "number": 3,
    "title": "Update docs",
    "labels": []
  }
]
EOF

# Determine script location relative to this test file
SCRIPT_PATH="$(dirname "$0")/../src/generate_summary.sh"

# Run the script
output=$(bash "$SCRIPT_PATH")

# Expected output
read -r -d '' expected <<'EOM'
# Open Issues Summary

## bug
- #1 Fix login bug

## enhancement
- #2 Add dark mode

## No Label
- #3 Update docs

EOM

# Compare
if [[ "$output" == "$expected" ]]; then
  echo "Test passed"
  exit 0
else
  echo "Test failed"
  echo "Expected:"
  echo "$expected"
  echo "Got:"
  echo "$output"
  exit 1
fi
