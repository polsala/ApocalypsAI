#!/bin/bash
set -euo pipefail

IMAGE_NAME="nightly-chrono-drift-docker-test"
UTIL_DIR="$(dirname "$(dirname "$(readlink -f "$0")")")" # Points to docker-tools/nightly-chrono-drift-docker

echo "--- Building Docker image for testing ---"
docker build -t "$IMAGE_NAME" "$UTIL_DIR"

echo "--- Running tests ---"

# Test 1: Absolute future date
TEST_DATE_ABS="2035-11-22 10:30:00"
echo "Test 1: Absolute future date ($TEST_DATE_ABS)"
OUTPUT=$(docker run --rm "$IMAGE_NAME" "$TEST_DATE_ABS" "date -u")
# Mock rationale: We are asserting against the output of a command run within a controlled Docker environment.
# The 'date -u' command ensures UTC output, making the comparison deterministic.
# The faketime library intercepts system calls, making the time reported by 'date' predictable.
if echo "$OUTPUT" | grep -q "Fri Nov 22 10:30:00 UTC 2035"; then
    echo "Test 1 PASSED"
else
    echo "Test 1 FAILED: Expected 'Fri Nov 22 10:30:00 UTC 2035', got '$OUTPUT'"
    exit 1
fi

# Test 2: Relative future date (+1 year)
echo "Test 2: Relative future date (+1y)"
CURRENT_YEAR=$(date +%Y)
EXPECTED_YEAR=$((CURRENT_YEAR + 1))
OUTPUT=$(docker run --rm "$IMAGE_NAME" "+1y" "date +%Y")
# Mock rationale: Similar to Test 1, the output of 'date +%Y' is predictable when faketime shifts by a known relative amount.
if [ "$OUTPUT" = "$EXPECTED_YEAR" ]; then
    echo "Test 2 PASSED"
else
    echo "Test 2 FAILED: Expected '$EXPECTED_YEAR', got '$OUTPUT'"
    exit 1
fi

# Test 3: Combined absolute base date with relative shift (+1 hour)
TEST_BASE_DATE="2024-01-15 12:00:00"
TEST_SHIFT="+1h"
EXPECTED_SHIFTED_DATE_PATTERN="Mon Jan 15 13:00:00 UTC 2024"

echo "Test 3: Combined absolute base date ($TEST_BASE_DATE) with relative shift ($TEST_SHIFT)"
OUTPUT_SHIFTED=$(docker run --rm "$IMAGE_NAME" "$TEST_BASE_DATE $TEST_SHIFT" "date -u")
# Mock rationale: We are testing faketime's ability to apply a relative shift from a specified base time.
# The output of 'date -u' is deterministic given the faketime input, ensuring the combined shift works as expected.
if echo "$OUTPUT_SHIFTED" | grep -q "$EXPECTED_SHIFTED_DATE_PATTERN"; then
    echo "Test 3 PASSED"
else
    echo "Test 3 FAILED: Expected '$EXPECTED_SHIFTED_DATE_PATTERN', got '$OUTPUT_SHIFTED'"
    exit 1
fi

# Test 4: Command with multiple arguments
echo "Test 4: Command with multiple arguments"
OUTPUT=$(docker run --rm "$IMAGE_NAME" "2020-01-01 00:00:00" "echo Hello World at $(date -u)")
# Mock rationale: This tests that the command string is correctly passed and executed by the entrypoint.
# The 'date -u' inside the echo command will reflect the faketime, confirming the command execution context.
if echo "$OUTPUT" | grep -q "Hello World at Wed Jan  1 00:00:00 UTC 2020"; then
    echo "Test 4 PASSED"
else
    echo "Test 4 FAILED: Expected 'Hello World at Wed Jan  1 00:00:00 UTC 2020', got '$OUTPUT'"
    exit 1
fi

echo "--- All tests passed! ---"

# Clean up the test image
echo "--- Cleaning up test image ---"
docker rmi "$IMAGE_NAME" > /dev/null 2>&1 || true
