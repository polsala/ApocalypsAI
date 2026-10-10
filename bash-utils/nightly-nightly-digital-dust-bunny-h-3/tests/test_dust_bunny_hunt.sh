#!/bin/bash

# Test suite for Nightly Digital Dust Bunny Hunt

SCRIPT_PATH="./src/dust_bunny_hunt.sh"

# Setup a temporary directory for tests
setup_test_env() {
    TEST_DIR=$(mktemp -d -t dbh-XXXXXX)
    export TEST_DIR # Make it available to mocked commands if needed
    echo "Test environment setup in: $TEST_DIR"
}

# Cleanup temporary directory
cleanup_test_env() {
    if [ -d "$TEST_DIR" ]; then
        rm -rf "$TEST_DIR"
        echo "Test environment cleaned up: $TEST_DIR"
    fi
}

# Mock rm command
# Mock rationale: Prevent actual file deletion during tests and log calls.
mock_rm() {
    echo "MOCK: rm called with arguments: $*" >> "$TEST_DIR/rm_calls.log"
    return 0 # Always succeed in mock
}
export -f mock_rm # Export so subshells can see it

# --- Test Cases ---

# Test 1: No dust bunnies found
test_no_dust_bunnies() {
    local test_name="No dust bunnies found"
    local expected_output_regex="All clear! No digital dust bunnies detected"
    local input_to_script="n" # Doesn't matter, no prompt if no files
    local script_args="$TEST_DIR 7" # Scan for files older than 7 days (irrelevant due to find mock)

    echo "--- Running test: $test_name ---"
    setup_test_env

    # Mock find to return nothing
    # Mock rationale: This simulates a scenario where no old files are found,
    # allowing deterministic testing of the 'no dust bunnies' output path.
    find() {
        echo ""
    }
    export -f find # Export the function so subshells can see it

    # Run the script with mocked commands
    echo "$input_to_script" | "$SCRIPT_PATH" "$script_args" > "$TEST_DIR/output.log" 2>&1

    if grep -qE "$expected_output_regex" "$TEST_DIR/output.log"; then
        echo "PASS: $test_name"
    else
        echo "FAIL: $test_name"
        echo "Expected regex: $expected_output_regex"
        echo "Actual output:"
        cat "$TEST_DIR/output.log"
        exit 1
    fi
    cleanup_test_env
    echo ""
}

# Test 2: Dust bunnies found, user says NO to cleanup
test_dust_bunnies_found_no_cleanup() {
    local test_name="Dust bunnies found, user declines cleanup"
    local expected_output_regex="The dust bunnies remain, for now"
    local input_to_script="n"
    local script_args="$TEST_DIR 7" # Age is irrelevant due to find mock

    echo "--- Running test: $test_name ---"
    setup_test_env

    # Create dummy files (their actual age doesn't matter, only their paths)
    touch "$TEST_DIR/old_file_1.txt"
    touch "$TEST_DIR/old_file_2.log"

    # Mock find to return the dummy files
    # Mock rationale: This ensures specific files are 'found' for testing the
    # interactive cleanup prompt and the 'no cleanup' path.
    find() {
        echo "$TEST_DIR/old_file_1.txt"
        echo "$TEST_DIR/old_file_2.log"
    }
    export -f find

    # Override rm to ensure it's NOT called
    # Mock rationale: Verifies that 'rm' is not invoked when the user declines cleanup.
    rm() {
        echo "MOCK: rm was unexpectedly called!" >> "$TEST_DIR/rm_calls.log"
        return 1 # Indicate failure if rm is called
    }
    export -f rm

    echo "$input_to_script" | "$SCRIPT_PATH" "$script_args" > "$TEST_DIR/output.log" 2>&1

    if grep -qE "$expected_output_regex" "$TEST_DIR/output.log" && ! grep -q "MOCK: rm was unexpectedly called!" "$TEST_DIR/rm_calls.log"; then
        echo "PASS: $test_name"
    else
        echo "FAIL: $test_name"
        echo "Expected regex: $expected_output_regex"
        echo "Actual output:"
        cat "$TEST_DIR/output.log"
        if grep -q "MOCK: rm was unexpectedly called!" "$TEST_DIR/rm_calls.log"; then
            echo "ERROR: rm was called when it shouldn't have been."
        fi
        exit 1
    fi
    cleanup_test_env
    echo ""
}

