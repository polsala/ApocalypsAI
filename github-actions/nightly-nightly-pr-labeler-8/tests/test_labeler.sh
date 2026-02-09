#!/usr/bin/env bash
set -euo pipefail

# Mock curl to capture request without making network calls
CURL_OUTPUT=$(mktemp)
function curl() {
  echo "curl called with: $@" >> "$CURL_OUTPUT"
  # Simulate a successful JSON response
  echo '{"id":1}'
}
export -f curl

# Prepare mock event JSON
EVENT_JSON=$(mktemp)
cat > "$EVENT_JSON" <<'EOF'
{
  "pull_request": {
    "title": "Add new feature for documentation",
    "number": 42
  },
  "repository": {
    "full_name": "example/repo"
  }
}
EOF

export GITHUB_EVENT_PATH="$EVENT_JSON"
export GITHUB_TOKEN="dummy-token"

# Run the labeler script
bash "$(dirname "$0")/../src/labeler.sh"

# Verify that curl was called with the expected label payload
EXPECTED_LABELS='["feature","docs","emoji-🚀"]'
if grep -q "$EXPECTED_LABELS" "$CURL_OUTPUT"; then
  echo "Test passed"
  exit 0
else
  echo "Test failed: expected labels $EXPECTED_LABELS"
  cat "$CURL_OUTPUT"
  exit 1
fi
