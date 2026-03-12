#!/bin/bash

# This script selects a random line from a given file.

MESSAGES_FILE="$1"

if [ ! -f "$MESSAGES_FILE" ]; then
  echo "Error: Messages file not found at '$MESSAGES_FILE'" >&2
  exit 1
fi

# Read all messages into an array
mapfile -t MESSAGES < "$MESSAGES_FILE"

NUM_MESSAGES=${#MESSAGES[@]}

if [ "$NUM_MESSAGES" -eq 0 ]; then
  echo "Error: No messages found in '$MESSAGES_FILE'" >&2
  exit 1
fi

# Use a deterministic seed for testing if available, otherwise use current time
# Mock rationale: For deterministic tests, we need to control the random number generation.
# This allows tests to pass consistently without relying on actual randomness.
if [ -n "$TEST_SEED" ]; then
  RANDOM="$TEST_SEED"
fi

# Generate a random index
RANDOM_INDEX=$(( RANDOM % NUM_MESSAGES ))

# Output the selected message
echo "${MESSAGES[$RANDOM_INDEX]}"
