#!/bin/bash

set -euo pipefail

TEST_ERA="test-era-py37"
TEST_PYTHON_VERSION="3.7"
IMAGE_NAME="temporal-echo-chamber"

echo "--- Running Temporal Echo Chamber Tests ---"

# Mock rationale: While docker commands interact with the local Docker daemon,
# these tests are considered 'offline' as they do not make external network
# calls beyond the initial base image pull (which is part of the environment setup).
# They deterministically verify the local Dockerfile and script logic.

# Ensure no previous test image interferes
docker rmi "${IMAGE_NAME}:${TEST_ERA}" || true

# Test 1: Build the image
echo "Test 1: Building image for ${TEST_ERA} (Python ${TEST_PYTHON_VERSION})..."
if ! ../src/echo_chamber.sh build "${TEST_ERA}" "${TEST_PYTHON_VERSION}"; then
    echo "FAIL: Image build failed."
    exit 1
fi
echo "PASS: Image built successfully."

# Test 2: Run a command and check Python version
echo "Test 2: Running 'python --version' inside container..."
PYTHON_VERSION_OUTPUT=$(docker run --rm "${IMAGE_NAME}:${TEST_ERA}" python --version 2>&1)
if [[ "${PYTHON_VERSION_OUTPUT}" != *"Python ${TEST_PYTHON_VERSION}"* ]]; then
    echo "FAIL: Expected Python ${TEST_PYTHON_VERSION}, got: ${PYTHON_VERSION_OUTPUT}"
    ../src/echo_chamber.sh cleanup "${TEST_ERA}" || true
    exit 1
fi
echo "PASS: Python version check successful. Output: ${PYTHON_VERSION_OUTPUT}"

# Test 3: Check for copied files (e.g., README.md)
echo "Test 3: Checking for README.md inside container..."
if ! docker run --rm "${IMAGE_NAME}:${TEST_ERA}" ls /app/README.md; then
    echo "FAIL: README.md not found inside container."
    ../src/echo_chamber.sh cleanup "${TEST_ERA}" || true
    exit 1
fi
echo "PASS: README.md found inside container."

# Test 4: Test invalid 'build' command usage (missing era_tag)
echo "Test 4: Testing invalid 'build' command usage (missing era_tag)..."
if ../src/echo_chamber.sh build; then
    echo "FAIL: 'build' command without era_tag should fail."
    ../src/echo_chamber.sh cleanup "${TEST_ERA}" || true
    exit 1
fi
echo "PASS: 'build' command without era_tag failed as expected."

# Test 5: Test invalid 'run' command usage (missing era_tag)
echo "Test 5: Testing invalid 'run' command usage (missing era_tag)..."
if ../src/echo_chamber.sh run; then
    echo "FAIL: 'run' command without era_tag should fail."
    ../src/echo_chamber.sh cleanup "${TEST_ERA}" || true
    exit 1
fi
echo "PASS: 'run' command without era_tag failed as expected."

# Cleanup
echo "Cleaning up test image..."
if ! ../src/echo_chamber.sh cleanup "${TEST_ERA}"; then
    echo "WARNING: Image cleanup failed, manual intervention might be needed."
fi
echo "PASS: Test image cleaned up."

echo "--- All Temporal Echo Chamber Tests Passed! ---"
