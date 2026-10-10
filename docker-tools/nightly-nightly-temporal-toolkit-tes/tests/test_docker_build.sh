#!/bin/bash
set -euo pipefail

IMAGE_NAME="temporal-toolkit-tesseract-test"
DOCKERFILE_PATH="../src/Dockerfile"
ENTRYPOINT_PATH="../src/entrypoint.sh"
BUILD_CONTEXT_PATH="../src"

echo "--- Testing Docker Image Build and Functionality ---"

# Ensure Dockerfile and entrypoint exist
if [ ! -f "$DOCKERFILE_PATH" ]; then
    echo "Error: Dockerfile not found at $DOCKERFILE_PATH"
    exit 1
fi
if [ ! -f "$ENTRYPOINT_PATH" ]; then
    echo "Error: Entrypoint script not found at $ENTRYPOINT_PATH"
    exit 1
fi

# Build the Docker image
echo "Building Docker image: $IMAGE_NAME from $DOCKERFILE_PATH (context: $BUILD_CONTEXT_PATH)"
docker build -t "$IMAGE_NAME" -f "$DOCKERFILE_PATH" "$BUILD_CONTEXT_PATH"
BUILD_STATUS=$?
if [ $BUILD_STATUS -ne 0 ]; then
    echo "Docker build failed!"
    exit $BUILD_STATUS
fi
echo "Docker image built successfully."

# Mock rationale: The tests are designed to be deterministic and offline by building and running a local Docker image.
# They do not rely on external network calls or services beyond the initial Docker image pull (which is cached)
# and local container execution. The verification steps run commands *inside* the locally built container.

# Function to check if a command exists and runs
check_tool() {
    local tool_name=$1
    local version_cmd=$2
    echo "Checking for $tool_name..."
    if docker run --rm "$IMAGE_NAME" bash -c "$version_cmd" > /dev/null 2>&1; then
        echo "  $tool_name found and executable."
    else
        echo "  Error: $tool_name not found or not executable. Command: '$version_cmd'"
        cleanup_and_exit 1
    fi
}

# Cleanup function to ensure image is removed even on failure
cleanup_and_exit() {
    local exit_code=$1
    echo "Cleaning up Docker image: $IMAGE_NAME"
    docker rmi "$IMAGE_NAME" || echo "Warning: Failed to remove Docker image $IMAGE_NAME. You may need to remove it manually."
    exit $exit_code
}

# List of tools and their version commands
check_tool "git" "git --version"
check_tool "curl" "curl --version"
check_tool "wget" "wget --version"
check_tool "jq" "jq --version"
check_tool "yq" "yq --version"
check_tool "vim" "vim --version | head -n 1" # Just check if it runs, output is long
check_tool "tmux" "tmux -V"
check_tool "htop" "htop -v" # Just check if it runs, output is long
check_tool "ping" "ping -c 1 localhost"
check_tool "ansible" "ansible --version"
check_tool "terraform" "terraform --version"
check_tool "kubectl" "kubectl version --client"
check_tool "aws" "aws --version"

echo "All essential tools verified successfully."

# Test entrypoint default command (should drop into bash and execute a command)
echo "Testing entrypoint default command..."
if docker run --rm -i "$IMAGE_NAME" bash -c "echo 'Hello from Tesseract'" | grep -q "Hello from Tesseract"; then
    echo "  Entrypoint default command (bash) works."
else
    echo "  Error: Entrypoint default command failed."
    cleanup_and_exit 1
fi

# Final cleanup
cleanup_and_exit 0

echo "--- All tests passed! ---"
