#!/bin/bash

# Test suite for Nightly Cosmic Container Cleaner

# Source the script to be tested
SCRIPT_TO_TEST="../src/cosmic_cleaner.sh"

# --- Mocking Docker commands ---
# Mock rationale: Simulate docker command output without requiring a Docker daemon
# or actually modifying the host's Docker environment. This ensures deterministic
# and offline testing.
MOCKED_DOCKER_OUTPUT=""
MOCKED_DOCKER_EXIT_CODE=0

docker() {
    echo "$MOCKED_DOCKER_OUTPUT"
    return "$MOCKED_DOCKER_EXIT_CODE"
}

# --- Test Helper Functions ---
assert_contains() {
    local expected_substring="$1"
    local actual_output="$2"
    local test_name="$3"
    if echo "$actual_output" | grep -q "$expected_substring"; then
        echo "✅ PASS: $test_name (contains '$expected_substring')"
    else
        echo "❌ FAIL: $test_name (expected to contain '$expected_substring', but got: $actual_output)"
        exit 1
    fi
}

assert_not_contains() {
    local unexpected_substring="$1"
    local actual_output="$2"
    local test_name="$3"
    if echo "$actual_output" | grep -q "$unexpected_substring"; then
        echo "❌ FAIL: $test_name (expected NOT to contain '$unexpected_substring', but got: $actual_output)"
        exit 1
    else
        echo "✅ PASS: $test_name (does not contain '$unexpected_substring')"
    fi
}

# --- Test Cases ---

# Test 1: Successful cleanup
test_successful_cleanup() {
    echo "--- Running Test: Successful Cleanup ---"
    MOCKED_DOCKER_OUTPUT="Total reclaimed space: 100MB"
    MOCKED_DOCKER_EXIT_CODE=0
    OUTPUT=$("$SCRIPT_TO_TEST")
    assert_contains "Success! We've swept away 100MB of cosmic dust." "$OUTPUT" "Successful Cleanup Message"
    assert_contains "Your Docker universe is now sparkling clean" "$OUTPUT" "Successful Cleanup Whimsical Message"
    echo ""
}

# Test 2: No resources to clean
test_no_resources_to_clean() {
    echo "--- Running Test: No Resources to Clean ---"
    MOCKED_DOCKER_OUTPUT="Total reclaimed: 0B"
    MOCKED_DOCKER_EXIT_CODE=0
    OUTPUT=$("$SCRIPT_TO_TEST")
    assert_contains "No cosmic dust found. Your Docker universe was already pristine!" "$OUTPUT" "No Resources Message"
    echo ""
}

# Test 3: Dry run with resources to clean
test_dry_run_with_resources() {
    echo "--- Running Test: Dry Run with Resources ---"
    MOCKED_DOCKER_OUTPUT="Total reclaimed space: 50MB"
    MOCKED_DOCKER_EXIT_CODE=0
    OUTPUT=$("$SCRIPT_TO_TEST" --dry-run)
    assert_contains "Performing a stellar scan (dry run mode)" "$OUTPUT" "Dry Run Indicator"
    assert_contains "The Cosmic Scanner predicts: 50MB of cosmic dust could be cleared." "$OUTPUT" "Dry Run Prediction"
    assert_not_contains "Success! We've swept away" "$OUTPUT" "Dry Run No Actual Cleanup"
    echo ""
}

# Test 4: Dry run with no resources to clean
test_dry_run_no_resources() {
    echo "--- Running Test: Dry Run No Resources ---"
    MOCKED_DOCKER_OUTPUT="Total reclaimed: 0B"
    MOCKED_DOCKER_EXIT_CODE=0
    OUTPUT=$("$SCRIPT_TO_TEST" --dry-run)
    assert_contains "Performing a stellar scan (dry run mode)" "$OUTPUT" "Dry Run Indicator"
    assert_contains "The Cosmic Scanner found no cosmic dust to clear. Your Docker universe is pristine!" "$OUTPUT" "Dry Run No Resources Message"
    assert_not_contains "Success! We've swept away" "$OUTPUT" "Dry Run No Actual Cleanup"
    echo ""
}

# Test 5: Docker command failure
test_docker_command_failure() {
    echo "--- Running Test: Docker Command Failure ---"
    MOCKED_DOCKER_OUTPUT="Error response from daemon: Docker daemon not running."
    MOCKED_DOCKER_EXIT_CODE=1
    OUTPUT=$("$SCRIPT_TO_TEST" 2>&1) # Capture stderr as well
    assert_contains "Cosmic Cleanup encountered an anomaly: Error response from daemon: Docker daemon not running." "$OUTPUT" "Docker Failure Message"
    assert_contains "Please ensure Docker is running and accessible." "$OUTPUT" "Docker Failure Hint"
    echo ""
}

# Test 6: Unknown option
test_unknown_option() {
    echo "--- Running Test: Unknown Option ---"
    OUTPUT=$("$SCRIPT_TO_TEST" --unknown-flag 2>&1)
    assert_contains "Unknown option: --unknown-flag" "$OUTPUT" "Unknown Option Error"
    assert_contains "Usage: $0 [--dry-run]" "$OUTPUT" "Unknown Option Help"
    echo ""
}

# Test 7: Help message
test_help_message() {
    echo "--- Running Test: Help Message ---"
    OUTPUT=$("$SCRIPT_TO_TEST" --help)
    assert_contains "Usage: $0 [--dry-run]" "$OUTPUT" "Help Message Usage"
    assert_contains "A whimsical Docker cleanup utility" "$OUTPUT" "Help Message Description"
    echo ""
}


# --- Run all tests ---
test_successful_cleanup
test_no_resources_to_clean
test_dry_run_with_resources
test_dry_run_no_resources
test_docker_command_failure
test_unknown_option
test_help_message

echo "All tests completed."
