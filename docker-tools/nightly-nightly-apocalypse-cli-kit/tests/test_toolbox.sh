#!/bin/bash

set -euo pipefail

IMAGE_NAME="apocalypse-cli-kit-test"
CONTAINER_NAME="apocalypse-cli-kit-container-test"

echo "--- Building Docker image ---"
docker build -t "$IMAGE_NAME" . > /dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Docker image build failed."
    exit 1
fi
echo "Build successful."

echo "--- Testing container run and basic tools ---"

# Test 1: Container runs and bash is the default command
echo "Test 1: Container runs and bash is the default command..."
OUTPUT=$(docker run --rm "$IMAGE_NAME" bash -c "echo \$0")
if [[ "$OUTPUT" != "bash" ]]; then
    echo "ERROR: Test 1 failed. Expected 'bash', got '$OUTPUT'."
    exit 1
fi
echo "Test 1 passed."

# Test 2: Check for a specific tool (curl)
echo "Test 2: Check for 'curl' tool..."
OUTPUT=$(docker run --rm "$IMAGE_NAME" curl --version 2>&1 | head -n 1)
if [[ "$OUTPUT" != *"curl"* ]]; then
    echo "ERROR: Test 2 failed. 'curl' not found or version output unexpected."
    echo "Output: $OUTPUT"
    exit 1
fi
echo "Test 2 passed."

# Test 3: Check for another specific tool (jq)
echo "Test 3: Check for 'jq' tool..."
OUTPUT=$(docker run --rm "$IMAGE_NAME" jq --version 2>&1 | head -n 1)
if [[ "$OUTPUT" != *"jq"* ]]; then
    echo "ERROR: Test 3 failed. 'jq' not found or version output unexpected."
    echo "Output: $OUTPUT"
    exit 1
fi
echo "Test 3 passed."

# Test 4: Check for custom prompt in interactive mode (requires a trick)
# Mock rationale: We can't truly test an interactive prompt directly in a non-interactive script.
# Instead, we'll run a command that prints the PS1 variable, which is set by our entrypoint.
echo "Test 4: Check for custom prompt (PS1 variable)..."
OUTPUT=$(docker run --rm "$IMAGE_NAME" bash -c 'echo "\$PS1"' | tr -d '\n') # Remove newline for exact comparison
EXPECTED_PS1="\[\033[01;31m\](ApocalypseKit)\[\033[00m\]:\w\$ "
if [[ "$OUTPUT" != "$EXPECTED_PS1" ]]; then
    echo "ERROR: Test 4 failed. Custom PS1 not set correctly."
    echo "Expected: '$EXPECTED_PS1'"
    echo "Got: '$OUTPUT'"
    exit 1
fi
echo "Test 4 passed."

# Test 5: Check welcome message (requires capturing stderr/stdout from entrypoint)
# Mock rationale: The entrypoint prints to stdout/stderr before exec. We can capture this.
echo "Test 5: Check welcome message..."
# Run a command that exits immediately, capturing all output.
# The entrypoint script prints the welcome message before `exec "\$@"`.
# We expect the welcome message to be present in the output.
WELCOME_MESSAGE_PART="Welcome to the ApocalypsAI CLI Survival Toolbox!"
FULL_OUTPUT=$(docker run --rm "$IMAGE_NAME" bash -c "exit 0" 2>&1)
if ! echo "$FULL_OUTPUT" | grep -q "$WELCOME_MESSAGE_PART"; then
    echo "ERROR: Test 5 failed. Welcome message not found."
    echo "Full output: $FULL_OUTPUT"
    exit 1
fi
echo "Test 5 passed."

echo "All tests passed successfully!"

# Clean up image
echo "--- Cleaning up Docker image ---"
docker rmi "$IMAGE_NAME" > /dev/null
echo "Cleanup complete."
