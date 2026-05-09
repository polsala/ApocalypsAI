#!/bin/bash

# Mock rationale:
# We need to test the script's logic for identifying files based on age.
# This requires creating temporary files with specific modification times.
# We mock the 'date' command to ensure deterministic age calculation for files
# created with 'touch -t', as 'stat -c %Y' will return the actual timestamp.
# By fixing the 'current time' for calculation, we can predict the 'age' output.
# We also mock 'du' to provide consistent file sizes for testing output formatting.

set -euo pipefail

SCRIPT_PATH="./src/dust_bunny_sweeper.sh"
TEST_DIR="test_temp_bunker"

# --- Mocks ---
# Mock 'date' to return a fixed timestamp for deterministic age calculation
MOCKED_DATE_EPOCH="1672531200" # Jan 1, 2023 00:00:00 UTC
MOCKED_DATE_CMD() {
    if [[ "$1" == "+%s" ]]; then
        echo "$MOCKED_DATE_EPOCH"
    else
        # Fallback for other date commands if needed, though not expected by script
        /bin/date "$@"
    fi
}
export -f MOCKED_DATE_CMD
alias date='MOCKED_DATE_CMD'

# Mock 'du' to return a consistent size for testing output formatting
MOCKED_DU_CMD() {
    echo "4.0K\t$1" # Always report 4.0K for any file
}
export -f MOCKED_DU_CMD
alias du='MOCKED_DU_CMD'
# --- End Mocks ---

setup() {
    mkdir -p "$TEST_DIR/sub_bunker"
    # Create files with specific modification times
    # Current time for mock: Jan 1, 2023 00:00:00 UTC (epoch 1672531200)

    # File 1: 100 days old (older than default 90)
    # Mod time: 1672531200 - (100 * 86400) = 1663852800 (Sep 22, 2022)
    touch -t 202209220000 "$TEST_DIR/old_file_1.txt"

    # File 2: 50 days old (younger than default 90)
    # Mod time: 1672531200 - (50 * 86400) = 1668105600 (Nov 10, 2022)
    touch -t 202211100000 "$TEST_DIR/recent_file_2.log"

    # File 3: 120 days old in sub_bunker (older than default 90)
    # Mod time: 1672531200 - (120 * 86400) = 1662124800 (Sep 02, 2022)
    touch -t 202209020000 "$TEST_DIR/sub_bunker/old_file_3.conf"

    # File 4: 10 days old in sub_bunker (younger than default 90)
    # Mod time: 1672531200 - (10 * 86400) = 1671667200 (Dec 22, 2022)
    touch -t 202212220000 "$TEST_DIR/sub_bunker/recent_file_4.data"

    # File 5: 200 days old (for custom -d test)
    # Mod time: 1672531200 - (200 * 86400) = 1655769600 (Jun 20, 2022)
    touch -t 202206200000 "$TEST_DIR/very_old_file_5.tmp"
}

teardown() {
    rm -rf "$TEST_DIR"
    # Unset aliases and functions to clean up environment
    unset -f MOCKED_DATE_CMD
    unset -f MOCKED_DU_CMD
    unalias date || true
    unalias du || true
}

# Test 1: Default scan (non-recursive, 90 days)
test_default_scan() {
    echo "Running Test 1: Default scan (non-recursive, 90 days)"
    local output
    output=$("$SCRIPT_PATH" "$TEST_DIR")

    # Expect old_file_1.txt (100 days) but not recent_file_2.log (50 days)
    # And not files in sub_bunker because it's non-recursive
    if ! echo "$output" | grep -q "old_file_1.txt"; then
        echo "FAIL: Test 1 - old_file_1.txt not found in default scan output."
        echo "Output: $output"
        return 1
    fi
    if echo "$output" | grep -q "recent_file_2.log"; then
        echo "FAIL: Test 1 - recent_file_2.log found in default scan output (should be too young)."
        echo "Output: $output"
        return 1
    fi
    if echo "$output" | grep -q "old_file_3.conf"; then
        echo "FAIL: Test 1 - old_file_3.conf found in default scan output (should be non-recursive)."
        echo "Output: $output"
        return 1
    fi
    if ! echo "$output" | grep -q "Age: 100 days, Size: 4.0K"; then
        echo "FAIL: Test 1 - Expected age/size details for old_file_1.txt not found."
        echo "Output: $output"
        return 1
    fi
    echo "PASS: Test 1"
    return 0
}

# Test 2: Recursive scan (-r)
test_recursive_scan() {
    echo "Running Test 2: Recursive scan (-r)"
    local output
    output=$("$SCRIPT_PATH" -r "$TEST_DIR")

    # Expect old_file_1.txt (100 days) and old_file_3.conf (120 days)
    if ! echo "$output" | grep -q "old_file_1.txt"; then
        echo "FAIL: Test 2 - old_file_1.txt not found in recursive scan output."
        echo "Output: $output"
        return 1
    fi
    if ! echo "$output" | grep -q "old_file_3.conf"; then
        echo "FAIL: Test 2 - old_file_3.conf not found in recursive scan output."
        echo "Output: $output"
        return 1
    fi
    if echo "$output" | grep -q "recent_file_2.log"; then
        echo "FAIL: Test 2 - recent_file_2.log found in recursive scan output (should be too young)."
        echo "Output: $output"
        return 1
    fi
    if echo "$output" | grep -q "recent_file_4.data"; then
        echo "FAIL: Test 2 - recent_file_4.data found in recursive scan output (should be too young)."
        echo "Output: $output"
        return 1
    fi
    echo "PASS: Test 2"
    return 0
}

