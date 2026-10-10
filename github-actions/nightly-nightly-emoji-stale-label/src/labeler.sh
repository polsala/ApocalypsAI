#!/usr/bin/env bash
set -e

# Default inputs
DAYS="${INPUT_DAYS:-30}"
LABEL="${INPUT_LABEL:-stale}"
EMOJI="${INPUT_EMOJI:-🧟}"

# Mock rationale: In a real action we would parse GITHUB_EVENT_PATH JSON to get issue number and updated_at.
# For this demo, we simply output a message.

# Retrieve issue/PR number from event payload if available
if [[ -f "$GITHUB_EVENT_PATH" ]]; then
  # Extract number using grep (simple mock)
  NUMBER=$(grep -o '"number": *[0-9]*' "$GITHUB_EVENT_PATH" | head -1 | grep -o '[0-9]*')
else
  NUMBER="UNKNOWN"
fi

echo "Would label #${NUMBER} with '${EMOJI} ${LABEL}' after ${DAYS} days of inactivity."
