#!/usr/bin/env bash
set -euo pipefail

# Setup temporary directory for mocks
TMPDIR=$(mktemp -d)
export PATH="$TMPDIR:$PATH"

# Mock gh CLI (supports only the subset used by the action)
cat > "$TMPDIR/gh" <<'EOF'
#!/usr/bin/env bash
# Simple mock for gh CLI
# Supports: pr view <num> --json files -q '.files[].path'
#          pr edit <num> --add-label <label>
if [[ "$1" == "pr" && "$2" == "view" ]]; then
  cat <<JSON
{
  "files": [
    {"path": "docs/README.md"},
    {"path": "src/main.py"},
    {"path": "tests/test_main.py"},
    {"path": ".github/workflows/ci.yml"}
  ]
}
JSON
elif [[ "$1" == "pr" && "$2" == "edit" ]]; then
  echo "gh edit called with: $@" >> "$TMPDIR/gh_calls.log"
else
  echo "Unsupported gh command: $@" >&2
  exit 1
fi
EOF
chmod +x "$TMPDIR/gh"

# Create fake event payload
EVENT_JSON='{"number":42}'
export GITHUB_EVENT_PATH="$TMPDIR/event.json"
echo "$EVENT_JSON" > "$GITHUB_EVENT_PATH"

# Run the labeler script (relative path assumes this test resides in tests/)
bash "$(dirname "$0")/../src/labeler.sh"

# Verify that gh edit was called with expected labels
EXPECTED_LABELS=("docs" "code" "tests" "ci")
for label in "${EXPECTED_LABELS[@]}"; do
  if ! grep -q "--add-label $label" "$TMPDIR/gh_calls.log"; then
    echo "Missing label $label"
    exit 1
  fi
done

echo "All labels applied correctly"
