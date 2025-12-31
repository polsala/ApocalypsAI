#!/bin/bash

# Test script for Nightly Digital Dust Bunny Sweeper

# Set -e to exit immediately if a command exits with a non-zero status.
set -e

# --- Mocking `find` and `rm` ---

# Mock rationale: `find` operates on the filesystem and its output depends on actual file timestamps,
# which are non-deterministic and make tests slow. Mocking allows us to control the exact "found"
# items and their properties, ensuring deterministic test results.
mock_find() {
    local path="$1"
    local type_flag=""
    local mtime_flag=""

    # Parse arguments to simulate find's behavior
    shift # remove path
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
            -type)
                type_flag="$2"
                shift
                ;;
            -mtime)
                mtime_flag="$2"
                shift
                ;;
        esac
        shift
    done

    # Simulate finding files/dirs based on type and mtime
    # For simplicity, we'll use hardcoded lists for specific test cases.
    # In a real scenario, this mock could be more sophisticated,
    # but for this utility, simple lists are sufficient.

    if [[ "$path" == "/tmp/test_path" ]]; then
        if [[ "$type_flag" == "f" && "$mtime_flag" == "+7" ]]; then
            echo "/tmp/test_path/old_file.log"
            echo "/tmp/test_path/another_old_file.txt"
        elif [[ "$type_flag" == "d" && "$mtime_flag" == "+7" ]]; then
            echo "/tmp/test_path/old_dir"
            echo "/tmp/test_path/another_old_dir"
        fi
    elif [[ "$path" == "/tmp/empty_path" ]]; then
        # No files/dirs should be found here
        :
    elif [[ "$path" == "/tmp/recent_path" ]]; then
        # No files/dirs older than +7 should be found here
        :
    elif [[ "$path" == "/tmp/specific_age_path" ]]; then
        if [[ "$type_flag" == "f" && "$mtime_flag" == "+30" ]]; then
            echo "/tmp/specific_age_path/very_old_report.pdf"
        elif [[ "$type_flag" == "d" && "$mtime_flag" == "+30" ]]; then
            echo "/tmp/specific_age_path/very_old_archive"
        fi
    fi
}

# Mock rationale: `rm` modifies the filesystem, which is non-deterministic and can lead to data loss
# if not careful. Mocking allows us to verify deletion attempts without actual filesystem changes,
# ensuring deterministic and safe test execution.
mock_rm() {
    # Record the arguments passed to rm
    echo "MOCK_RM_CALLED: $*" >> "$MOCK_RM_LOG"
    # Simulate success
    return 0
}

# Override system commands with our mocks
alias find="mock_find"
alias rm="mock_rm"

# Path to the script under test
SCRIPT_PATH="./src/dust_bunny_sweeper.sh"

# Temporary log file for mock_rm
MOCK_RM_LOG=$(mktemp)

# --- Test Helper Functions ---

# Function to run a test case
run_test() {
    local test_name="$1"
    local command="$2"
    local expected_output_regex="$3"
    local expected_exit_code="$4"
    local rm_log_check_regex="$5" # Optional regex to check mock_rm_log

    echo "--- Running Test: $test_name ---"
    
    # Clear mock_rm_log for each test
    > "$MOCK_RM_LOG"

    # Execute the script and capture output and exit code
    # We use a subshell to ensure aliases are active and don't leak
    local output
    local exit_code
    output=$(eval "$command" 2>&1)
    exit_code=$?

    echo "Command: $command"
    echo "Output:"
    echo "$output"
    echo "Exit Code: $exit_code"

    # Check exit code
    if [[ "$exit_code" -ne "$expected_exit_code" ]]; then
        echo "FAIL: $test_name - Expected exit code $expected_exit_code, got $exit_code"
        exit 1
    fi

    # Check output using regex
    if ! echo "$output" | grep -Eq "$expected_output_regex"; then
        echo "FAIL: $test_name - Output did not match expected regex."
        echo "Expected Regex: $expected_output_regex"
        exit 1
    fi

    # Check mock_rm_log if provided
    if [[ -n "$rm_log_check_regex" ]]; then
        local rm_log_content=$(cat "$MOCK_RM_LOG")
        if ! echo "$rm_log_content" | grep -Eq "$rm_log_check_regex"; then
            echo "FAIL: $test_name - MOCK_RM_LOG did not match expected regex."
            echo "RM Log Content: $rm_log_content"
            echo "Expected RM Log Regex: $rm_log_check_regex"
            exit 1
        fi
    fi

    echo "PASS: $test_name"
    echo ""
}

