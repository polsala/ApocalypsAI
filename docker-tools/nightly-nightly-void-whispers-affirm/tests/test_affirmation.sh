#!/bin/bash

# Mock rationale: We simulate Docker output by directly invoking the script
OUTPUT=$(sh src/entrypoint.sh)

if [ -z "$OUTPUT" ]; then
  echo "FAIL: No output received"
  exit 1
fi

echo "PASS: Affirmation received: $OUTPUT"
