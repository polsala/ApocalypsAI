#!/bin/bash

set -euo pipefail

IMAGE_NAME="apocalypsai/survival-kit-dockerizer:test"
KIT_DIR="$(dirname "$0")"

echo "--- Building Docker image ---"
docker build -t "$IMAGE_NAME" "$KIT_DIR/.."

# Mock rationale: The tests use pre-defined mock input files (mock_kit_simple.txt, mock_kit_complex.txt) 
# and a hardcoded Python script logic. This ensures deterministic, offline testing 
# without external dependencies or network calls.

# Test Case 1: Simple kit list
echo "\n--- Running with simple kit list (mock_kit_simple.txt) ---"
OUTPUT_SIMPLE=$(docker run --rm -v "$KIT_DIR/mock_kit_simple.txt:/app/kit.txt" "$IMAGE_NAME" /app/kit.txt)

if echo "$OUTPUT_SIMPLE" | grep -q "Item: water filter" && \
   echo "$OUTPUT_SIMPLE" | grep -q "Survival Function: Hydration Management" && \
   echo "$OUTPUT_SIMPLE" | grep -q "Suggested Docker Tool: apocalypsai/aqua-purifier-bot:latest" && \
   echo "$OUTPUT_SIMPLE" | grep -q "Item: radio" && \
   echo "$OUTPUT_SIMPLE" | grep -q "Survival Function: Long-Range Comms" && \
   echo "$OUTPUT_SIMPLE" | grep -q "Suggested Docker Tool: apocalypsai/signal-scout-cli:latest"; then
    echo "Test Case 1 PASSED: Simple kit list processed correctly."
else
    echo "Test Case 1 FAILED: Simple kit list output mismatch."
    echo "Output:\n$OUTPUT_SIMPLE"
    exit 1
fi

# Test Case 2: Complex kit list with unknown items and empty lines
echo "\n--- Running with complex kit list (mock_kit_complex.txt) ---"
OUTPUT_COMPLEX=$(docker run --rm -v "$KIT_DIR/mock_kit_complex.txt:/app/kit.txt" "$IMAGE_NAME" /app/kit.txt)

if echo "$OUTPUT_COMPLEX" | grep -q "Item: first aid kit" && \
   echo "$OUTPUT_COMPLEX" | grep -q "Survival Function: Emergency Medicine" && \
   echo "$OUTPUT_COMPLEX" | grep -q "Item: seeds" && \
   echo "$OUTPUT_COMPLEX" | grep -q "Survival Function: Sustainable Agriculture" && \
   echo "$OUTPUT_COMPLEX" | grep -q "Item: unknown item 123" && \
   echo "$OUTPUT_COMPLEX" | grep -q "Survival Function: General Survival" && \
   echo "$OUTPUT_COMPLEX" | grep -q "Suggested Docker Tool: apocalypsai/generic-survival-aid:latest" && \
   echo "$OUTPUT_COMPLEX" | grep -q "Item: books" && \
   echo "$OUTPUT_COMPLEX" | grep -q "Survival Function: Knowledge Preservation"; then
    echo "Test Case 2 PASSED: Complex kit list processed correctly."
else
    echo "Test Case 2 FAILED: Complex kit list output mismatch."
    echo "Output:\n$OUTPUT_COMPLEX"
    exit 1
fi

# Test Case 3: Empty kit file
echo "\n--- Running with empty kit file ---"
EMPTY_KIT_FILE="$KIT_DIR/mock_kit_empty.txt"
touch "$EMPTY_KIT_FILE"
OUTPUT_EMPTY=$(docker run --rm -v "$EMPTY_KIT_FILE:/app/kit.txt" "$IMAGE_NAME" /app/kit.txt)
rm "$EMPTY_KIT_FILE"

if echo "$OUTPUT_EMPTY" | grep -q "Processing survival kit..." && ! echo "$OUTPUT_EMPTY" | grep -q "Item:"; then
    echo "Test Case 3 PASSED: Empty kit file handled correctly."
else
    echo "Test Case 3 FAILED: Empty kit file output mismatch."
    echo "Output:\n$OUTPUT_EMPTY"
    exit 1
fi

# Test Case 4: Non-existent kit file
echo "\n--- Running with non-existent kit file ---"
# The script exits with code 1 and prints to stderr, so we capture stderr and allow failure
OUTPUT_NONEXISTENT=$(docker run --rm "$IMAGE_NAME" /app/non_existent_kit.txt 2>&1 || true)

if echo "$OUTPUT_NONEXISTENT" | grep -q "Error: Kit file not found at '/app/non_existent_kit.txt'"; then
    echo "Test Case 4 PASSED: Non-existent kit file handled correctly."
else
    echo "Test Case 4 FAILED: Non-existent kit file output mismatch."
    echo "Output:\n$OUTPUT_NONEXISTENT"
    exit 1
fi

# Clean up image
docker rmi "$IMAGE_NAME" > /dev/null 2>&1 || true

echo "\nAll tests passed!"