# --- Test Cases ---

# Test 1: Basic dry run, default age
run_test "Dry Run - Default Age" \
    "$SCRIPT_PATH /tmp/test_path" \
    "Initiating Digital Dust Bunny Sweep in '/tmp/test_path' for items older than 7 days \\(Dry Run\\)...\\n.*Found 4 digital dust bunnies:\\n--- Old Files ---\\n  - File: /tmp/test_path/old_file.log\\n  - File: /tmp/test_path/another_old_file.txt\\n--- Old Directories ---\\n  - Dir: /tmp/test_path/old_dir\\n  - Dir: /tmp/test_path/another_old_dir\\n.*To actually clean these up, run with the '--clean' option." \
    0 \
    "" # No rm calls expected

# Test 2: Dry run with specific age
run_test "Dry Run - Specific Age" \
    "$SCRIPT_PATH /tmp/specific_age_path --age 30" \
    "Initiating Digital Dust Bunny Sweep in '/tmp/specific_age_path' for items older than 30 days \\(Dry Run\\)...\\n.*Found 2 digital dust bunnies:\\n--- Old Files ---\\n  - File: /tmp/specific_age_path/very_old_report.pdf\\n--- Old Directories ---\\n  - Dir: /tmp/specific_age_path/very_old_archive" \
    0 \
    "" # No rm calls expected

# Test 3: Clean mode
run_test "Clean Mode" \
    "$SCRIPT_PATH /tmp/test_path --clean" \
    "Initiating Digital Dust Bunny Sweep in '/tmp/test_path' for items older than 7 days...\\n.*Found 4 digital dust bunnies:\\n.*Sweeping away the digital dust bunnies...\\n  🧹 Removed: /tmp/test_path/old_file.log\\n  🧹 Removed: /tmp/test_path/another_old_file.txt\\n  🧹 Removed: /tmp/test_path/old_dir\\n  🧹 Removed: /tmp/test_path/another_old_dir\\n.*Finished sweeping! 4 dust bunnies banished from your system." \
    0 \
    "MOCK_RM_CALLED: -rf /tmp/test_path/old_file.log\\nMOCK_RM_CALLED: -rf /tmp/test_path/another_old_file.txt\\nMOCK_RM_CALLED: -rf /tmp/test_path/old_dir\\nMOCK_RM_CALLED: -rf /tmp/test_path/another_old_dir"

# Test 4: No dust bunnies found
run_test "No Dust Bunnies" \
    "$SCRIPT_PATH /tmp/empty_path" \
    "Hooray! No digital dust bunnies found in '/tmp/empty_path'. Your digital space is sparkling clean!" \
    0 \
    ""

# Test 5: Invalid path
run_test "Invalid Path" \
    "$SCRIPT_PATH /non/existent/path" \
    "Error: Target path '/non/existent/path' is not a valid directory." \
    1 \
    ""

# Test 6: Missing path
run_test "Missing Path" \
    "$SCRIPT_PATH" \
    "Error: Missing <path> argument.\\nUsage: test_dust_bunny_sweeper.sh <path> \\[--age <days>\\] \\[--clean\\] \\[--help\\]" \
    1 \
    ""

# Test 7: Invalid age argument
run_test "Invalid Age Argument" \
    "$SCRIPT_PATH /tmp/test_path --age abc" \
    "Error: --age requires a numeric value.\\nUsage: test_dust_bunny_sweeper.sh <path> \\[--age <days>\\] \\[--clean\\] \\[--help\\]" \
    1 \
    ""

# Test 8: Unknown option
run_test "Unknown Option" \
    "$SCRIPT_PATH /tmp/test_path --unknown-option" \
    "Error: Unknown option '--unknown-option'.\\nUsage: test_dust_bunny_sweeper.sh <path> \\[--age <days>\\] \\[--clean\\] \\[--help\\]" \
    1 \
    ""

# Clean up mock log
rm "$MOCK_RM_LOG"

echo "All tests passed!"
