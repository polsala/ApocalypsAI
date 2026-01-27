#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Test that entrypoint.sh constructs correct API call and comment.

# Create temporary directory
TMPDIR=$(mktemp -d)
cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

# Mock GITHUB_EVENT_PATH JSON (not actually parsed by jq in this test)
cat > "$TMPDIR/event.json" <<'EOF'
{
  "pull_request": {
    "number": 42,
    "title": "Fix time distortion"
  },
  "repository": {
    "full_name": "example/repo"
  }
}
EOF

export GITHUB_EVENT_PATH="$TMPDIR/event.json"
export GITHUB_TOKEN="dummy-token"

# Mock jq to return expected values
jq() {
  local opt=$1
  local query=$2
  local file=$3
  case "$query" in
    .pull_request.number) echo "42" ;;
    .pull_request.title) echo "Fix time distortion" ;;
    .repository.full_name) echo "example/repo" ;;
    *) echo "" ;;
  esac
}

# Capture curl arguments
CURL_OUTPUT="$TMPDIR/curl_args.txt"
curl() {
  echo "URL:$1" >> "$CURL_OUTPUT"
  shift
  while (( "$#" )); do
    echo "ARG:$1" >> "$CURL_OUTPUT"
    shift
  done
}

# Source the script (it will execute)
source "$(dirname "${BASH_SOURCE[0]}")/../src/entrypoint.sh"

# Verify output
if ! grep -q "URL:https://api.github.com/repos/example/repo/issues/42/comments" "$CURL_OUTPUT"; then
  echo "Test failed: API URL not as expected"
  exit 1
fi
if ! grep -q "ARG:-d" "$CURL_OUTPUT"; then
  echo "Test failed: POST data not sent"
  exit 1
fi
if ! grep -q "Congratulations on merging PR #42: Fix time distortion! Keep the apocalypse at bay!" "$CURL_OUTPUT"; then
  echo "Test failed: Comment body not as expected"
  exit 1
fi

echo "All tests passed."
