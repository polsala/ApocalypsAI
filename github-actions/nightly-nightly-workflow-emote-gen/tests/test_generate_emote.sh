#!/bin/bash

# Mock rationale: We are mocking the GitHub Actions environment variables
# (INPUT_STATUS) and the GITHUB_OUTPUT file mechanism to test the script offline
# without needing a full GitHub Actions runner environment.

set -euo pipefail

SCRIPT_PATH="$(dirname "$0")"/../src/generate_emote.sh

# Function to run the script with a given status and capture output
run_test() {
    local test_status="$1"
    local expected_emote="$2"

    # Create a temporary file for GITHUB_OUTPUT
    export GITHUB_OUTPUT=$(mktemp)
    # Mock the input environment variable
    export INPUT_STATUS="$test_status"

    # Run the script
    bash "$SCRIPT_PATH"

    # Read the output from the temporary file
    local actual_output=$(cat "$GITHUB_OUTPUT")

    # Clean up mock environment
    rm "$GITHUB_OUTPUT"
    unset INPUT_STATUS
    unset GITHUB_OUTPUT

    # Assert the output
    if [[ "$actual_output" == "emote=$expected_emote" ]]; then
        echo "✅ Test passed for status '$test_status'"
    else
        echo "❌ Test failed for status '$test_status'"
        echo "   Expected: emote=$expected_emote"
        echo "   Actual:   $actual_output"
        exit 1
    fi
}

echo "Running tests for Nightly Workflow Emote Generator..."

run_test "success" "✨ Galactic Triumph! ✨"
run_test "failure" "💥 Cosmic Catastrophe! 💥"
run_test "cancelled" "💨 Vanished into the Aether 💨"
run_test "skipped" "😴 Hibernating in Hyperspace 😴"
run_test "unknown" "❓ Unknown Cosmic Event ❓"

echo "All tests completed successfully."
