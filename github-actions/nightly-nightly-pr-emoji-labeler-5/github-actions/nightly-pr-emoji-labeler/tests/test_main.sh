#!/usr/bin/env bash
set -euo pipefail

# Mock environment variables
export GITHUB_TOKEN="dummy-token"
export KEYWORD_EMOJI_MAP='{"fix":"🔧","feat":"✨"}'

# Create a mock GitHub event payload (PR title contains the keyword "feat")
cat > event.json <<'EOF'
{
  "pull_request": {
    "title": "feat: add new widget"
  }
}
EOF
export GITHUB_EVENT_PATH="$(pwd)/event.json"

# Define where the action should write its outputs (GitHub runner sets this)
export GITHUB_OUTPUT="$(pwd)/output.txt"

# Ensure the script is executable
chmod +x "$(pwd)/src/main.sh"

# Run the action script
bash "$(pwd)/src/main.sh"

# Verify the output
EXPECTED="emoji=✨"
ACTUAL=$(cat "$GITHUB_OUTPUT")
if [[ "$ACTUAL" == "$EXPECTED" ]]; then
  echo "Test passed"
  exit 0
else
  echo "Test failed: expected '$EXPECTED' but got '$ACTUAL'"
  exit 1
fi
