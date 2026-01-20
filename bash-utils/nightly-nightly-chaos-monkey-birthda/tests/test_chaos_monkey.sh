#!/bin/bash

# Mock rationale: We simulate directory and file structure using temporary directories and files.

set -e

TEMP_DIR=$(mktemp -d)

echo "Creating mock files..."
for i in {1..3}; do
  touch "$TEMP_DIR/file$i.txt"
done

echo "Running chaos_monkey.sh on mock directory..."
OUTPUT=$(./src/chaos_monkey.sh "$TEMP_DIR" 2>&1)

if [[ "$OUTPUT" == *"Chaos Monkey Birthday Prank complete"* ]]; then
  echo "✅ Test passed: Prank simulation ran successfully."
else
  echo "❌ Test failed: Unexpected output."
  echo "$OUTPUT"
  exit 1
fi

# Cleanup
rm -rf "$TEMP_DIR"
