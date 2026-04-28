#!/usr/bin/env bash
set -euo pipefail

# Mock curl to capture its arguments without performing a network request
CURL_OUTPUT=""
mock_curl() {
  local method=""
  local url=""
  local data=""
  while (( "$#" )); do
    case "$1" in
      -X)
        method="$2"
        shift 2
        ;;
      -H)
        shift 2 # ignore headers
        ;;
      -d)
        data="$2"
        shift 2
        ;;
      *)
        if [[ -z "$url" ]]; then
          url="$1"
        fi
        shift
        ;;
    esac
  done
  CURL_OUTPUT="METHOD=$method URL=$url DATA=$data"
}
export -f mock_curl

# Override curl with our mock
alias curl=mock_curl

# Create a temporary event JSON file mimicking a pull_request event
EVENT_JSON='{"pull_request":{"number":42}}'
export GITHUB_EVENT_PATH=$(mktemp)
echo "$EVENT_JSON" > "$GITHUB_EVENT_PATH"

# Set required environment variables for the script
export GITHUB_REPOSITORY="owner/repo"
export GITHUB_TOKEN="fake-token"
export LABEL="auto-label"

# Execute the script under test
bash "$(dirname "$0")/../src/label_pr.sh"

# Expected curl invocation
expected="METHOD=POST URL=https://api.github.com/repos/owner/repo/issues/42/labels DATA={\"labels\":[\"auto-label\"]}"

if [[ "$CURL_OUTPUT" != "$expected" ]]; then
  echo "Test failed: expected '$expected' but got '$CURL_OUTPUT'"
  exit 1
fi

echo "Test passed."
