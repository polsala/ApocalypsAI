#!/bin/bash
set -e

IMAGE_NAME="nightly-resource-scavenger-bot-test"
CONTAINER_NAME="scavenger-test-run"
RESOURCES_FILE="src/resources.txt"

echo "---\n--- Building Docker image: $IMAGE_NAME ---\n---"
docker build -t $IMAGE_NAME .

echo "---\n--- Running container and capturing output ---\n---"
OUTPUT=$(docker run --name $CONTAINER_NAME --rm $IMAGE_NAME)
EXIT_CODE=$?

echo "---\n--- Verifying output ---\n---"
if [ $EXIT_CODE -ne 0 ]; then
    echo "Test failed: Container exited with non-zero status $EXIT_CODE"
    echo "Output was:\n$OUTPUT"
    exit 1
fi

# Check for the main report header
if ! echo "$OUTPUT" | grep -q "Scavenger Bot reports:"; then
    echo "Test failed: Output does not contain 'Scavenger Bot reports:'"
    echo "Output was:\n$OUTPUT"
    exit 1
fi

# Check if it reported finding 0 items or some items
if echo "$OUTPUT" | grep -q "A thorough search yielded nothing but echoes of the past."; then
    echo "Test passed: Bot reported finding 0 items (valid outcome)."
elif echo "$OUTPUT" | grep -q "Found [0-9]* valuable items!"; then
    echo "Test passed: Bot reported finding some items (valid outcome)."
    # Further check: if items were found, ensure at least one is from our known list
    FOUND_ANY_KNOWN_RESOURCE=false
    while IFS= read -r resource; do
        # Escape special characters in resource name for grep pattern matching
        escaped_resource=$(echo "$resource" | sed 's/[^^$.*+?|(){}\[\]]/\&/g')
        if echo "$OUTPUT" | grep -q -- "- $escaped_resource"; then
            FOUND_ANY_KNOWN_RESOURCE=true
            break
        fi
    done < "$RESOURCES_FILE"

    if [ "$FOUND_ANY_KNOWN_RESOURCE" = false ]; then
        echo "Test failed: Bot reported finding items, but none of them are from the known resources list."
        echo "Output was:\n$OUTPUT"
        exit 1
    fi
else
    echo "Test failed: Output does not indicate 0 items found or some items found."
    echo "Output was:\n$OUTPUT"
    exit 1
fi

echo "---\n--- All tests passed! ---\n---"

# Mock rationale:
# The 'src/resources.txt' file serves as a static, mocked source for the available resources.
# This ensures that the bot always attempts to 'scavenge' from a predefined, testable list.
# The test script then verifies the structural integrity of the bot's output,
# checking for expected phrases and confirming that any reported 'found' items
# originate from this mocked list, making the test deterministic despite the
# random selection logic within the bot. The test covers both scenarios: finding
# no items and finding some items, ensuring the output format is consistent.
