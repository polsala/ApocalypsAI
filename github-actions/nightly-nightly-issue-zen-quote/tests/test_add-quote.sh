#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Simulate GitHub environment and capture the curl request without making a network call.

# Create a temporary event payload
cat > event.json <<'EOF'
{
  "repository": {
    "full_name": "owner/repo"
  },
  "issue": {
    "number": 42
  }
}
EOF

export GITHUB_EVENT_PATH="$(pwd)/event.json"
export GITHUB_REPOSITORY="owner/repo"
export GITHUB_TOKEN="dummy-token"

# Mock curl to capture arguments
capture_file="$(pwd)/captured.txt"
export CURL_CMD="bash -c 'cat > $capture_file'"

# Run the script
bash "$(pwd)/src/add-quote.sh"

# Verify that captured payload contains a known quote
if grep -q '"body":"' "$capture_file"; then
  echo "Test passed: comment payload captured"
else
  echo "Test failed: comment payload not captured"
  exit 1
fi

# Clean up
rm -f event.json captured.txt
