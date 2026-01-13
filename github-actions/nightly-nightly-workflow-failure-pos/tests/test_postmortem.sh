#!/usr/bin/env bash
set -euo pipefail

# Mock curl to capture request
function curl() {
  echo "curl called with args: $@"
  # Simulate successful response
  echo '{"html_url":"https://github.com/owner/repo/issues/1"}'
}
export -f curl

# Set environment variables for test
export GITHUB_TOKEN="test-token"
export GITHUB_REPOSITORY="owner/repo"
export GITHUB_RUN_ID="12345"
export GITHUB_WORKFLOW="CI"
export GITHUB_SERVER_URL="https://github.com"

# Run script
output=$(bash "$(dirname "$0")/../postmortem.sh")

# Verify that curl was called
if [[ "$output" == *"curl called with args:"* ]]; then
  echo "Test passed"
  exit 0
else
  echo "Test failed"
  exit 1
fi
