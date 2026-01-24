#!/bin/bash

# Mock rationale:
# - `find` command is mocked to control the output and avoid actual filesystem scans during tests.
# - `rm` command is mocked to prevent actual file deletion during tests.
# - `read` command is mocked using `echo` to simulate user input for deterministic tests.
# - `date` command is mocked to control the current time for age calculations (less critical due to `find` mock).

# --- Test Setup ---
TEST_DIR=$(mktemp -d -t dust-bunny-test-XXXXXX)
SCRIPT_PATH="$(dirname "$0")"/../src/dust_bunny_sweeper.sh
EXIT_CODE=0

# Create a mock environment
export PATH="$TEST_DIR:$PATH" # Add TEST_DIR to PATH so our mock commands are found first

# Mock `find`
cat << 'EOF' > "$TEST_DIR/find"
#!/bin/bash
# Mock rationale: Simulate `find` command output for specific test scenarios.
# This mock is designed to be simple and only respond to the specific arguments
# used by the dust_bunny_sweeper.sh script for finding files/dirs older than N days.
# It does not fully replicate `find`'s complex behavior.

# Expected arguments: <path> -depth -type f -o -type d -mtime +<days> -print0
# We'll just check for the -mtime argument and return predefined "old" files.

MOCK_PATH="$1"
MOCK_MTIME_ARG=""
for arg in "$@"; do
    if [[ "$arg" == -mtime* ]]; then
        MOCK_MTIME_ARG="$arg"
        break
    fi
done

# Simulate finding files older than 0 days (i.e., all files) or 30 days (default)
# For testing purposes, we'll return specific mock files based on the path and age.
# These files are expected to be created by the test setup for `rm` mock to log.
if [[ "$MOCK_MTIME_ARG" == "-mtime+0" || "$MOCK_MTIME_ARG" == "-mtime+30" ]]; then
    if [[ "$MOCK_PATH" == *"/test_path_old"* ]]; then
        echo -ne "${MOCK_PATH}/old_file_1.txt\0"
        echo -ne "${MOCK_PATH}/old_dir_1\0"
        echo -ne "${MOCK_PATH}/old_dir_1/nested_old_file.log\0"
    elif [[ "$MOCK_PATH" == *"/test_path_mixed"* ]]; then
        echo -ne "${MOCK_PATH}/old_file_2.txt\0"
    fi
else
    # Default: no files found for other mtime values or paths
    true # Do nothing, output empty
fi
EOF
chmod +x "$TEST_DIR/find"

# Mock `rm`
cat << 'EOF' > "$TEST_DIR/rm"
#!/bin/bash
# Mock rationale: Prevent actual file deletion during tests.
# Instead, log what would have been deleted to a temporary file.
echo "MOCKED_RM: $@" >> "$TEST_DIR/mock_rm_log.txt"
true # Always succeed for the mock
EOF
chmod +x "$TEST_DIR/rm"

# Mock `date` for consistent age calculation (though `find -mtime` handles this)
# This mock is less critical as `find -mtime` is mocked, but good practice for completeness.
cat << 'EOF' > "$TEST_DIR/date"
#!/bin/bash
# Mock rationale: Ensure deterministic date for any date-related logic.
# For this script, `find -mtime` handles the date logic internally,
# but if the script were to use `date` for comparisons, this would be crucial.
echo "2023-01-01" # A fixed date for testing
EOF
chmod +x "$TEST_DIR/date"


