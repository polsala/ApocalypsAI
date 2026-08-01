#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: simulate GITHUB_EVENT_PATH and GITHUB_TOKEN, capture curl output.

# Create temporary event JSON
cat > event.json <<'EOF'
{
  "issue": {
    "title": "Add new feature for user login",
    "number": 42
  },
  "repository": {
    "full_name": "example/repo"
  }
}
EOF

export GITHUB_EVENT_PATH="$(pwd)/event.json"
export GITHUB_TOKEN="test-token"

# Mock curl to capture request without network access
function curl() {
  # Capture arguments for verification (printed to stdout for test visibility)
  echo "CURL_CALLED $@"
  # Simulate successful JSON response
  echo '{"id":1}'
}
export -f curl

# Run the action script
output=$(bash src/main.sh)

# Verify that the script reported success
if [[ "$output" != *"Posted fortune comment."* ]]; then
  echo "Test failed: unexpected output"
  exit 1
fi

echo "Test passed"
