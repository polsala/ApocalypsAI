#!/bin/bash

# Mock rationale: We need to test the script's behavior with a controlled manifest file
# without affecting any real user data or relying on external file system state.
# Creating and cleaning up a temporary file ensures deterministic and isolated tests.

SCRIPT_PATH="./src/scavenger-manifest.sh"
TEST_MANIFEST="test_manifest.txt"

# Helper function to run the script and capture output/exit code
run_script() {
    local cmd=($@)
    # Redirect stdout and stderr to a temporary file
    local output_file=$(mktemp)
    # Run the script, passing the test manifest file as the target
    # Mock rationale: Overriding MANIFEST_FILE to point to a test-specific file.
    # This ensures tests are isolated and don't interfere with each other or real data.
    MANIFEST_FILE="$TEST_MANIFEST" "$SCRIPT_PATH" "${cmd[@]}" > "$output_file" 2>&1
    local exit_code=$?
    cat "$output_file" # Print output for debugging if test fails
    rm "$output_file"
    return $exit_code
}

# Setup function for each test
setup() {
    rm -f "$TEST_MANIFEST" # Ensure a clean slate
    touch "$TEST_MANIFEST" # Create an empty manifest for tests
}

# Teardown function for each test
teardown() {
    rm -f "$TEST_MANIFEST"
}

# Test counter
TEST_COUNT=0
FAIL_COUNT=0

# Assertion functions
assert_equals() {
    TEST_COUNT=$((TEST_COUNT + 1))
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "$actual" == "$expected" ]]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message"
        echo "  Expected: '$expected'"
        echo "  Actual:   '$actual'"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}

assert_contains() {
    TEST_COUNT=$((TEST_COUNT + 1))
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if [[ "$haystack" == *"$needle"* ]]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message"
        echo "  Expected to contain: '$needle'"
        echo "  Actual:              '$haystack'"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}

assert_not_contains() {
    TEST_COUNT=$((TEST_COUNT + 1))
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if [[ "$haystack" != *"$needle"* ]]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message"
        echo "  Expected NOT to contain: '$needle'"
        echo "  Actual:                  '$haystack'"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}

assert_exit_code() {
    TEST_COUNT=$((TEST_COUNT + 1))
    local expected_code="$1"
    local actual_code="$2"
    local message="$3"
    if [[ "$actual_code" -eq "$expected_code" ]]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message"
        echo "  Expected exit code: $expected_code"
        echo "  Actual exit code:   $actual_code"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}

assert_file_exists() {
    TEST_COUNT=$((TEST_COUNT + 1))
    local file="$1"
    local message="$2"
    if [ -f "$file" ]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message"
        echo "  File '$file' does not exist."
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}

assert_file_content() {
    TEST_COUNT=$((TEST_COUNT + 1))
    local file="$1"
    local expected_content="$2"
    local message="$3"
    local actual_content=$(cat "$file" 2>/dev/null)
    if [[ "$actual_content" == "$expected_content" ]]; then
        echo "PASS: $message"
    else
        echo "FAIL: $message"
        echo "  File: '$file'"
        echo "  Expected content: '$expected_content'"
        echo "  Actual content:   '$actual_content'"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}

# --- Test Cases ---

test_init_creates_file() {
    setup
    echo "--- Running test_init_creates_file ---"
    rm -f "$TEST_MANIFEST" # Ensure it doesn't exist before init
    run_script init
    assert_exit_code 0 $? "init command should exit with 0"
    assert_file_exists "$TEST_MANIFEST" "manifest.txt should be created by init"
    assert_file_content "$TEST_MANIFEST" "" "manifest.txt should be empty after init"
    teardown
}

test_add_new_item() {
    setup
    echo "--- Running test_add_new_item ---"
    run_script add FOOD "Canned Beans" 5
    assert_exit_code 0 $? "add command should exit with 0"
    assert_file_content "$TEST_MANIFEST" "FOOD: Canned Beans: 5" "manifest should contain the new item"
    teardown
}

