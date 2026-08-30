#!/bin/bash

# --- Test Setup ---
# Mock rationale: We need to test the script's logic and output without
# actually interacting with a live Docker daemon or deleting real resources.
# This mock replaces the 'docker' command with a controlled function that
# outputs predefined strings, allowing deterministic testing.

MOCKED_DOCKER_OUTPUT_SUCCESS="Total reclaimed space: 1.23GB\nDeleted images: image1, image2\nDeleted containers: container1"
MOCKED_DOCKER_OUTPUT_FAILURE="Error response from daemon: Something went wrong"

# Function to mock the 'docker' command for success scenario
mock_docker_success() {
    echo -e "$MOCKED_DOCKER_OUTPUT_SUCCESS"
    return 0
}

# Function to mock the 'docker' command for failure scenario
mock_docker_failure() {
    echo -e "$MOCKED_DOCKER_OUTPUT_FAILURE" >&2 # Send error to stderr like real docker
    return 1
}

# --- Test Cases ---

echo "Running tests for nightly-temporal-docker-janitor..."

# Test Case 1: Successful Pruning
echo "--- Test Case 1: Successful Pruning ---"
# Temporarily override the 'docker' command for this test
export -f docker=mock_docker_success
OUTPUT=$(bash src/janitor.sh)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ] && \
   echo "$OUTPUT" | grep -q "Temporal void swept clean!" && \
   echo "$OUTPUT" | grep -q "Total reclaimed space: 1.23GB" && \
   echo "$OUTPUT" | grep -q "Your Docker environment is now pristine"; then
    echo "✅ Test Case 1 Passed: Successful pruning output detected."
else
    echo "❌ Test Case 1 Failed: Expected success output not found or exit code was $EXIT_CODE."
    echo "Output:"
    echo "$OUTPUT"
    exit 1
fi
unset -f docker # Unset the mock for cleanliness

# Test Case 2: Pruning Failure
echo "--- Test Case 2: Pruning Failure ---"
# Temporarily override the 'docker' command for this test
export -f docker=mock_docker_failure
OUTPUT=$(bash src/janitor.sh 2>&1) # Capture stderr as well
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ] && \
   echo "$OUTPUT" | grep -q "Temporal distortion detected during void-sweeping!" && \
   echo "$OUTPUT" | grep -q "Error response from daemon: Something went wrong"; then
    echo "✅ Test Case 2 Passed: Failure output and non-zero exit code detected."
else
    echo "❌ Test Case 2 Failed: Expected failure output not found or exit code was $EXIT_CODE."
    echo "Output:"
    echo "$OUTPUT"
    exit 1
fi
unset -f docker # Unset the mock

echo "All tests completed."
