#!/usr/bin/env bash
set -euo pipefail

# Mock curl to capture calls and provide fake responses
declare -a CURL_CALLS=()
function curl() {
  local args=("$@")
  CURL_CALLS+=("${args[*]}")
  if [[ "${args[*]}" == *"/issues/42"* && "${args[*]}" != *"-X POST"* ]]; then
    # Mock GET issue response with labels
    cat <<'EOF'
{
  "labels": [
    {"name": "enhancement"},
    {"name": "help wanted"}
  ]
}
EOF
  elif [[ "${args[*]}" == *"/reactions"* && "${args[*]}" == *"-X POST"* ]]; then
    # Mock POST reaction response
    echo '{"id":1}'
  else
    echo '{}'
  fi
}
export -f curl

# Set environment variables for the action
export GITHUB_TOKEN="dummy-token"
export ISSUE_NUMBER=42
export REPO="owner/repo"
export LABEL_EMOJI_MAP='{"bug":"+1","enhancement":"rocket"}'

# Execute the script (path relative to repo root)
bash src/run.sh

# Verify that a POST to the reactions endpoint was made with the correct emoji
found=0
for call in "${CURL_CALLS[@]}"; do
  if [[ "$call" == *"/reactions"* && "$call" == *'"content":"rocket"'* ]]; then
    found=1
    break
  fi
 done

if [[ $found -eq 1 ]]; then
  echo "TEST PASSED"
  exit 0
else
  echo "TEST FAILED: rocket reaction not sent"
  exit 1
fi

