#!/usr/bin/env bash
set -euo pipefail

# Mock data
export MOCK_MODE=1
export MOCK_BRANCHES='[
  {"name":"feature/old-idea"},
  {"name":"feature/recent"},
  {"name":"main"}
]'

# PR search mock returns a merged PR for old-idea (old date) and a non‑merged PR for recent
export MOCK_PR_RESPONSE='{
  "items": [
    {
      "state":"closed",
      "pull_request": {"merged_at":"2023-01-01T12:00:00Z"}
    },
    {
      "state":"open",
      "pull_request": {"merged_at":null}
    }
  ]
}'

# Set environment variables expected by the script
export GITHUB_TOKEN="dummy"
export DAYS_OLD="365"
export GITHUB_REPOSITORY="owner/repo"

# Run the cleanup script
output=$(bash ../src/cleanup.sh)

# Expected output line
expected="🗑️ Farewell, \`feature/old-idea\`! May your code rest in peace."

if echo "$output" | grep -q "$expected"; then
  echo "Test passed"
  exit 0
else
  echo "Test failed"
  echo "Output was:"
  echo "$output"
  exit 1
fi
