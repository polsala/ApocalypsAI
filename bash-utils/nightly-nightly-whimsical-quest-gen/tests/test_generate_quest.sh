#!/bin/bash

# Test script for generate_quest.sh

# Mock rationale: We need to control the randomness and date output for deterministic tests.
# Mocking 'shuf' and 'date' commands allows us to provide predictable inputs to the script.

# Setup a temporary directory for mocks
TEST_DIR=$(mktemp -d)
export PATH="$TEST_DIR:$PATH" # Prepend test dir to PATH

# Mock shuf
# Mock rationale: 'shuf' is used for random selection. We need to ensure it returns specific values for testing.
# This mock will always return the first line of its input, making selections predictable.
cat << 'EOF' > "$TEST_DIR/shuf"
#!/bin/bash
head -n 1
EOF
chmod +x "$TEST_DIR/shuf"

# Mock date
# Mock rationale: 'date' is used to get the day of the week. We need to fix it for deterministic output.
# This mock will always return "Monday" for the day of the week.
cat << 'EOF' > "$TEST_DIR/date"
#!/bin/bash
if [[ "$1" == "+%A" ]]; then
    echo "Monday"
else
    # Fallback to real date for other formats if needed, though not used by the script
    /bin/date "$@"
fi
EOF
chmod +x "$TEST_DIR/date"

# Define the path to the script under test
SCRIPT_UNDER_TEST="../src/generate_quest.sh"

# --- Test Cases ---

# Test 1: Basic quest generation with mocked shuf and date
test_basic_quest_generation() {
    echo "Running test_basic_quest_generation..."
    # Expected output based on mocked shuf (always picks first element from each array) and date (Monday)
    # QUEST_TEMPLATES[0]: "Retrieve the legendary {object} from the {location} before the {threat} arrives."
    # WHIMSICAL_OBJECTS[0]: "Glimmering Spork of Destiny"
    # WHIMSICAL_LOCATIONS[0]: "Echoing Dustbowl"
    # WHIMSICAL_THREATS[0]: "Grumpy Goblins of Glitch"
    EXPECTED_OUTPUT="Your Whimsical Quest for Monday:\n-------------------------------------\nRetrieve the legendary Glimmering Spork of Destiny from the Echoing Dustbowl before the Grumpy Goblins of Glitch arrives.\n-------------------------------------\nGood luck, wanderer!"

    ACTUAL_OUTPUT=$(bash "$SCRIPT_UNDER_TEST")

    if [[ "$ACTUAL_OUTPUT" == "$EXPECTED_OUTPUT" ]]; then
        echo "PASS: Basic quest generation matched expected output."
    else
        echo "FAIL: Basic quest generation did NOT match expected output."
        echo "--- Expected ---"
        echo -e "$EXPECTED_OUTPUT"
        echo "--- Actual ---"
        echo "$ACTUAL_OUTPUT"
        exit 1
    fi
}

# Test 2: Ensure no unreplaced placeholders remain in the output
test_no_unreplaced_placeholders() {
    echo "Running test_no_unreplaced_placeholders..."
    ACTUAL_OUTPUT=$(bash "$SCRIPT_UNDER_TEST")

    if echo "$ACTUAL_OUTPUT" | grep -qE '\{[a-zA-Z_]+\}'; then
        echo "FAIL: Unreplaced placeholders found in output."
        echo "--- Actual Output ---"
        echo "$ACTUAL_OUTPUT"
        exit 1
    else
        echo "PASS: No unreplaced placeholders found."
    fi
}

# Run all tests
test_basic_quest_generation
test_no_unreplaced_placeholders

# Cleanup
rm -rf "$TEST_DIR"
echo "All tests completed."