test_add_multiple_items() {
    setup
    echo "--- Running test_add_multiple_items ---"
    run_script add FOOD "Canned Beans" 5
    run_script add WEAPON "Rusty Pipe" 1
    run_script add TOOL "Wrench" 2
    assert_exit_code 0 $? "add command for second item should exit with 0"
    local expected_content="FOOD: Canned Beans: 5\nWEAPON: Rusty Pipe: 1\nTOOL: Wrench: 2"
    assert_file_content "$TEST_MANIFEST" "$expected_content" "manifest should contain all added items in order"
    teardown
}

test_add_updates_existing_item_quantity() {
    setup
    echo "--- Running test_add_updates_existing_item_quantity ---"
    run_script add FOOD "Canned Beans" 5
    run_script add FOOD "Canned Beans" 3
    assert_exit_code 0 $? "add command update should exit with 0"
    assert_file_content "$TEST_MANIFEST" "FOOD: Canned Beans: 8" "quantity should be updated for existing item"
    teardown
}

test_add_updates_existing_item_quantity_with_other_items() {
    setup
    echo "--- Running test_add_updates_existing_item_quantity_with_other_items ---"
    run_script add FOOD "Canned Beans" 5
    run_script add WEAPON "Rusty Pipe" 1
    run_script add TOOL "Wrench" 2
    run_script add FOOD "Canned Beans" 3 # This should update the first Canned Beans entry
    local expected_content="FOOD: Canned Beans: 8\nWEAPON: Rusty Pipe: 1\nTOOL: Wrench: 2"
    assert_file_content "$TEST_MANIFEST" "$expected_content" "manifest should have updated quantity and preserved order"
    teardown
}

test_add_invalid_quantity_fails() {
    setup
    echo "--- Running test_add_invalid_quantity_fails ---"
    run_script add FOOD "Canned Beans" "abc"
    assert_exit_code 1 $? "add with invalid quantity should fail"
    assert_file_content "$TEST_MANIFEST" "" "manifest should remain empty"
    teardown
}

test_list_all_items() {
    setup
    echo "--- Running test_list_all_items ---"
    echo "FOOD: Canned Beans: 5" >> "$TEST_MANIFEST"
    echo "WEAPON: Rusty Pipe: 1" >> "$TEST_MANIFEST"
    local output=$(run_script list)
    assert_exit_code 0 $? "list command should exit with 0"
    assert_contains "$output" "FOOD: Canned Beans: 5" "list output should contain first item"
    assert_contains "$output" "WEAPON: Rusty Pipe: 1" "list output should contain second item"
    teardown
}

test_list_by_category() {
    setup
    echo "--- Running test_list_by_category ---"
    echo "FOOD: Canned Beans: 5" >> "$TEST_MANIFEST"
    echo "WEAPON: Rusty Pipe: 1" >> "$TEST_MANIFEST"
    echo "FOOD: Purified Water: 10" >> "$TEST_MANIFEST"
    local output=$(run_script list FOOD)
    assert_exit_code 0 $? "list by category should exit with 0"
    assert_contains "$output" "FOOD: Canned Beans: 5" "list output should contain food item 1"
    assert_contains "$output" "FOOD: Purified Water: 10" "list output should contain food item 2"
    assert_not_contains "$output" "WEAPON: Rusty Pipe: 1" "list output should not contain weapon item"
    teardown
}

test_summary_empty_manifest() {
    setup
    echo "--- Running test_summary_empty_manifest ---"
    local output=$(run_script summary)
    assert_exit_code 0 $? "summary on empty manifest should exit with 0"
    assert_contains "$output" "Manifest is empty." "summary output should indicate empty manifest"
    teardown
}

