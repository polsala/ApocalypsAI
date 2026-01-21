#!/usr/bin/env bash
set -euo pipefail

# Mock GITHUB_EVENT_PATH
EVENT_FILE=$(mktemp)
cat > "$EVENT_FILE" <<'EOF'
{
  "pull_request": {
    "title": "Add new feature for user login"
  }
}
EOF
export GITHUB_EVENT_PATH="$EVENT_FILE"

# Run the script with a sample mapping
OUTPUT=$(bash ./src/label_pr.sh $'feat:enhancement\nbug:bug')
expected="::add-label::enhancement"

if [[ "$OUTPUT" != "$expected" ]]; then
  echo "Test failed: expected '$expected', got '$OUTPUT'"
  exit 1
fi

echo "Test passed"
