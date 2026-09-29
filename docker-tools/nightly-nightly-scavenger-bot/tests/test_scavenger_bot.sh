#!/bin/bash

set -euo pipefail

# Mock rationale: The scavenger_bot.py uses random values for resource type and quantity.
# The test verifies the structural output of the script and its Docker execution,
# not the specific random values. Thus, no direct mocking of random is needed;
# we assert on the expected output pattern, which is deterministic.

echo "Running tests for nightly-scavenger-bot..."

# Navigate to the src directory for docker-compose operations
pushd src > /dev/null

# Clean up any previous runs
docker-compose down --rmi all --volumes --remove-orphans > /dev/null 2>&1 || true

# Build the Docker image
echo "Building Docker image..."
if ! docker-compose build > /dev/null; then
    echo "Error: Docker image build failed!"
    popd > /dev/null
    exit 1
fi

# Run the scavenger bot and capture its output
echo "Running scavenger bot and capturing output..."
OUTPUT=$(docker-compose run --rm scavenger 2>&1)
EXIT_CODE=$?

# Check if the command ran successfully
if [ $EXIT_CODE -ne 0 ]; then
    echo "Error: Scavenger bot exited with code $EXIT_CODE."
    echo "Output:"
    echo "$OUTPUT"
    popd > /dev/null
    exit 1
fi

# Assertions for the output
echo "Verifying output..."

# Check for initiation message
if ! echo "$OUTPUT" | grep -q "Initiating scavenging protocol..."; then
    echo "Test Failed: 'Initiating scavenging protocol...' message not found."
    echo "Output:"
    echo "$OUTPUT"
    popd > /dev/null
    exit 1
fi

# Check for found resource message pattern
if ! echo "$OUTPUT" | grep -E -q "Scavenger Bot [0-9]{3} found [0-9]+ units of .+"; then
    echo "Test Failed: 'found X units of Y' message pattern not found."
    echo "Output:"
    echo "$OUTPUT"
    popd > /dev/null
    exit 1
fi

# Check for completion message
if ! echo "$OUTPUT" | grep -q "Scavenging complete. Returning to base."; then
    echo "Test Failed: 'Scavenging complete. Returning to base.' message not found."
    echo "Output:"
    echo "$OUTPUT"
    popd > /dev/null
    exit 1
fi

# Clean up Docker resources
echo "Cleaning up Docker resources..."
docker-compose down --rmi all --volumes --remove-orphans > /dev/null

popd > /dev/null

echo "All tests passed for nightly-scavenger-bot!"
exit 0