# Test 3: Dust bunnies found, user says YES to cleanup
test_dust_bunnies_found_and_cleanup() {
    local test_name="Dust bunnies found, user accepts cleanup"
    local expected_output_regex="Digital dust bunnies swept away!"
    local input_to_script="y"
    local script_args="$TEST_DIR 7" # Age is irrelevant due to find mock

    echo "--- Running test: $test_name ---"
    setup_test_env

    # Create dummy files
    touch "$TEST_DIR/old_file_1.txt"
    touch "$TEST_DIR/old_file_2.log"

    # Mock find to return the dummy files
    # Mock rationale: Ensures specific files are 'found' for testing the
    # interactive cleanup prompt and the 'cleanup' path.
    find() {
        echo "$TEST_DIR/old_file_1.txt"
        echo "$TEST_DIR/old_file_2.log"
    }
    export -f find

    # Use the global mock_rm to log calls
    # Mock rationale: Verifies that 'rm' is called with the correct files when the user accepts cleanup.
    rm() { mock_rm "$@"; }
    export -f rm

    echo "$input_to_script" | "$SCRIPT_PATH" "$script_args" > "$TEST_DIR/output.log" 2>&1

    if grep -qE "$expected_output_regex" "$TEST_DIR/output.log" && \
       grep -q "MOCK: rm called with arguments: -f $TEST_DIR/old_file_1.txt" "$TEST_DIR/rm_calls.log" && \
       grep -q "MOCK: rm called with arguments: -f $TEST_DIR/old_file_2.log" "$TEST_DIR/rm_calls.log"; then
        echo "PASS: $test_name"
    else
        echo "FAIL: $test_name"
        echo "Expected regex: $expected_output_regex"
        echo "Actual output:"
        cat "$TEST_DIR/output.log"
        echo "rm calls log:"
        cat "$TEST_DIR/rm_calls.log"
        exit 1
    fi
    cleanup_test_env
    echo ""
}

# Test 4: Dry run option
test_dry_run() {
    local test_name="Dry run option"
    local expected_output_regex="This was a dry run. No dust bunnies were swept away."
    local input_to_script="y" # User input doesn't matter for dry run
    local script_args="$TEST_DIR 7 --dry-run"

    echo "--- Running test: $test_name ---"
    setup_test_env

    # Create dummy files
    touch "$TEST_DIR/old_file_1.txt"
    touch "$TEST_DIR/old_file_2.log"

    # Mock find to return the dummy files
    # Mock rationale: Ensures specific files are 'found' for testing the dry run path.
    find() {
        echo "$TEST_DIR/old_file_1.txt"
        echo "$TEST_DIR/old_file_2.log"
    }
    export -f find

    # Override rm to ensure it's NOT called
    # Mock rationale: Verifies that 'rm' is not invoked during a dry run.
    rm() {
        echo "MOCK: rm was unexpectedly called during dry run!" >> "$TEST_DIR/rm_calls.log"
        return 1 # Indicate failure if rm is called
    }
    export -f rm

    echo "$input_to_script" | "$SCRIPT_PATH" "$script_args" > "$TEST_DIR/output.log" 2>&1

    if grep -qE "$expected_output_regex" "$TEST_DIR/output.log" && ! grep -q "MOCK: rm was unexpectedly called!" "$TEST_DIR/rm_calls.log"; then
        echo "PASS: $test_name"
    else
        echo "FAIL: $test_name"
        echo "Expected regex: $expected_output_regex"
        echo "Actual output:"
        cat "$TEST_DIR/output.log"
        if grep -q "MOCK: rm was unexpectedly called!" "$TEST_DIR/rm_calls.log"; then
            echo "ERROR: rm was called when it shouldn't have been during dry run."
        fi
        exit 1
    fi
    cleanup_test_env
    echo ""
}

# Run all tests
test_no_dust_bunnies
test_dust_bunnies_found_no_cleanup
test_dust_bunnies_found_and_cleanup
test_dry_run

echo "All tests completed."
