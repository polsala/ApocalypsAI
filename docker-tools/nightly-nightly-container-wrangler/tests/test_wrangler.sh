#!/bin/bash

set -euo pipefail

# Test function
run_test() {
    local test_name="$1"
    local scenario="$2"
    local expected_output_regex="$3"
    local unexpected_output_regex="$4"

    echo "--- Running test: $test_name ---"
    
    # Set the scenario for the mock 'docker' executable
    export MOCK_DOCKER_OUTPUT_SCENARIO="$scenario"

    # Prepend the directory containing the mock 'docker' executable to PATH
    # Mock rationale: This ensures that when 'docker' is called by wrangler.sh,
    # our mock script (named 'docker' in the tests/ directory) is executed instead of the actual docker CLI.
    PATH="$(dirname "$0"):$PATH" \
    output=$(bash src/wrangler.sh)
    
    echo "Script output:"
    echo "$output"

    if [[ "$output" =~ $expected_output_regex ]]; then
        echo "PASS: Expected output found."
    else
        echo "FAIL: Expected output NOT found."
        echo "Expected regex: $expected_output_regex"
        return 1
    fi

    if [[ -n "$unexpected_output_regex" && "$output" =~ $unexpected_output_regex ]]; then
        echo "FAIL: Unexpected output found."
        echo "Unexpected regex: $unexpected_output_regex"
        return 1
    else
        echo "PASS: Unexpected output NOT found (or not specified)."
    fi
    echo ""
    return 0
}

# Test cases

# Test 1: No ephemeral containers
run_test "No ephemeral containers" "no_ephemeral" \
    "ApocalypsAI Container Wrangler finished." \
    "Found ephemeral container" || exit 1

# Test 2: Expired ephemeral container
run_test "Expired ephemeral container" "expired_ephemeral" \
    "MOCK: Would stop and remove container expired_id" \
    "MOCK: Would stop and remove container active_id" || exit 1

# Test 3: Ephemeral container with no expiry label
run_test "Ephemeral container with no expiry label" "ephemeral_no_expiry" \
    "Ephemeral container no_expiry_id has no 'apocalypsai.expires_at' label. Leaving it be." \
    "MOCK: Would stop and remove container no_expiry_id" || exit 1

echo "All tests passed!"