# Helper function to run a test
run_test() {
    local test_name="$1"
    local command="$2"
    local expected_output_regex="$3"
    local expected_exit_code="$4"
    local mock_input="${5:-}" # Optional mock input for `read`

    echo "--- Running Test: $test_name ---"

    # Clear mock rm log for each test
    > "$TEST_DIR/mock_rm_log.txt"

    # Run the command, capturing stdout and stderr
    if [ -n "$mock_input" ]; then
        ACTUAL_OUTPUT=$(echo "$mock_input" | eval "$command" 2>&1)
    else
        ACTUAL_OUTPUT=$(eval "$command" 2>&1)
    fi
    ACTUAL_EXIT_CODE=$?

    # Check exit code
    if [ "$ACTUAL_EXIT_CODE" -ne "$expected_exit_code" ]; then
        echo "FAIL: $test_name - Expected exit code $expected_exit_code, got $ACTUAL_EXIT_CODE"
        echo "Output: $ACTUAL_OUTPUT"
        EXIT_CODE=1
        return
    fi

    # Check output using regex
    if [[ ! "$ACTUAL_OUTPUT" =~ $expected_output_regex ]]; then
        echo "FAIL: $test_name - Output mismatch"
        echo "Expected regex: $expected_output_regex"
        echo "Actual output: $ACTUAL_OUTPUT"
        EXIT_CODE=1
        return
    fi

    echo "PASS: $test_name"
}

# --- Test Cases ---

# Test 1: No dust bunnies found
run_test "No dust bunnies" \
    "$SCRIPT_PATH -p $TEST_DIR/non_existent_path -a 1" \
    "No digital dust bunnies found! Your system is sparkling clean." \
    0

# Test 2: Dry run mode, finds dust bunnies
# Create mock files/dirs for the mock `find` to "find" (for rm mock logging)
mkdir -p "$TEST_DIR/test_path_old/old_dir_1"
touch "$TEST_DIR/test_path_old/old_file_1.txt"
touch "$TEST_DIR/test_path_old/old_dir_1/nested_old_file.log"

run_test "Dry run finds bunnies" \
    "$SCRIPT_PATH -p $TEST_DIR/test_path_old -a 30 -d" \
    "Found 3 digital dust bunnies:\n  - $TEST_DIR/test_path_old/old_file_1.txt\n  - $TEST_DIR/test_path_old/old_dir_1\n  - $TEST_DIR/test_path_old/old_dir_1/nested_old_file.log\n\nDry run complete. No files were deleted." \
    0

# Test 3: Deletion confirmed (auto-yes)
# Create mock files/dirs for the mock `find` to "find" (for rm mock logging)
mkdir -p "$TEST_DIR/test_path_mixed"
touch "$TEST_DIR/test_path_mixed/old_file_2.txt"
touch "$TEST_DIR/test_path_mixed/new_file.txt" # This one should not be "found" by mock find

run_test "Deletion with auto-yes" \
    "$SCRIPT_PATH -p $TEST_DIR/test_path_mixed -a 30 -y" \
    "Found 1 digital dust bunnies:\n  - $TEST_DIR/test_path_mixed/old_file_2.txt\n\nSweeping away digital dust bunnies...\n  - Swept away: $TEST_DIR/test_path_mixed/old_file_2.txt\n\u2728 Digital dust bunny sweep complete!" \
    0

# Verify `rm` was called for the auto-yes case
if ! grep -q "MOCKED_RM: -rf \"$TEST_DIR/test_path_mixed/old_file_2.txt\"" "$TEST_DIR/mock_rm_log.txt"; then
    echo "FAIL: Deletion with auto-yes - Mocked rm was not called as expected."
    EXIT_CODE=1
fi

# Test 4: Deletion denied (manual 'n')
run_test "Deletion denied" \
    "$SCRIPT_PATH -p $TEST_DIR/test_path_old -a 30" \
    "Found 3 digital dust bunnies:.*Sweep aborted. Digital dust bunnies remain." \
    0 \
    "n"

# Verify `rm` was NOT called for the denied case
if grep -q "MOCKED_RM" "$TEST_DIR/mock_rm_log.txt"; then
    echo "FAIL: Deletion denied - Mocked rm was called unexpectedly."
    EXIT_CODE=1
fi

# Test 5: Invalid age argument
run_test "Invalid age argument" \
    "$SCRIPT_PATH -a abc" \
    "Error: Age must be a positive integer.\nUsage: $SCRIPT_PATH" \
    1

# Test 6: Help message
run_test "Help message" \
    "$SCRIPT_PATH -h" \
    "Usage: $SCRIPT_PATH" \
    1

# --- Cleanup ---
rm -rf "$TEST_DIR"
exit $EXIT_CODE
