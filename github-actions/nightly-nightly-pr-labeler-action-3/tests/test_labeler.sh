#!/usr/bin/env bash
set -euo pipefail

# Mock the gh CLI so no network call is made
function gh() {
  echo "gh mock called with args: $*"
}
export -f gh

# Create a temporary directory for the fake event payload
tmpdir=$(mktemp -d)
cat > "$tmpdir/event.json" <<'EOF'
{
  "pull_request": {
    "title": "Add new feature for user login",
    "number": 42
  },
  "repository": {
    "full_name": "example/repo"
  }
}
EOF

export GITHUB_EVENT_PATH="$tmpdir/event.json"
# Provide a custom mapping that includes the keyword "feature"
export INPUT_LABEL_MAPPING='{"feature":"enhancement","bug":"bug"}'

# Capture the script output
output=$(bash src/labeler.sh)

# Verify that the expected label was mentioned in the output
if [[ "$output" == *"Mock add label 'enhancement'"* ]]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: unexpected output"
  echo "$output"
  exit 1
fi