# Test 3: Custom days threshold (-d)
test_custom_days_threshold() {
    echo "Running Test 3: Custom days threshold (-d 150)"
    local output
    output=$("$SCRIPT_PATH" -d 150 -r "$TEST_DIR")

    # Expect very_old_file_5.tmp (200 days)
    # old_file_1.txt (100 days) and old_file_3.conf (120 days) should NOT be found
    if ! echo "$output" | grep -q "very_old_file_5.tmp"; then
        echo "FAIL: Test 3 - very_old_file_5.tmp not found with -d 150."
        echo "Output: $output"
        return 1
    fi
    if echo "$output" | grep -q "old_file_1.txt"; then
        echo "FAIL: Test 3 - old_file_1.txt found with -d 150 (should be too young)."
        echo "Output: $output"
        return 1
    fi
    if echo "$output" | grep -q "old_file_3.conf"; then
        echo "FAIL: Test 3 - old_file_3.conf found with -d 150 (should be too young)."
        echo "Output: $output"
        return 1
    fi
    if ! echo "$output" | grep -q "Age: 200 days, Size: 4.0K"; then
        echo "FAIL: Test 3 - Expected age/size details for very_old_file_5.tmp not found."
        echo "Output: $output"
        return 1
    fi
    echo "PASS: Test 3"
    return 0
}

# Test 4: List only (-l)
test_list_only() {
    echo "Running Test 4: List only (-l)"
    local output
    output=$("$SCRIPT_PATH" -l "$TEST_DIR")

    # Expect old_file_1.txt, but only the path, no age/size details
    if ! echo "$output" | grep -q "$TEST_DIR/old_file_1.txt"; then
        echo "FAIL: Test 4 - old_file_1.txt path not found in list-only output."
        echo "Output: $output"
        return 1
    fi
    if echo "$output" | grep -q "Age:"; then
        echo "FAIL: Test 4 - Age details found in list-only output."
        echo "Output: $output"
        return 1
    fi
    if echo "$output" | grep -q "Size:"; then
        echo "FAIL: Test 4 - Size details found in list-only output."
        echo "Output: $output"
        return 1
    fi
    echo "PASS: Test 4"
    return 0
}

# Test 5: Invalid directory
test_invalid_directory() {
    echo "Running Test 5: Invalid directory"
    local output
    output=$("$SCRIPT_PATH" "non_existent_dir" 2>&1 || true) # Capture stderr and allow failure

    if ! echo "$output" | grep -q "Error: Directory 'non_existent_dir' does not exist or is not a directory."; then
        echo "FAIL: Test 5 - Expected error message for invalid directory not found."
        echo "Output: $output"
        return 1
    fi
    echo "PASS: Test 5"
    return 0
}

# Test 6: No directory specified
test_no_directory() {
    echo "Running Test 6: No directory specified"
    local output
    output=$("$SCRIPT_PATH" 2>&1 || true) # Capture stderr and allow failure

    if ! echo "$output" | grep -q "Error: No directory specified."; then
        echo "FAIL: Test 6 - Expected error message for no directory not found."
        echo "Output: $output"
        return 1
    fi
    echo "PASS: Test 6"
    return 0
}

# Test 7: Invalid -d argument
test_invalid_d_arg() {
    echo "Running Test 7: Invalid -d argument"
    local output
    output=$("$SCRIPT_PATH" -d abc "$TEST_DIR" 2>&1 || true) # Capture stderr and allow failure

    if ! echo "$output" | grep -q "Error: -d requires a positive integer for days."; then
        echo "FAIL: Test 7 - Expected error message for invalid -d argument not found."
        echo "Output: $output"
        return 1
    fi
    echo "PASS: Test 7"
    return 0
}


# Main test execution
run_tests() {
    local failed_tests=0
    setup

    test_default_scan || failed_tests=$((failed_tests + 1))
    test_recursive_scan || failed_tests=$((failed_tests + 1))
    test_custom_days_threshold || failed_tests=$((failed_tests + 1))
    test_list_only || failed_tests=$((failed_tests + 1))
    test_invalid_directory || failed_tests=$((failed_tests + 1))
    test_no_directory || failed_tests=$((failed_tests + 1))
    test_invalid_d_arg || failed_tests=$((failed_tests + 1))

    teardown

    if [ "$failed_tests" -eq 0 ]; then
        echo "All tests passed!"
        return 0
    else
        echo "Some tests failed: $failed_tests failures."
        return 1
    fi
}

run_tests
