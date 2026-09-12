#!/bin/bash

# Test script for apocalypse_tasks.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
SCRIPT="$SCRIPT_DIR/apocalypse_tasks.sh"

# Mock rationale: Use a temporary file for tasks to ensure tests are isolated and deterministic.
# This prevents interference with any real user task file and makes tests repeatable.
TEMP_TASK_FILE=$(mktemp)
export APOCALYPSE_TASK_FILE="$TEMP_TASK_FILE"

# Cleanup function
cleanup() {
    rm -f "$TEMP_TASK_FILE"
}
trap cleanup EXIT

# Test counter
TEST_COUNT=0
PASS_COUNT=0

# Helper function for assertions
assert_equals() {
    TEST_COUNT=$((TEST_COUNT + 1))
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "$expected" == "$actual" ]]; then
        echo "PASS: $message"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo "FAIL: $message"
        echo "  Expected: '$expected'"
        echo "  Actual:   '$actual'"
    fi
}

assert_contains() {
    TEST_COUNT=$((TEST_COUNT + 1))
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if echo "$haystack" | grep -q "$needle"; then
        echo "PASS: $message"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo "FAIL: $message"
        echo "  Haystack did not contain: '$needle'"
        echo "  Haystack: '$haystack'"
    fi
}

assert_not_contains() {
    TEST_COUNT=$((TEST_COUNT + 1))
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if ! echo "$haystack" | grep -q "$needle"; then
        echo "PASS: $message"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo "FAIL: $message"
        echo "  Haystack unexpectedly contained: '$needle'"
        echo "  Haystack: '$haystack'"
    fi
}

# --- Test Cases ---

echo "Running tests for apocalypse_tasks.sh..."

# Test 1: Initial file creation
rm -f "$TEMP_TASK_FILE" # Ensure it's clean for this test
"$SCRIPT" list > /dev/null # Trigger init
assert_equals "$(head -n 1 "$TEMP_TASK_FILE")" "# Apocalypse Task Log - Created $(date +%Y-%m-%d)" "Task file created with correct header"
# Mock rationale: The date is dynamic but formatted to YYYY-MM-DD, allowing deterministic comparison for the header line.

# Test 2: Add a task
"$SCRIPT" add CRITICAL 1 "Secure the last can of irradiated peaches"
assert_contains "$(cat "$TEMP_TASK_FILE")" "1 | [ ] | CRITICAL | 1 | Secure the last can of irradiated peaches" "Task 1 added correctly"

# Test 3: Add another task
"$SCRIPT" add SCAVENGE 3 "Scavenge for spare parts in Sector 7"
assert_contains "$(cat "$TEMP_TASK_FILE")" "2 | [ ] | SCAVENGE | 3 | Scavenge for spare parts in Sector 7" "Task 2 added correctly"

# Test 4: Add a task with invalid category
OUTPUT=$("$SCRIPT" add INVALID 2 "Find a unicorn horn" 2>&1)
assert_contains "$OUTPUT" "Error: Invalid category." "Invalid category rejected"
assert_not_contains "$(cat "$TEMP_TASK_FILE")" "Find a unicorn horn" "Invalid task not added"

# Test 5: Add a task with invalid priority
OUTPUT=$("$SCRIPT" add MORALE 6 "Tell a joke to a sentient dust bunny" 2>&1)
assert_contains "$OUTPUT" "Error: Priority must be a number between 1 and 5." "Invalid priority rejected"
assert_not_contains "$(cat "$TEMP_TASK_FILE")" "Tell a joke to a sentient dust bunny" "Invalid task not added"

# Test 6: List all tasks
OUTPUT=$("$SCRIPT" list)
assert_contains "$OUTPUT" "ID: 1 | Status: [ ] | Cat: CRITICAL | Prio: 1 | Task: Secure the last can of irradiated peaches" "List contains task 1"
assert_contains "$OUTPUT" "ID: 2 | Status: [ ] | Cat: SCAVENGE | Prio: 3 | Task: Scavenge for spare parts in Sector 7" "List contains task 2"
assert_contains "$OUTPUT" "Wasteland Wisdom:" "List contains a wisdom tip"
# Mock rationale: The wisdom tip is random, so we only assert its presence, not its specific content.

# Test 7: List tasks by category (CRITICAL)
OUTPUT=$("$SCRIPT" list CRITICAL)
assert_contains "$OUTPUT" "ID: 1 | Status: [ ] | Cat: CRITICAL | Prio: 1 | Task: Secure the last can of irradiated peaches" "List filtered by CRITICAL contains task 1"
assert_not_contains "$OUTPUT" "ID: 2 | Status: [ ] | Cat: SCAVENGE | Prio: 3 | Task: Scavenge for spare parts in Sector 7" "List filtered by CRITICAL does not contain task 2"

# Test 8: Complete a task
"$SCRIPT" complete 1
assert_contains "$(cat "$TEMP_TASK_FILE")" "1 | [X] | CRITICAL | 1 | Secure the last can of irradiated peaches" "Task 1 marked as completed in file"

# Test 9: List tasks after completion (task 1 should show as [X])
OUTPUT=$("$SCRIPT" list)
assert_contains "$OUTPUT" "ID: 1 | Status: [X] | Cat: CRITICAL | Prio: 1 | Task: Secure the last can of irradiated peaches" "List shows task 1 as completed"
assert_contains "$OUTPUT" "ID: 2 | Status: [ ] | Cat: SCAVENGE | Prio: 3 | Task: Scavenge for spare parts in Sector 7" "List shows task 2 as pending"

# Test 10: Try to complete an already completed task
OUTPUT=$("$SCRIPT" complete 1 2>&1)
assert_contains "$OUTPUT" "Error: Task ID 1 not found or already completed." "Cannot complete already completed task"

# Test 11: Clear completed tasks
"$SCRIPT" clear
assert_not_contains "$(cat "$TEMP_TASK_FILE")" "1 | [X] | CRITICAL | 1 | Secure the last can of irradiated peaches" "Completed task 1 cleared from file"
assert_contains "$(cat "$TEMP_TASK_FILE")" "2 | [ ] | SCAVENGE | 3 | Scavenge for spare parts in Sector 7" "Pending task 2 remains after clear"

# Test 12: Add a new task after clearing (ID should increment correctly)
"$SCRIPT" add MORALE 2 "Organize a post-apocalyptic poetry slam"
assert_contains "$(cat "$TEMP_TASK_FILE")" "3 | [ ] | MORALE | 2 | Organize a post-apocalyptic poetry slam" "New task ID increments correctly after clear"

# Test 13: List an empty category
OUTPUT=$("$SCRIPT" list TEMPORAL)
assert_contains "$OUTPUT" "No tasks found for category 'TEMPORAL'." "Correct message for empty category"

# Test 14: List when no tasks exist
rm -f "$TEMP_TASK_FILE" # Clear file completely
OUTPUT=$("$SCRIPT" list)
assert_contains "$OUTPUT" "No tasks found. Time to scavenge for new objectives!" "Correct message for no tasks"

echo "--- Test Summary ---"
echo "Total tests: $TEST_COUNT"
echo "Passed: $PASS_COUNT"
echo "Failed: $((TEST_COUNT - PASS_COUNT))"

if [[ "$PASS_COUNT" -eq "$TEST_COUNT" ]]; then
    echo "All tests passed!"
    exit 0
else
    echo "Some tests failed."
    exit 1
fi
