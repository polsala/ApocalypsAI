#!/usr/bin/env bash
set -euo pipefail

# Mock curl to capture arguments
captured_url=""
captured_data=""
mock_curl() {
  local method=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -X) shift; method=$1 ;;&n      -H) shift; ;;&n      -d) shift; captured_data=$1 ;;&n      *) if [[ "$1" =~ ^https:// ]]; then captured_url=$1; fi ;;&n    esac
    shift
  done
  echo "mock curl called"
}
export -f mock_curl
alias curl=mock_curl

# Set deterministic environment
export PR_NUMBER=7
export GITHUB_TOKEN=dummy
export REPO=owner/repo

# Run the entrypoint
bash src/entrypoint.sh

# Compute expected quote index
seed=$PR_NUMBER
a=1664525
c=1013904223
m=4294967296
rand=$(((seed * a + c) % m))

total=$(wc -l < quotes.txt)
index=$(( (rand % total) + 1 ))
expected_quote=$(sed -n "${index}p" quotes.txt)
escaped_expected=${expected_quote//"/\"}
expected_payload="{\"body\":\"$escaped_expected\"}"
expected_url="https://api.github.com/repos/$REPO/issues/$PR_NUMBER/comments"

if [[ "$captured_url" != "$expected_url" ]]; then
  echo "FAIL: URL mismatch"
  echo "got: $captured_url"
  echo "expected: $expected_url"
  exit 1
fi

if [[ "$captured_data" != "$expected_payload" ]]; then
  echo "FAIL: payload mismatch"
  echo "got: $captured_data"
  echo "expected: $expected_payload"
  exit 1
fi

echo "PASS"

