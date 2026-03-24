#!/bin/bash

# Mock rationale: We need to prevent actual file deletion during tests.
# By aliasing rm and rmdir to echo, we can capture what *would* have been deleted
# without affecting the filesystem. This makes tests deterministic and safe.
alias rm='echo MOCKED_RM'
alias rmdir='echo MOCKED_RMDIR'

# Source the script to test its functions, or run it directly.
SCRIPT_TO_TEST="../src/digital_debris_duster.sh"

# Get DEFAULT_AGE_DAYS from the script itself for robust testing
DEFAULT_AGE_DAYS=$(grep -m 1 "DEFAULT_AGE_DAYS=" "$SCRIPT_TO_TEST" | cut -d'=' -f2)

# --- Test Setup ---
TEST_DIR="test_temp_dir"

setup_test_environment() {
    cd .. # Ensure we are outside the test_temp_dir if previous test failed
    rm -rf "$TEST_DIR"
    mkdir -p "$TEST_DIR"
    cd "$TEST_DIR" || exit 1

    # Create test files and directories
    # Using a fixed old date (Jan 1, 2023) to ensure files are older than DEFAULT_AGE_DAYS (30 days)
    # This makes tests deterministic regardless of the current system date (assuming current date > Feb 1, 2023).
    touch -t 202301010000 "old_file_1.txt"
    touch -t 202301010000 "old_file_2.log"
    touch "recent_file.txt" # Current date
    touch "temp_file.tmp"
    touch "backup_file.bak"
    touch "hidden_temp_file~"
    touch ".DS_Store"
    mkdir -p "empty_dir"
    mkdir -p "non_empty_dir"
    touch "non_empty_dir/file.txt"
}

# --- Test Functions ---

run_test() {
    local test_name="$1"
    local command="$2"
    local expected_output_regex="$3"
    local unexpected_output_regex="$4"
    local expected_rm_count="$5"
    local expected_rmdir_count="$6"

    echo "--- Running Test: $test_name ---"
    
    # Execute the command and capture its full output
    FULL_OUTPUT=$(eval "$command" 2>&1)

    # Count mock calls from the captured output
    MOCKED_RM_COUNT=$(echo "$FULL_OUTPUT" | grep -c 'MOCKED_RM')
    MOCKED_RMDIR_COUNT=$(echo "$FULL_OUTPUT" | grep -c 'MOCKED_RMDIR')

    # Check for expected output
    if echo "$FULL_OUTPUT" | grep -Eq "$expected_output_regex"; then
        echo "  ✅ Expected output found: '$expected_output_regex'"
    else
        echo "  ❌ Test Failed: Expected output '$expected_output_regex' not found."
        echo "     Full Output:"
        echo "$FULL_OUTPUT"
        return 1
    fi

    # Check for unexpected output
    if [ -n "$unexpected_output_regex" ] && echo "$FULL_OUTPUT" | grep -Eq "$unexpected_output_regex"; then
        echo "  ❌ Test Failed: Unexpected output '$unexpected_output_regex' found."
        echo "     Full Output:"
        echo "$FULL_OUTPUT"
        return 1
    else
        echo "  ✅ Unexpected output '$unexpected_output_regex' not found (as expected)."
    fi

    # Check mock counts
    if [ "$MOCKED_RM_COUNT" -eq "$expected_rm_count" ]; then
        echo "  ✅ MOCKED_RM calls count correct: $MOCKED_RM_COUNT (expected $expected_rm_count)"
    else
        echo "  ❌ Test Failed: MOCKED_RM calls count incorrect. Expected $expected_rm_count, got $MOCKED_RM_COUNT."
        echo "     Full Output:"
        echo "$FULL_OUTPUT"
        return 1
    fi

    if [ "$MOCKED_RMDIR_COUNT" -eq "$expected_rmdir_count" ]; then
        echo "  ✅ MOCKED_RMDIR calls count correct: $MOCKED_RMDIR_COUNT (expected $expected_rmdir_count)"
    else
        echo "  ❌ Test Failed: MOCKED_RMDIR calls count incorrect. Expected $expected_rmdir_count, got $MOCKED_RMDIR_COUNT."
        echo "     Full Output:"
        echo "$FULL_OUTPUT"
        return 1
    fi

    echo "--- Test '$test_name' Passed ---"
    return 0
}

