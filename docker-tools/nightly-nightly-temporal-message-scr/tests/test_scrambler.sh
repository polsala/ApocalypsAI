#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

IMAGE_NAME="temporal-scrambler-test"
TEST_MESSAGE="The quick brown fox jumps over the lazy dog."
TEST_MESSAGE_SHORT="Hello World"

echo "--- Building Docker image: $IMAGE_NAME ---"
docker build -t "$IMAGE_NAME" . > /dev/null
echo "Docker image built successfully."

# --- Test Case 1: Default behavior (delay 0.5s, char scramble 1, word reorder 0) ---
echo "--- Test Case 1: Default scrambling ---"
START_TIME=$(date +%s.%N)
OUTPUT=$(docker run "$IMAGE_NAME" "$TEST_MESSAGE" --seed 1) # Use a seed for determinism
END_TIME=$(date +%s.%N)
DURATION=$(echo "$END_TIME - $START_TIME" | bc)

if (( $(echo "$DURATION >= 0.5" | bc -l) )); then
    echo "PASS: Default delay respected (duration: ${DURATION}s)."
else
    echo "FAIL: Default delay not respected (duration: ${DURATION}s)."
    exit 1
fi

if [[ "$OUTPUT" == *"$TEST_MESSAGE"* ]]; then
    echo "FAIL: Default scrambling did not alter the message."
    echo "Output: $OUTPUT"
    exit 1
else
    echo "PASS: Default scrambling altered the message."
fi
# Mock rationale: The delay is tested by measuring execution time. The scrambling is tested by asserting the output is different from the input, and by using a fixed seed to ensure consistent (though not identical to input) output.

# --- Test Case 2: No scrambling (delay 0, char 0, word 0) ---
echo "--- Test Case 2: No scrambling ---"
OUTPUT=$(docker run "$IMAGE_NAME" "$TEST_MESSAGE" --delay 0 --char-scramble-level 0 --word-reorder-level 0)

if [[ "$OUTPUT" == "$TEST_MESSAGE" ]]; then
    echo "PASS: No scrambling produced original message."
else
    echo "FAIL: No scrambling altered the message."
    echo "Expected: '$TEST_MESSAGE'"
    echo "Got:      '$OUTPUT'"
    exit 1
fi
# Mock rationale: Verifies that with all scrambling levels set to 0, the output is identical to input.

# --- Test Case 3: Specific delay (2 seconds) ---
echo "--- Test Case 3: Specific delay (2 seconds) ---"
START_TIME=$(date +%s.%N)
OUTPUT=$(docker run "$IMAGE_NAME" "$TEST_MESSAGE_SHORT" --delay 2 --char-scramble-level 0 --word-reorder-level 0)
END_TIME=$(date +%s.%N)
DURATION=$(echo "$END_TIME - $START_TIME" | bc)

if (( $(echo "$DURATION >= 2.0" | bc -l) )); then
    echo "PASS: 2-second delay respected (duration: ${DURATION}s)."
else
    echo "FAIL: 2-second delay not respected (duration: ${DURATION}s)."
    exit 1
fi
if [[ "$OUTPUT" == "$TEST_MESSAGE_SHORT" ]]; then
    echo "PASS: Message unaltered during delay-only test."
else
    echo "FAIL: Message altered during delay-only test."
    echo "Expected: '$TEST_MESSAGE_SHORT'"
    echo "Got:      '$OUTPUT'"
    exit 1
fi
# Mock rationale: Measures execution time to confirm the specified delay is applied.

# --- Test Case 4: Aggressive character scrambling (level 2) ---
echo "--- Test Case 4: Aggressive character scrambling (level 2) ---"
OUTPUT_LEVEL2=$(docker run "$IMAGE_NAME" "$TEST_MESSAGE_SHORT" --delay 0 --char-scramble-level 2 --word-reorder-level 0 --seed 2)

if [[ "$OUTPUT_LEVEL2" != "$TEST_MESSAGE_SHORT" ]]; then
    echo "PASS: Aggressive character scrambling altered the message."
else
    echo "FAIL: Aggressive character scrambling did not alter the message."
    echo "Output: $OUTPUT_LEVEL2"
    exit 1
fi
# Check for expected aggressive changes (e.g., symbols, case changes)
if [[ "$OUTPUT_LEVEL2" =~ [^a-zA-Z0-9\ ] ]]; then # Check for non-alphanumeric/space characters
    echo "PASS: Aggressive scrambling introduced symbols/non-standard chars."
else
    echo "FAIL: Aggressive scrambling did not introduce expected symbols/non-standard chars."
    echo "Output: $OUTPUT_LEVEL2"
    exit 1
fi
# Mock rationale: Uses a fixed seed to ensure deterministic output for comparison. Asserts that the output is different and contains expected types of aggressive changes (symbols).

# --- Test Case 5: Word reordering (level 1) ---
echo "--- Test Case 5: Word reordering (level 1) ---"
OUTPUT_REORDER=$(docker run "$IMAGE_NAME" "One Two Three Four" --delay 0 --char-scramble-level 0 --word-reorder-level 1 --seed 3)

if [[ "$OUTPUT_REORDER" != "One Two Three Four" ]]; then
    echo "PASS: Word reordering altered the message."
else
    echo "FAIL: Word reordering did not alter the message."
    echo "Output: $OUTPUT_REORDER"
    exit 1
fi
# For deterministic reordering with seed 3, "One Two Three Four" might become "Two One Four Three" or similar.
# We can't assert exact output without knowing the RNG, but we can check if words are indeed reordered.
# A simple check is that the output is not the original, and it contains the same words.
EXPECTED_WORDS="One Two Three Four"
OUTPUT_WORDS=$(echo "$OUTPUT_REORDER" | tr ' ' '\n' | sort | tr '\n' ' ')
EXPECTED_SORTED_WORDS=$(echo "$EXPECTED_WORDS" | tr ' ' '\n' | sort | tr '\n' ' ')

if [[ "$OUTPUT_WORDS" == "$EXPECTED_SORTED_WORDS" ]]; then
    echo "PASS: Reordered message contains the original words."
else
    echo "FAIL: Reordered message does not contain the original words."
    echo "Expected sorted: '$EXPECTED_SORTED_WORDS'"
    echo "Got sorted:      '$OUTPUT_WORDS'"
    exit 1
fi
# Mock rationale: Uses a fixed seed. Asserts that the output is different from the input but contains the same set of words, indicating reordering rather than deletion/addition.

echo "--- All tests passed! ---"

# Clean up the test image
docker rmi "$IMAGE_NAME" > /dev/null
