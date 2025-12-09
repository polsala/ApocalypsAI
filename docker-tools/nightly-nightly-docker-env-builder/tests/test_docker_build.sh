#!/bin/bash

set -euo pipefail

# Mock rationale: These tests verify the Docker build process and the presence of tools within the container. They are deterministic and offline as they rely on local Docker image building and execution.

IMAGE_NAME="apoc-dev-env-test"

# Define the tools to test. This should match or be a subset of TOOLS_TO_INSTALL in the Dockerfile.
TOOLS_TO_VERIFY=("git" "node" "python" "docker" "kubectl" "aws")

echo "Building Docker image..."
docker build -t "$IMAGE_NAME" .

echo "Verifying installed tools..."

for tool in "${TOOLS_TO_VERIFY[@]}"; do
    echo "Checking for '$tool'..."
    # Use 'which' to find the executable. For 'docker', 'which docker' is sufficient.
    # For 'aws-cli', 'which aws' is the command.
    if [[ "$tool" == "docker" ]]; then
        command_to_check="docker"
    elif [[ "$tool" == "aws" ]]; then
        command_to_check="aws"
    else
        command_to_check="$tool"
    fi

    if docker run --rm "$IMAGE_NAME" which "$command_to_check" > /dev/null 2>&1;
    then
        echo "  ✅ '$tool' found."
    else
        echo "  ❌ '$tool' NOT found."
        exit 1
    fi
done

echo "All specified tools verified successfully!"

# Clean up the test image
docker rmi "$IMAGE_NAME"

exit 0
