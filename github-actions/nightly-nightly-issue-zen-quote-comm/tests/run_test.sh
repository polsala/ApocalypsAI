#!/usr/bin/env bash
set -euo pipefail

# Mock curl to capture its arguments without making a network request
CURL_LOG=$(mktemp)
function curl() {
  echo "curl called with args: $@" >> "$CURL_LOG"
  # Simulate a successful GitHub API response
  echo '{"id":1,"url":"https://api.github.com/..."}'
}
export -f curl

# Fix the random seed so the first quote is always selected
export RANDOM=0

# Create a mock GitHub event payload representing a newly opened issue
EVENT_JSON=$(mktemp)
cat > "$EVENT_JSON" <<'EOF'
{
  "issue": {
    "number": 42
  }
}
EOF
export GITHUB_EVENT_PATH="$EVENT_JSON"
export GITHUB_REPOSITORY="owner/repo"
export GITHUB_TOKEN="dummy-token"

# Execute the action script
bash "$(dirname "$0")/../src/main.sh"

# Verify that curl was invoked with the expected URL and payload containing the first quote
EXPECTED_QUOTE="The journey of a thousand miles begins with one step."
if grep -q "\"body\":\"$EXPECTED_QUOTE\"" "$CURL_LOG"; then
  echo "Test passed: expected quote was sent"
  exit 0
else
  echo "Test failed: expected quote not found in curl call"
  echo "--- curl log ---"
  cat "$CURL_LOG"
  exit 1
fi