# --- Tests ---

# Expected counts for a non-dry run with the setup_test_environment:
# Old files: old_file_1.txt, old_file_2.log (2 files)
# Temp files: temp_file.tmp, backup_file.bak, hidden_temp_file~, .DS_Store (4 files)
# Empty dirs: empty_dir (1 directory)
# Total rm: 2 + 4 = 6
# Total rmdir: 1

# Test 1: Dry run, expect detection but no deletion
setup_test_environment
run_test "Dry Run - Detection Only" \
    "$SCRIPT_TO_TEST -d ." \
    "Found these dusty relics:|Found these transient specks:|Found these vacant spaces:|Dry Run Mode: No actual deletions will occur." \
    "MOCKED_RM|MOCKED_RMDIR" \
    0 0

# Test 2: Actual run (mocked), expect deletion messages
setup_test_environment
run_test "Actual Run - Deletion (Mocked)" \
    "$SCRIPT_TO_TEST ." \
    "Swept!|Collapsed!" \
    "Dry Run Mode" \
    6 1

# Test 3: No debris scenario
# Run once to 'clean' (mocked), then test dry run again
setup_test_environment
$SCRIPT_TO_TEST . > /dev/null 2>&1 # Perform the 'cleanup' silently
run_test "No Debris Scenario" \
    "$SCRIPT_TO_TEST -d ." \
    "Your digital realm is sparkling clean! No debris detected." \
    "Found these dusty relics:|Found these transient specks:|Found these vacant spaces:" \
    0 0

# Test 4: Interactive mode (mocked input - confirm all)
setup_test_environment
# Mock rationale: `yes` command is used to simulate user input 'y' for interactive prompts.
# This ensures deterministic behavior for interactive mode tests without actual user intervention.
run_test "Interactive Run - Confirm All (Mocked)" \
    "yes | $SCRIPT_TO_TEST -i ." \
    "Swept!|Collapsed!|Sweep away '.*'? (y/N) y|Collapse '.*'? (y/N) y" \
    "Dry Run Mode" \
    6 1

# Test 5: Interactive mode (mocked input - deny all)
setup_test_environment
# Mock rationale: `printf "n\nn\nn\n"` simulates user input 'n' for interactive prompts.
# This ensures deterministic behavior for interactive mode tests where the user declines deletion.
run_test "Interactive Run - Deny All (Mocked)" \
    "printf \"n\\nn\\nn\\n\" | $SCRIPT_TO_TEST -i ." \
    "Skipped." \
    "Swept!|Collapsed!" \
    0 0

# Test 6: Specific age parameter
setup_test_environment
# Create files with different ages relative to DEFAULT_AGE_DAYS
# File older than 60 days (e.g., 202201010000)
touch -t 202201010000 "very_old_file.txt"
# File older than 30 days but not 60 (e.g., 202301010000, already created by setup)
# File not older than 30 days (e.g., recent_file.txt, already created by setup)

# Test with -a 60, only very_old_file.txt should be found
run_test "Specific Age - 60 days" \
    "$SCRIPT_TO_TEST -d -a 60 ." \
    "very_old_file.txt" \
    "old_file_1.txt|old_file_2.log|recent_file.txt" \
    0 0

# Test with -a 10, both very_old_file.txt and the two old_file_*.txt should be found
setup_test_environment
touch -t 202201010000 "very_old_file.txt"
run_test "Specific Age - 10 days" \
    "$SCRIPT_TO_TEST -d -a 10 ." \
    "very_old_file.txt|old_file_1.txt|old_file_2.log" \
    "recent_file.txt" \
    0 0

# --- Cleanup ---
cd ..
rm -rf "$TEST_DIR"

echo "All tests completed."