test_summary_single_item() {
    setup
    echo "--- Running test_summary_single_item ---"
    echo "FOOD: Canned Beans: 5" >> "$TEST_MANIFEST"
    local output=$(run_script summary)
    assert_exit_code 0 $? "summary on single item should exit with 0"
    assert_equals "Canned Beans: 5" "$(echo "$output" | head -n 1)" "summary output should be correct for single item"
    teardown
}

test_summary_multiple_items_same_name_different_category() {
    setup
    echo "--- Running test_summary_multiple_items_same_name_different_category ---"
    echo "FOOD: Rope: 2" >> "$TEST_MANIFEST"
    echo "TOOL: Rope: 3" >> "$TEST_MANIFEST"
    local output=$(run_script summary)
    assert_exit_code 0 $? "summary should exit with 0"
    assert_contains "$output" "Rope: 5" "summary should sum quantities for same item name across categories"
    teardown
}

test_summary_multiple_items_different_names() {
    setup
    echo "--- Running test_summary_multiple_items_different_names ---"
    run_script add FOOD "Canned Beans" 5
    run_script add WEAPON "Rusty Pipe" 1
    run_script add FOOD "Purified Water" 10
    run_script add FOOD "Canned Beans" 2 # This should update the first Canned Beans entry
    local output=$(run_script summary)
    assert_exit_code 0 $? "summary should exit with 0"
    assert_contains "$output" "Canned Beans: 7" "summary should show correct total for Canned Beans"
    assert_contains "$output" "Purified Water: 10" "summary should show correct total for Purified Water"
    assert_contains "$output" "Rusty Pipe: 1" "summary should show correct total for Rusty Pipe"
    teardown
}

test_check_item_exists() {
    setup
    echo "--- Running test_check_item_exists ---"
    echo "FOOD: Canned Beans: 5" >> "$TEST_MANIFEST"
    run_script check "Canned Beans"
    assert_exit_code 0 $? "check for existing item should exit with 0"
    teardown
}

test_check_item_does_not_exist() {
    setup
    echo "--- Running test_check_item_does_not_exist ---"
    echo "FOOD: Canned Beans: 5" >> "$TEST_MANIFEST"
    run_script check "Medical Kit"
    assert_exit_code 1 $? "check for non-existing item should exit with 1"
    teardown
}

test_check_item_case_insensitive() {
    setup
    echo "--- Running test_check_item_case_insensitive ---"
    echo "FOOD: Canned Beans: 5" >> "$TEST_MANIFEST"
    run_script check "canned beans"
    assert_exit_code 0 $? "check for existing item (case-insensitive) should exit with 0"
    teardown
}

test_list_category_case_insensitive() {
    setup
    echo "--- Running test_list_category_case_insensitive ---"
    echo "FOOD: Canned Beans: 5" >> "$TEST_MANIFEST"
    echo "WEAPON: Rusty Pipe: 1" >> "$TEST_MANIFEST"
    local output=$(run_script list food)
    assert_exit_code 0 $? "list by category (case-insensitive) should exit with 0"
    assert_contains "$output" "FOOD: Canned Beans: 5" "list output should contain food item"
    assert_not_contains "$output" "WEAPON: Rusty Pipe: 1" "list output should not contain weapon item"
    teardown
}

# Run all tests
echo "Starting tests for scavenger-manifest.sh"
test_init_creates_file
test_add_new_item
test_add_multiple_items
test_add_updates_existing_item_quantity
test_add_updates_existing_item_quantity_with_other_items
test_add_invalid_quantity_fails
test_list_all_items
test_list_by_category
test_summary_empty_manifest
test_summary_single_item
test_summary_multiple_items_same_name_different_category
test_summary_multiple_items_different_names
test_check_item_exists
test_check_item_does_not_exist
test_check_item_case_insensitive
test_list_category_case_insensitive

echo "--- Test Results ---"
echo "Total tests: $TEST_COUNT"
echo "Failed tests: $FAIL_COUNT"

if [ "$FAIL_COUNT" -eq 0 ]; then
    echo "All tests passed!"
    exit 0
else
    echo "Some tests failed."
    exit 1
fi
