#!/usr/bin/env bash
set -euo pipefail

# Create a temporary directory for the mock environment
TMPDIR=$(mktemp -d)
cd "$TMPDIR"

# Mock gh CLI to capture its arguments instead of performing real API calls
export MOCK_GH_LOG=$(mktemp)
cat > mock_gh <<'EOF'
#!/usr/bin/env bash
# Append all received arguments to the log file for later inspection
echo "$@" >> "$MOCK_GH_LOG"
EOF
chmod +x mock_gh
export PATH="$PWD:$PATH"

# Create a fake GitHub event payload (PR title contains "feat")
cat > event.json <<'EOF'
{
  "pull_request": {
    "number": 42,
    "title": "feat: add magical feature"
  }
}
EOF
export GITHUB_EVENT_PATH="$PWD/event.json"
export GITHUB_REPOSITORY="example/repo"

# Run the labeler script (relative path assumes we are inside the utility folder)
bash "../src/label_pr.sh"

# Verify that the mock gh was invoked with the expected label
if grep -q "pr edit 42 --add-label feature" "$MOCK_GH_LOG"; then
  echo "PASS"
  exit 0
else
  echo "FAIL"
  exit 1
fi
