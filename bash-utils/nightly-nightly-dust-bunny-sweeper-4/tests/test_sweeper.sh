#!/bin/bash

# Test script for Nightly Digital Dust Bunny Sweeper

# Source the main script to get functions/variables if needed, or just call it.
# For simplicity and isolation, we'll call the script directly.

SCRIPT_PATH="./src/dust_bunny_sweeper.sh"
TEST_DIR=""

# Whimsical colors for test output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Helper function for assertions
assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [ "$expected" = "$actual" ]; then
        echo -e "${GREEN}PASS: $message${NC}"
    else
        echo -e "${RED}FAIL: $message${NC}"
        echo -e "      Expected: '$expected'"
        echo -e "      Actual:   '$actual'"
        exit 1
    fi
}

assert_file_exists() {
    local file="$1"
    local message="$2"
    if [ -f "$file" ]; then
        echo -e "${GREEN}PASS: $message${NC}"
    else
        echo -e "${RED}FAIL: $message${NC}"
        exit 1
    fi
}

assert_file_does_not_exist() {
    local file="$1"
    local message="$2"
    if [ ! -f "$file" ]; then
        echo -e "${GREEN}PASS: $message${NC}"
    else
        echo -e "${RED}FAIL: $message${NC}"
        exit 1
    fi
}

# Setup function
setup() {
    TEST_DIR=$(mktemp -d -t dust-bunny-test-XXXXX)
    echo -e "${YELLOW}Setting up test environment in $TEST_DIR${NC}"
    # Ensure the script is executable
    chmod +x "$SCRIPT_PATH"
}

# Teardown function
teardown() {
    echo -e "${YELLOW}Cleaning up test environment $TEST_DIR${NC}"
    rm -rf "$TEST_DIR"
}

# Trap to ensure teardown runs even if tests fail
trap teardown EXIT

# --- Test Cases ---

# Test 1: No files found, default criteria
test_no_files_found() {
    setup
    echo -e "${YELLOW}Running Test 1: No files found, default criteria.${NC}"
    OUTPUT=$("$SCRIPT_PATH" -d "$TEST_DIR" 2>&1)
    assert_equals "0" "$?" "Script exited with status 0"
    echo "$OUTPUT" | grep -q "No digital dust bunnies found"
    assert_equals "0" "$?" "Output indicates no dust bunnies found"
    teardown
}

# Test 2: Old file found and deleted (with confirmation)
test_old_file_deleted_with_confirm() {
    setup
    echo -e "${YELLOW}Running Test 2: Old file found and deleted (with confirmation).${NC}"
    OLD_FILE="$TEST_DIR/old_log.txt"
    touch -d "2 months ago" "$OLD_FILE" # Mock rationale: Simulates an old file for 'find' to detect.
    
    # Run script, pipe 'y' for confirmation
    OUTPUT=$(echo "y" | "$SCRIPT_PATH" -d "$TEST_DIR" -a 30 2>&1)
    assert_equals "0" "$?" "Script exited with status 0"
    echo "$OUTPUT" | grep -q "Found these digital dust bunnies"
    assert_equals "0" "$?" "Output indicates dust bunnies found"
    echo "$OUTPUT" | grep -q "Sweeping away the clutter"
    assert_equals "0" "$?" "Output indicates sweeping"
    assert_file_does_not_exist "$OLD_FILE" "Old file should be deleted"
    teardown
}

# Test 3: Large file found and deleted (with confirmation)
test_large_file_deleted_with_confirm() {
    setup
    echo -e "${YELLOW}Running Test 3: Large file found and deleted (with confirmation).${NC}"
    LARGE_FILE="$TEST_DIR/large_data.bin"
    # Mock rationale: Creates a large file for 'find' to detect.
    dd if=/dev/zero of="$LARGE_FILE" bs=1M count=150 > /dev/null 2>&1 
    
    # Run script, pipe 'y' for confirmation
    OUTPUT=$(echo "y" | "$SCRIPT_PATH" -d "$TEST_DIR" -s 100 2>&1)
    assert_equals "0" "$?" "Script exited with status 0"
    echo "$OUTPUT" | grep -q "Found these digital dust bunnies"
    assert_equals "0" "$?" "Output indicates dust bunnies found"
    assert_file_does_not_exist "$LARGE_FILE" "Large file should be deleted"
    teardown
}

# Test 4: Pattern file found and deleted (with confirmation)
test_pattern_file_deleted_with_confirm() {
    setup
    echo -e "${YELLOW}Running Test 4: Pattern file found and deleted (with confirmation).${NC}"
    PATTERN_FILE="$TEST_DIR/temp_report.tmp"
    touch "$PATTERN_FILE" # Mock rationale: Creates a file matching a pattern.
    
    # Run script, pipe 'y' for confirmation
    OUTPUT=$(echo "y" | "$SCRIPT_PATH" -d "$TEST_DIR" -p "*.tmp" 2>&1)
    assert_equals "0" "$?" "Script exited with status 0"
    echo "$OUTPUT" | grep -q "Found these digital dust bunnies"
    assert_equals "0" "$?" "Output indicates dust bunnies found"
    assert_file_does_not_exist "$PATTERN_FILE" "Pattern file should be deleted"
    teardown
}

