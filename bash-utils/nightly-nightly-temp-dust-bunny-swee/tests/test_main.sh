#!/bin/bash

# Source the main script to test its functions or run it directly
SCRIPT_TO_TEST="../src/main.sh"

# Function to get a date string for 'N' days ago, compatible with `touch -t`
# Mock rationale: This function provides a deterministic way to generate past timestamps
# for file modification times, ensuring tests are repeatable regardless of the current date.
get_past_date_format() {
    local days_ago=$1
    local date_str=""

    # Try BSD/macOS date command
    date_str=$(date -v-"${days_ago}d" +%Y%m%d%H%M.%S 2>/dev/null)

    if [[ -z "$date_str" ]]; then
        # Fallback to GNU/Linux date command
        date_str=$(date -d "${days_ago} days ago" +%Y%m%d%H%M.%S 2>/dev/null)
    fi

    if [[ -z "$date_str" ]]; then
        echo "Error: Could not determine a compatible 'date' command for setting file times." >&2
        exit 1
    fi
    echo "$date_str"
}

# Setup a temporary directory for tests
TEST_DIR=$(mktemp -d -t dust-bunny-test-XXXXXX)
if [[ ! -d "$TEST_DIR" ]]; then
    echo "Failed to create test directory." >&2
    exit 1
fi

cleanup() {
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

echo "Running tests in $TEST_DIR"

# --- Test Case 1: Basic sweep, default age (7 days) ---
echo "Test Case 1: Basic sweep, default age (7 days)"
OLD_DATE_8D=$(get_past_date_format 8)
NEW_DATE_6D=$(get_past_date_format 6)

# Create old files/directories
touch -t "$OLD_DATE_8D" "$TEST_DIR/old_file_1.txt"
touch -t "$OLD_DATE_8D" "$TEST_DIR/old_file_2.log"
mkdir "$TEST_DIR/old_dir_1"
touch -t "$OLD_DATE_8D" "$TEST_DIR/old_dir_1" # Set dir mtime
touch -t "$OLD_DATE_8D" "$TEST_DIR/old_dir_1/inside_old.txt" # File inside old dir

# Create new files/directories
touch -t "$NEW_DATE_6D" "$TEST_DIR/new_file_1.txt"
mkdir "$TEST_DIR/new_dir_1"
touch -t "$NEW_DATE_6D" "$TEST_DIR/new_dir_1" # Set dir mtime
touch -t "$NEW_DATE_6D" "$TEST_DIR/new_dir_1/inside_new.txt" # File inside new dir

# Run the script
"$SCRIPT_TO_TEST" -d "$TEST_DIR" -a 7 > /dev/null

# Assertions
if [[ -f "$TEST_DIR/old_file_1.txt" || -f "$TEST_DIR/old_file_2.log" || -d "$TEST_DIR/old_dir_1" ]]; then
    echo "FAIL: Old files/directories were not deleted." >&2
    ls -l "$TEST_DIR" >&2
    exit 1
fi

if [[ ! -f "$TEST_DIR/new_file_1.txt" || ! -d "$TEST_DIR/new_dir_1" ]]; then
    echo "FAIL: New files/directories were unexpectedly deleted." >&2
    ls -l "$TEST_DIR" >&2
    exit 1
fi
echo "PASS: Basic sweep deleted old files and kept new ones."

cleanup
TEST_DIR=$(mktemp -d -t dust-bunny-test-XXXXXX)
trap cleanup EXIT

# --- Test Case 2: Dry run ---
echo "Test Case 2: Dry run"
OLD_DATE_10D=$(get_past_date_format 10)
touch -t "$OLD_DATE_10D" "$TEST_DIR/dry_run_old.txt"

output=$("$SCRIPT_TO_TEST" -d "$TEST_DIR" -a 7 -n)

if ! echo "$output" | grep -q "DRY RUN"; then
    echo "FAIL: Dry run message not found." >&2
    echo "$output" >&2
    exit 1
fi
if ! echo "$output" | grep -q "$TEST_DIR/dry_run_old.txt"; then
    echo "FAIL: Dry run did not list old file." >&2
    echo "$output" >&2
    exit 1
fi
if [[ ! -f "$TEST_DIR/dry_run_old.txt" ]]; then
    echo "FAIL: Dry run deleted file." >&2
    exit 1
fi
echo "PASS: Dry run correctly identified files without deleting them."

cleanup
TEST_DIR=$(mktemp -d -t dust-bunny-test-XXXXXX)
trap cleanup EXIT

# --- Test Case 3: Custom age ---
echo "Test Case 3: Custom age (3 days)"
OLD_DATE_4D=$(get_past_date_format 4)
NEW_DATE_2D=$(get_past_date_format 2)

touch -t "$OLD_DATE_4D" "$TEST_DIR/custom_age_old.txt"
touch -t "$NEW_DATE_2D" "$TEST_DIR/custom_age_new.txt"

"$SCRIPT_TO_TEST" -d "$TEST_DIR" -a 3 > /dev/null

if [[ -f "$TEST_DIR/custom_age_old.txt" ]]; then
    echo "FAIL: Custom age old file not deleted." >&2
    exit 1
fi
if [[ ! -f "$TEST_DIR/custom_age_new.txt" ]]; then
    echo "FAIL: Custom age new file deleted." >&2
    exit 1
fi
echo "PASS: Custom age sweep worked correctly."

cleanup
TEST_DIR=$(mktemp -d -t dust-bunny-test-XXXXXX)
trap cleanup EXIT

# --- Test Case 4: Invalid directory ---
echo "Test Case 4: Invalid directory"
output=$("$SCRIPT_TO_TEST" -d "/nonexistent/path/123" 2>&1 > /dev/null)
if ! echo "$output" | grep -q "Error: Target directory '/nonexistent/path/123' does not exist."; then
    echo "FAIL: Did not catch invalid directory." >&2
    echo "$output" >&2
    exit 1
fi
echo "PASS: Invalid directory handled."

cleanup
TEST_DIR=$(mktemp -d -t dust-bunny-test-XXXXXX)
trap cleanup EXIT

# --- Test Case 5: Invalid age ---
echo "Test Case 5: Invalid age"
output=$("$SCRIPT_TO_TEST" -d "$TEST_DIR" -a "abc" 2>&1 > /dev/null)
if ! echo "$output" | grep -q "Error: Age in days must be a non-negative integer."; then
    echo "FAIL: Did not catch invalid age (abc)." >&2
    echo "$output" >&2
    exit 1
fi
output=$("$SCRIPT_TO_TEST" -d "$TEST_DIR" -a "-5" 2>&1 > /dev/null)
if ! echo "$output" | grep -q "Error: Age in days must be a non-negative integer."; then
    echo "FAIL: Did not catch invalid age (-5)." >&2
    echo "$output" >&2
    exit 1
fi
echo "PASS: Invalid age handled."

echo "All tests passed!"
