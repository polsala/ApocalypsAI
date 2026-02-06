#!/bin/bash

set -euo pipefail

IMAGE_NAME="quibble-quencher-test"
QUIBBLE_FILE="example.quib"
EXPECTED_OUTPUT_FILE="expected_output.txt"
ACTUAL_OUTPUT_FILE="actual_output.txt"

# Mock rationale:
# We are testing the Docker image build and execution flow.
# The 'quibble.sh' script itself is a mock interpreter for a fictional language.
# We mock the expected output by defining it in a file and comparing against it.
# Docker commands are real, but their interaction with the fictional language is mocked.

echo "Running tests for Nightly Quibble Quencher..."

# Create a temporary expected output file
cat <<EOF > "$EXPECTED_OUTPUT_FILE"
Hello, ApocalypsAI!
Quibbles quenched!
  Indentation doesn't matter much.
The universe is a quibble.
EOF

# 1. Build the Docker image
echo "Building Docker image '$IMAGE_NAME'..."
docker build -t "$IMAGE_NAME" . > /dev/null
if [ $? -ne 0 ]; then
    echo "Test Failed: Docker image build failed."
    exit 1
fi
echo "Docker image built successfully."

# 2. Run the example QuibbleScript file in the container
echo "Running '$QUIBBLE_FILE' in container..."
# Mount the current directory (which contains src/) into /app/scripts in the container
docker run --rm -v "$(pwd)/src:/app/scripts" "$IMAGE_NAME" /app/scripts/"$QUIBBLE_FILE" > "$ACTUAL_OUTPUT_FILE"
if [ $? -ne 0 ]; then
    echo "Test Failed: Docker container execution failed."
    rm -f "$EXPECTED_OUTPUT_FILE" "$ACTUAL_OUTPUT_FILE"
    exit 1
fi
echo "QuibbleScript executed, output captured."

# 3. Compare actual output with expected output
echo "Comparing actual output with expected output..."
if diff -u "$EXPECTED_OUTPUT_FILE" "$ACTUAL_OUTPUT_FILE"; then
    echo "Test Passed: Output matches expected."
else
    echo "Test Failed: Output mismatch."
    rm -f "$EXPECTED_OUTPUT_FILE" "$ACTUAL_OUTPUT_FILE"
    exit 1
fi

# Clean up
echo "Cleaning up temporary files..."
rm -f "$EXPECTED_OUTPUT_FILE" "$ACTUAL_OUTPUT_FILE"
echo "All tests passed for Nightly Quibble Quencher!"

exit 0
