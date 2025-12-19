#!/usr/bin/env bash
# Test script for labeler.js
# Mock rationale: we simulate GitHub Action environment variables and capture output.

set -e

# Create temporary file to capture GITHUB_OUTPUT
OUTPUT_FILE=$(mktemp)

# Export required env vars for first scenario
export INPUT_TITLE="Add new feature to dashboard"
export GITHUB_OUTPUT="$OUTPUT_FILE"

# Run the labeler script
node src/labeler.js

# Read the output
LABELS=$(grep '^labels=' "$OUTPUT_FILE" | cut -d'=' -f2-)

# Expected label is "enhancement"
if [ "$LABELS" != "enhancement" ]; then
  echo "Test failed: expected 'enhancement' got '$LABELS'"
  exit 1
fi

# Additional test case: bug title
export INPUT_TITLE="Fix critical bug in auth"
> "$OUTPUT_FILE"
node src/labeler.js
LABELS=$(grep '^labels=' "$OUTPUT_FILE" | cut -d'=' -f2-)
if [ "$LABELS" != "bug" ]; then
  echo "Test failed: expected 'bug' got '$LABELS'"
  exit 1
fi

# Additional test case: no keyword
export INPUT_TITLE="Update CI config"
> "$OUTPUT_FILE"
node src/labeler.js
LABELS=$(grep '^labels=' "$OUTPUT_FILE" | cut -d'=' -f2-)
if [ "$LABELS" != "question" ]; then
  echo "Test failed: expected 'question' got '$LABELS'"
  exit 1
fi

echo "All tests passed."
