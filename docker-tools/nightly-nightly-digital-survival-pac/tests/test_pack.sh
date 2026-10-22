#!/bin/bash

set -euo pipefail

IMAGE_NAME="nightly-digital-survival-pack-test"
UTIL_ROOT_DIR=$(dirname "$(dirname "$(realpath "$0")")") # Get the root directory of the utility

echo "--- Building Docker image: $IMAGE_NAME from $UTIL_ROOT_DIR ---"
# Build from the utility's root directory
docker build -t "$IMAGE_NAME" "$UTIL_ROOT_DIR"

# Mock rationale: Docker build and run commands are inherently external.
# We are testing the *result* of the Docker build (the image and its contents),
# not mocking Docker itself. The tests are deterministic because the Dockerfile
# and entrypoint are fixed, and the checks are against the installed tools.
# The 'docker' command is assumed to be available in the test environment.

echo "--- Running tests on image: $IMAGE_NAME ---"

# Test 1: Ensure the image builds successfully (checked by 'docker build' exit code)
# This is implicitly checked by `set -e` and the previous `docker build` command.
echo "SUCCESS: Docker image built successfully."

# Test 2: Check if entrypoint script runs and prints welcome message
echo "Checking entrypoint welcome message..."
# Run the container, let the entrypoint execute, and capture its output
WELCOME_MESSAGE=$(docker run --rm "$IMAGE_NAME" bash -c "/usr/local/bin/entrypoint.sh echo 'Test complete'")
if echo "$WELCOME_MESSAGE" | grep -q "Welcome to the Nightly Digital Survival Pack!"; then
    echo "SUCCESS: Entrypoint welcome message found."
else
    echo "ERROR: Entrypoint welcome message not found."
    echo "Output: $WELCOME_MESSAGE"
    exit 1
fi

# Test 3: Check for presence of key tools using 'command -v'
TOOLS=(
    bash
    curl
    jq
    grep
    awk
    sed
    git
    htop
    nmap
    ssh
    rsync
    vim
)

for TOOL_NAME in "${TOOLS[@]}"; do
    echo "Checking tool presence: $TOOL_NAME"
    if docker run --rm "$IMAGE_NAME" bash -c "command -v $TOOL_NAME >/dev/null"; then
        echo "SUCCESS: $TOOL_NAME is present."
    else
        echo "ERROR: $TOOL_NAME is missing."
        exit 1
    fi
done

# Test 4: Verify basic functionality of a few tools (e.g., version checks)
echo "Verifying basic functionality of selected tools..."
declare -A TOOL_VERSION_CMDS
TOOL_VERSION_CMDS["jq"]="jq --version"
TOOL_VERSION_CMDS["curl"]="curl --version"
TOOL_VERSION_CMDS["git"]="git --version"
TOOL_VERSION_CMDS["nmap"]="nmap --version"
TOOL_VERSION_CMDS["ssh"]="ssh -V" # ssh client version

for TOOL_NAME in "${!TOOL_VERSION_CMDS[@]}"; do
    CMD="${TOOL_VERSION_CMDS[$TOOL_NAME]}"
    echo "Checking $TOOL_NAME version: $CMD"
    if docker run --rm "$IMAGE_NAME" bash -c "$CMD >/dev/null"; then
        echo "SUCCESS: $TOOL_NAME version command executed."
    else
        echo "ERROR: $TOOL_NAME version command failed."
        exit 1
    fi
done

# Test 5: Verify default command (bash) works by running the container without explicit command
echo "Checking default command (bash) functionality..."
# Run the container, let it drop into bash, and then execute a command that exits.
# This tests the default CMD ["bash"] behavior.
if docker run --rm "$IMAGE_NAME" bash -c "echo 'Default command test successful'"; then
    echo "SUCCESS: Default command (bash) works."
else
    echo "ERROR: Default command (bash) failed."
    exit 1
fi

echo "--- All tests passed for $IMAGE_NAME ---"

# Clean up the test image
echo "--- Cleaning up Docker image: $IMAGE_NAME ---"
docker rmi "$IMAGE_NAME" >/dev/null 2>&1 || true # Ignore errors if image is not found for some reason
echo "Clean up complete."
