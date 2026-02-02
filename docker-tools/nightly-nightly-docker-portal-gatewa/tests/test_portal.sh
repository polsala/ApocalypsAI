#!/bin/sh

# test_portal.sh - builds and tests the portal-gateway Docker image

set -e

# Mock rationale: assumes docker is installed and functional in the test environment.

# Build the Docker image (quietly)
docker build -t portal-gateway-test . > /dev/null

# Run the container with a custom destination and capture output
OUTPUT=$(docker run --rm -e DESTINATION="Testland" portal-gateway-test)

# Verify that the output contains the custom destination string
echo "$OUTPUT" | grep -q "You have entered: Testland" || {
  echo "Test failed: custom destination not found in output"
  exit 1
}

echo "Test passed"
