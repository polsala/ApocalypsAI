#!/usr/bin/env bash
set -euo pipefail

# Create a temporary payload file mimicking GitHub issue event
cat > /tmp/payload.json <<'EOF'
{
  "action": "opened",
  "issue": {
    "number": 42,
    "title": "Radiation leak in the bunker",
    "body": "We need a survivor to check the containment."
  }
}
EOF

# Export required environment variables
export EVENT_PAYLOAD="/tmp/payload.json"
export GITHUB_REPOSITORY="example/repo"
export GITHUB_TOKEN="dummy-token"

# Mock curl to capture its arguments without making network calls
function curl() {
  echo "curl called with: $*"
  # Simulate a successful API response
  echo '{"labels":["radiation","survivor"]}'
}
export -f curl

# Run the labeler script
output=$(bash "${PWD}/src/labeler.sh")

# Verify that expected labels are reported
if [[ "$output" == *"Added labels: radiation survivor"* ]]; then
  echo "TEST PASSED: Correct labels added"
  exit 0
else
  echo "TEST FAILED: Unexpected output"
  echo "$output"
  exit 1
fi
