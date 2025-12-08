#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Simulate GitHub environment and capture curl request.

# Create mock event JSON
cat > event.json <<'EOF'
{
  "pull_request": {
    "number": 42,
    "title": "Fix critical bug in parser"
  }
}
EOF

export GITHUB_EVENT_PATH="$(pwd)/event.json"
export GITHUB_REPOSITORY="owner/repo"
export GITHUB_TOKEN="dummy-token"

# Mock curl to capture arguments
CURL_OUTPUT="curl_args.txt"
function curl() {
  echo "$@" > "$CURL_OUTPUT"
  # Simulate successful response
  echo '{"id":1}'
}
export -f curl

# Run the entrypoint script
bash "$(dirname "$0")/../src/entrypoint.sh"

# Verify that the captured data contains the expected label payload
EXPECTED_LABEL='{"labels":["🐛 PR"]}'
if grep -F "$EXPECTED_LABEL" "$CURL_OUTPUT" > /dev/null; then
  echo "Test passed"
  exit 0
else
  echo "Test failed: expected label not found"
  cat "$CURL_OUTPUT"
  exit 1
fi
