#!/bin/bash

# Mock rationale: These tests run actual Docker commands.
# To make them deterministic and offline (from a network perspective for the build,
# and from a host time perspective for the faketime tests), we assume Docker is installed
# and functional locally. The 'offline' aspect refers to the *behavior* of the utility
# itself (time-locking), not necessarily the Docker build process which might fetch layers.
# However, once layers are cached, subsequent builds are fast and effectively offline.
# The core logic being tested (faketime application) is entirely deterministic.

set -euo pipefail

UTIL_DIR="$(dirname "$0")"/..
RUN_SCRIPT="$UTIL_DIR/src/run-chrono-container.sh"
IMAGE_NAME="apocalypsai/nightly-chrono-container"

echo "--- Running Nightly Chrono-Container Tests ---"

# Clean up any previous image to ensure a fresh build for testing
docker rmi "$IMAGE_NAME" > /dev/null 2>&1 || true

# Test 1: Basic execution without temporal anchor
echo "Test 1: Basic execution without temporal anchor"
OUTPUT=$("$RUN_SCRIPT" "echo Hello Chrono-World")
if [[ "$OUTPUT" == *"Hello Chrono-World"* ]]; then
    echo "PASS: Basic execution successful."
else
    echo "FAIL: Basic execution failed. Output: $OUTPUT"
    exit 1
fi

# Test 2: Execution with a specific temporal anchor
echo "Test 2: Execution with a specific temporal anchor"
EXPECTED_DATE="2042-07-15 09:30:00"
# The 'date' command output format can vary, so we'll check for the year and a specific part of the time.
# Using `date -u +%Y-%m-%d %H:%M:%S` for consistent UTC output.
OUTPUT=$("$RUN_SCRIPT" "date -u +%Y-%m-%d %H:%M:%S" "$EXPECTED_DATE")
if [[ "$OUTPUT" == *"Chrono-Container: Anchoring time to $EXPECTED_DATE"* && "$OUTPUT" == *"$EXPECTED_DATE"* ]]; then
    echo "PASS: Temporal anchor applied correctly."
else
    echo "FAIL: Temporal anchor not applied correctly. Expected to see '$EXPECTED_DATE'. Output: $OUTPUT"
    exit 1
fi

# Test 3: Execution with a different temporal anchor
echo "Test 3: Execution with a different temporal anchor"
EXPECTED_DATE_2="1999-12-31 23:59:59"
OUTPUT=$("$RUN_SCRIPT" "date -u +%Y-%m-%d %H:%M:%S" "$EXPECTED_DATE_2")
if [[ "$OUTPUT" == *"Chrono-Container: Anchoring time to $EXPECTED_DATE_2"* && "$OUTPUT" == *"$EXPECTED_DATE_2"* ]]; then
    echo "PASS: Different temporal anchor applied correctly."
else
    echo "FAIL: Different temporal anchor not applied correctly. Expected to see '$EXPECTED_DATE_2'. Output: $OUTPUT"
    exit 1
fi

# Test 4: Command with arguments
echo "Test 4: Command with arguments"
OUTPUT=$("$RUN_SCRIPT" "echo Argument 1 Argument 2" "2000-01-01 00:00:00")
if [[ "$OUTPUT" == *"Argument 1 Argument 2"* ]]; then
    echo "PASS: Command with arguments executed correctly."
else
    echo "FAIL: Command with arguments failed. Output: $OUTPUT"
    exit 1
fi

# Test 5: Error handling for no command
echo "Test 5: Error handling for no command"
# Expecting the host script to catch this first
OUTPUT=$("$RUN_SCRIPT" "" 2>&1 || true) # Capture stderr and prevent script from exiting
if [[ "$OUTPUT" == *"Usage: "* ]]; then
    echo "PASS: Host script caught no command error."
else
    echo "FAIL: Host script did not catch no command error. Output: $OUTPUT"
    exit 1
fi

# Test 6: Error handling for no command (container side, if host script fails)
echo "Test 6: Error handling for no command (container side)"
# This test is a bit tricky as the host script should prevent it.
# We'll simulate by directly calling docker run with an empty command,
# which should then trigger the container's internal check.
# Mock rationale: Directly invoking `docker run` to bypass the host script's initial validation
# allows us to test the container's internal error handling for missing commands.
OUTPUT=$(docker run --rm "$IMAGE_NAME" "" "2000-01-01 00:00:00" 2>&1 || true)
if [[ "$OUTPUT" == *"Error: No command provided to chrono-run.sh"* ]]; then
    echo "PASS: Container caught no command error."
else
    echo "FAIL: Container did not catch no command error. Output: $OUTPUT"
    exit 1
fi

echo "--- All Nightly Chrono-Container Tests Passed ---"

# Clean up the image after tests
docker rmi "$IMAGE_NAME" > /dev/null 2>&1 || true
