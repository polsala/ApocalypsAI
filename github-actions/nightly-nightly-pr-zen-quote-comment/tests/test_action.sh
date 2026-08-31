#!/usr/bin/env bash
set -euo pipefail

# Mock curl to capture its arguments instead of performing a network request
CURL_LOG=$(mktemp)
function curl() {
  echo "$@" > "$CURL_LOG"
}
export -f curl

# Export required environment variables for the action
export GITHUB_TOKEN="dummy-token"
export GITHUB_REPOSITORY="owner/repo"
export PR_NUMBER="42"
export GITHUB_API_URL="https://api.github.com"
# Seed RANDOM to make selection deterministic (first quote)
RANDOM=0

# Run the script under test
./src/post_zen.sh

# Read captured curl command
captured=$(cat "$CURL_LOG")

# Expected quote (first in the list)
expected_quote="The journey of a thousand miles begins with one step."
expected_payload=$(printf '{"body":"%s"}' "$expected_quote")
expected_url="https://api.github.com/repos/owner/repo/issues/42/comments"

# Verify URL
if [[ "$captured" != *"$expected_url"* ]]; then
  echo "FAIL: Expected URL $expected_url not found in curl call"
  exit 1
fi

# Verify payload
if [[ "$captured" != *"-d $expected_payload"* ]]; then
  echo "FAIL: Expected payload $expected_payload not found in curl call"
  exit 1
fi

# Clean up
rm -f "$CURL_LOG"

echo "All tests passed!"