# Test 5: No deletion if 'n' is entered
test_no_deletion_on_n() {
    setup
    echo -e "${YELLOW}Running Test 5: No deletion if 'n' is entered.${NC}"
    SHOULD_STAY_FILE="$TEST_DIR/important_config.log"
    touch -d "2 months ago" "$SHOULD_STAY_FILE" # Mock rationale: Simulates an old file.
    
    # Run script, pipe 'n' for no confirmation
    OUTPUT=$(echo "n" | "$SCRIPT_PATH" -d "$TEST_DIR" -a 30 2>&1)
    assert_equals "0" "$?" "Script exited with status 0"
    echo "$OUTPUT" | grep -q "Digital dust bunnies spared"
    assert_equals "0" "$?" "Output indicates files were spared"
    assert_file_exists "$SHOULD_STAY_FILE" "File should NOT be deleted"
    teardown
}

# Test 6: Force deletion
test_force_deletion() {
    setup
    echo -e "${YELLOW}Running Test 6: Force deletion.${NC}"
    FORCE_DELETE_FILE="$TEST_DIR/force_me.cache"
    touch -d "3 months ago" "$FORCE_DELETE_FILE" # Mock rationale: Simulates an old file.
    
    OUTPUT=$("$SCRIPT_PATH" -d "$TEST_DIR" -a 30 -f 2>&1)
    assert_equals "0" "$?" "Script exited with status 0"
    echo "$OUTPUT" | grep -q "Force deletion enabled"
    assert_equals "0" "$?" "Output indicates force deletion"
    assert_file_does_not_exist "$FORCE_DELETE_FILE" "File should be force deleted"
    teardown
}

# Test 7: Multiple patterns
test_multiple_patterns() {
    setup
    echo -e "${YELLOW}Running Test 7: Multiple patterns.${NC}"
    FILE1="$TEST_DIR/report.log"
    FILE2="$TEST_DIR/temp.tmp"
    FILE3="$TEST_DIR/keep.txt"
    touch "$FILE1" "$FILE2" "$FILE3" # Mock rationale: Creates files for pattern matching.

    OUTPUT=$(echo "y" | "$SCRIPT_PATH" -d "$TEST_DIR" -p "*.log" -p "*.tmp" 2>&1)
    assert_equals "0" "$?" "Script exited with status 0"
    assert_file_does_not_exist "$FILE1" "File1 (.log) should be deleted"
    assert_file_does_not_exist "$FILE2" "File2 (.tmp) should be deleted"
    assert_file_exists "$FILE3" "File3 (.txt) should NOT be deleted"
    teardown
}

# Test 8: Non-existent directory
test_non_existent_directory() {
    setup
    echo -e "${YELLOW}Running Test 8: Non-existent directory.${NC}"
    OUTPUT=$("$SCRIPT_PATH" -d "$TEST_DIR/non_existent" 2>&1)
    assert_equals "1" "$?" "Script exited with status 1 (error)"
    echo "$OUTPUT" | grep -q "Error: Target directory .* does not exist."
    assert_equals "0" "$?" "Error message for non-existent directory"
    teardown
}

# Test 9: Combined criteria (old OR large)
test_combined_criteria_or() {
    setup
    echo -e "${YELLOW}Running Test 9: Combined criteria (old OR large).${NC}"
    # File 1: Old but small
    OLD_SMALL_FILE="$TEST_DIR/old_small.txt"
    touch -d "2 months ago" "$OLD_SMALL_FILE" # Mock rationale: Old file.
    # File 2: New but large
    NEW_LARGE_FILE="$TEST_DIR/new_large.bin"
    dd if=/dev/zero of="$NEW_LARGE_FILE" bs=1M count=150 > /dev/null 2>&1 # Mock rationale: Large file.
    # File 3: New and small (should be kept)
    NEW_SMALL_FILE="$TEST_DIR/new_small.txt"
    touch "$NEW_SMALL_FILE" # Mock rationale: File to be kept.

    OUTPUT=$(echo "y" | "$SCRIPT_PATH" -d "$TEST_DIR" -a 30 -s 100 2>&1)
    assert_equals "0" "$?" "Script exited with status 0"
    assert_file_does_not_exist "$OLD_SMALL_FILE" "Old small file should be deleted"
    assert_file_does_not_exist "$NEW_LARGE_FILE" "New large file should be deleted"
    assert_file_exists "$NEW_SMALL_FILE" "New small file should NOT be deleted"
    teardown
}

# Test 10: Combined criteria (old OR pattern)
test_combined_criteria_old_or_pattern() {
    setup
    echo -e "${YELLOW}Running Test 10: Combined criteria (old OR pattern).${NC}"
    # File 1: Old, not pattern
    OLD_FILE="$TEST_DIR/old_doc.txt"
    touch -d "2 months ago" "$OLD_FILE"
    # File 2: New, but pattern
    PATTERN_FILE="$TEST_DIR/new_temp.tmp"
    touch "$PATTERN_FILE"
    # File 3: New, not pattern
    KEEP_FILE="$TEST_DIR/keep.log"
    touch "$KEEP_FILE"

    OUTPUT=$(echo "y" | "$SCRIPT_PATH" -d "$TEST_DIR" -a 30 -p "*.tmp" 2>&1)
    assert_equals "0" "$?" "Script exited with status 0"
    assert_file_does_not_exist "$OLD_FILE" "Old file should be deleted"
    assert_file_does_not_exist "$PATTERN_FILE" "Pattern file should be deleted"
    assert_file_exists "$KEEP_FILE" "Keep file should NOT be deleted"
    teardown
}


# Run all tests
echo -e "${GREEN}Starting all tests for Nightly Digital Dust Bunny Sweeper...${NC}"
test_no_files_found
test_old_file_deleted_with_confirm
test_large_file_deleted_with_confirm
test_pattern_file_deleted_with_confirm
test_no_deletion_on_n
test_force_deletion
test_multiple_patterns
test_non_existent_directory
test_combined_criteria_or
test_combined_criteria_old_or_pattern
echo -e "${GREEN}All tests passed! 🎉${NC}"
