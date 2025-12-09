#!/bin/bash

# Test script for nightly-dust-bunny-sweeper

SCRIPT_PATH="../src/dust_bunny_sweeper.sh"
TEST_DIR="test_temp_dir"

# --- Helper Functions ---
setup_test_env() {
    mkdir -p "$TEST_DIR/old_dir" "$TEST_DIR/empty_dir" "$TEST_DIR/recent_dir"
    
    # Create old files (older than 30 days)
    touch -d "31 days ago" "$TEST_DIR/old_file_1.txt"
    touch -d "35 days ago" "$TEST_DIR/old_dir/old_file_2.log"
    
    # Create recent files (should not be deleted)
    touch "$TEST_DIR/recent_file.txt"
    touch "$TEST_DIR/recent_dir/recent_file_in_dir.tmp"
    
    # Create an empty file (should be considered old if its atime is old)
    touch -d "40 days ago" "$TEST_DIR/empty_content_old_file.txt"
    
    # Create a file that will make its parent dir not empty
    echo "content" > "$TEST_DIR/old_dir/not_empty.txt"
}

cleanup_test_env() {
    rm -rf "$TEST_DIR"
}

# --- Test Cases ---

test_dry_run_lists_correctly() {
    echo "--- Test: Dry run lists correct dust bunnies ---"
    setup_test_env
    
    # Mock rationale: We are testing the listing functionality, not actual deletion.
    # The 'find' command will operate on the temporary test environment, which is controlled.
    # We expect specific files and directories to be listed based on their creation/access times.
    OUTPUT=$("$SCRIPT_PATH" -d "$TEST_DIR")
    
    if echo "$OUTPUT" | grep -q "old_file_1.txt" && \
       echo "$OUTPUT" | grep -q "old_dir/old_file_2.log" && \
       echo "$OUTPUT" | grep -q "empty_dir" && \
       echo "$OUTPUT" | grep -q "empty_content_old_file.txt" && \
       ! echo "$OUTPUT" | grep -q "recent_file.txt" && \
       ! echo "$OUTPUT" | grep -q "recent_dir" && \
       ! echo "$OUTPUT" | grep -q "old_dir/not_empty.txt"; then
        echo "PASS: Dry run listed expected dust bunnies."
    else
        echo "FAIL: Dry run did not list expected dust bunnies."
        echo "Output:"
        echo "$OUTPUT"
        cleanup_test_env
        exit 1
    fi
    cleanup_test_env
}

test_cleanup_removes_correctly() {
    echo "--- Test: Cleanup removes correct dust bunnies ---"
    setup_test_env
    
    # Mock rationale: Simulate user confirmation 'y' for deletion using the -y flag.
    # This allows the script to proceed with actual file removal in the controlled test environment.
    "$SCRIPT_PATH" -y "$TEST_DIR" > /dev/null # -y flag auto-confirms, redirect output to avoid clutter
    
    if [ ! -f "$TEST_DIR/old_file_1.txt" ] && \
       [ ! -f "$TEST_DIR/old_dir/old_file_2.log" ] && \
       [ ! -d "$TEST_DIR/empty_dir" ] && \
       [ ! -f "$TEST_DIR/empty_content_old_file.txt" ] && \
       [ -f "$TEST_DIR/recent_file.txt" ] && \
       [ -d "$TEST_DIR/recent_dir" ] && \
       [ -f "$TEST_DIR/old_dir/not_empty.txt" ]; then
        echo "PASS: Cleanup removed expected dust bunnies and left recent files."
    else
        echo "FAIL: Cleanup did not remove expected dust bunnies or removed too much."
        echo "Remaining files/dirs:"
        ls -R "$TEST_DIR"
        cleanup_test_env
        exit 1
    fi
    cleanup_test_env
}

test_custom_age_works() {
    echo "--- Test: Custom age parameter works ---"
    setup_test_env
    
    # Create a file that is 10 days old
    touch -d "10 days ago" "$TEST_DIR/medium_age_file.txt"
    
    # Run with -a 5 (should include medium_age_file and older ones)
    # Mock rationale: Testing the '-a' flag's effect on 'find' command's age criteria.
    # The 'find' command will operate on the temporary test environment.
    OUTPUT=$("$SCRIPT_PATH" -d -a 5 "$TEST_DIR")
    
    if echo "$OUTPUT" | grep -q "medium_age_file.txt" && \
       echo "$OUTPUT" | grep -q "old_file_1.txt"; then
        echo "PASS: Custom age parameter (5 days) included expected files."
    else
        echo "FAIL: Custom age parameter (5 days) did not work as expected."
        echo "Output:"
        echo "$OUTPUT"
        cleanup_test_env
        exit 1
    fi
    
    # Run with -a 15 (should NOT include medium_age_file, but include older ones)
    OUTPUT=$("$SCRIPT_PATH" -d -a 15 "$TEST_DIR")
    
    if ! echo "$OUTPUT" | grep -q "medium_age_file.txt" && \
       echo "$OUTPUT" | grep -q "old_file_1.txt"; then
        echo "PASS: Custom age parameter (15 days) excluded expected files."
    else
        echo "FAIL: Custom age parameter (15 days) did not exclude expected files."
        echo "Output:"
        echo "$OUTPUT"
        cleanup_test_env
        exit 1
    fi
    cleanup_test_env
}

test_no_bunnies_message() {
    echo "--- Test: No dust bunnies message ---"
    cleanup_test_env # Ensure a clean slate
    mkdir -p "$TEST_DIR/only_recent"
    touch "$TEST_DIR/only_recent/recent.txt"

    # Mock rationale: Testing the output when no files match the criteria.
    # The 'find' command will operate on the temporary test environment.
    OUTPUT=$("$SCRIPT_PATH" -d "$TEST_DIR")

    if echo "$OUTPUT" | grep -q "No digital dust bunnies found. Your system is sparkling clean (digitally speaking)!"; then
        echo "PASS: Correct message displayed when no dust bunnies."
    else
        echo "FAIL: Incorrect message or no message when no dust bunnies."
        echo "Output:"
        echo "$OUTPUT"
        cleanup_test_env
        exit 1
    fi
    cleanup_test_env
}

# --- Run Tests ---
cleanup_test_env # Ensure clean start before running tests
test_dry_run_lists_correctly
test_cleanup_removes_correctly
test_custom_age_works
test_no_bunnies_message

echo "All tests completed."
