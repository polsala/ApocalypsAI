#!/usr/bin/env bash
set -e

# Prepare mock event payload
cat > event.json <<'EOF'
{
  "number": 42,
  "updated_at": "2023-01-01T00:00:00Z"
}
EOF

export GITHUB_EVENT_PATH="$(pwd)/event.json"
export INPUT_DAYS="10"
export INPUT_LABEL="needs-attention"
export INPUT_EMOJI="⚠️"

# Capture output
OUTPUT=$(bash ./src/labeler.sh)

# Expected substring
EXPECTED="Would label #42 with '⚠️ needs-attention' after 10 days of inactivity."

if [[ "$OUTPUT" == *"$EXPECTED"* ]]; then
  echo "Test passed"
  exit 0
else
  echo "Test failed"
  echo "Got: $OUTPUT"
  exit 1
fi
