#!/bin/bash

# Mock rationale: Create a temporary file to simulate user input without filesystem dependencies.
TEST_FILE="test_input.txt"
TEST_OUTPUT="test_input.txt.salvaged.tar.gz"

# Setup
echo "Launch codes: 42-8-42-99" > "$TEST_FILE"

# Run salvage
bash src/salvage.sh "$TEST_FILE"

# Verify output
if [ -f "$TEST_OUTPUT" ]; then
  echo "PASS: Salvaged archive created."
else
  echo "FAIL: Salvaged archive missing."
  exit 1
fi

# Verify checksum
if [ -f "$TEST_OUTPUT.sha256" ]; then
  echo "PASS: Checksum file created."
else
  echo "FAIL: Checksum file missing."
  exit 1
fi

# Cleanup
rm -f "$TEST_FILE" "$TEST_OUTPUT" "$TEST_OUTPUT.sha256"
