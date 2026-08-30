#!/bin/bash

# Source the script to be tested to access its functions directly
. ../src/serendipity_spinner.sh

# --- Test Utilities ---
assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [ "$expected" = "$actual" ]; then
        echo "✅ Test Passed: $message"
    else
        echo "❌ Test Failed: $message"
        echo "   Expected: '$expected'"
        echo "   Actual:   '$actual'"
        exit 1
    fi
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if [[ "$haystack" == *"$needle"* ]]; then
        echo "✅ Test Passed: $message"
    else
        echo "❌ Test Failed: $message"
        echo "   Haystack: '$haystack'"
        echo "   Did not contain: '$needle'"
        exit 1
    fi
}

assert_not_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if [[ "$haystack" != *"$needle"* ]]; then
        echo "✅ Test Passed: $message"
    else
        echo "❌ Test Failed: $message"
        echo "   Haystack: '$haystack'"
        echo "   Unexpectedly contained: '$needle'"
        exit 1
    fi
}

assert_exit_code() {
    local expected_code="$1"
    local actual_code="$2"
    local message="$3"
    if [ "$expected_code" -eq "$actual_code" ]; then
        echo "✅ Test Passed: $message"
    else
        echo "❌ Test Failed: $message"
        echo "   Expected exit code: $expected_code"
        echo "   Actual exit code:   $actual_code"
        exit 1
    fi
}

# --- Mocking shuf for deterministic tests ---
# Mock rationale: The 'select_random_task' function uses 'shuf' for randomness.
# To ensure deterministic test results, we override the 'shuf' command
# to always return the first line of its input. This allows us to predict
# which task will be chosen when testing the 'main' function, given that
# 'get_tasks_for_mood' now sorts its output deterministically.
shuf() {
    head -n 1 "$@"
}
export -f shuf # Export the function so it's available in subshells when the script is run directly

# --- Test Cases ---

echo "Running tests for Serendipity Spinner..."

# Test 1: get_tasks_for_mood "low"
echo "--- Test 1: get_tasks_for_mood 'low' ---"
low_tasks=$(get_tasks_for_mood "low")
assert_contains "$low_tasks" "Rest and recuperate" "Low mood tasks should include 'Rest and recuperate'"
assert_contains "$low_tasks" "Organize inventory" "Low mood tasks should include 'Organize inventory'"
assert_contains "$low_tasks" "Tend to garden/crops" "Low mood tasks should include 'Tend to garden/crops'"
assert_contains "$low_tasks" "Clean and maintain weapons" "Low mood tasks should include 'Clean and maintain weapons'"
assert_contains "$low_tasks" "Study survival guides" "Low mood tasks should include 'Study survival guides'"
assert_not_contains "$low_tasks" "Fortify shelter defenses" "Low mood tasks should NOT include 'Fortify shelter defenses'"
assert_not_contains "$low_tasks" "Scavenge for supplies" "Low mood tasks should NOT include 'Scavenge for supplies'"

# Test 2: get_tasks_for_mood "medium"
echo "--- Test 2: get_tasks_for_mood 'medium' ---"
medium_tasks=$(get_tasks_for_mood "medium")
assert_contains "$medium_tasks" "Scavenge for supplies" "Medium mood tasks should include 'Scavenge for supplies'"
assert_contains "$medium_tasks" "Repair essential equipment" "Medium mood tasks should include 'Repair essential equipment'"
assert_contains "$medium_tasks" "Organize inventory" "Medium mood tasks should include 'Organize inventory'"
assert_contains "$medium_tasks" "Scout immediate perimeter" "Medium mood tasks should include 'Scout immediate perimeter'"
assert_contains "$medium_tasks" "Craft useful tools" "Medium mood tasks should include 'Craft useful tools'"
assert_not_contains "$medium_tasks" "Rest and recuperate" "Medium mood tasks should NOT include 'Rest and recuperate'"
assert_not_contains "$medium_tasks" "Fortify shelter defenses" "Medium mood tasks should NOT include 'Fortify shelter defenses'"

# Test 3: get_tasks_for_mood "high"
echo "--- Test 3: get_tasks_for_mood 'high' ---"
high_tasks=$(get_tasks_for_mood "high")
assert_contains "$high_tasks" "Scavenge for supplies" "High mood tasks should include 'Scavenge for supplies'"
assert_contains "$high_tasks" "Fortify shelter defenses" "High mood tasks should include 'Fortify shelter defenses'"
assert_not_contains "$high_tasks" "Rest and recuperate" "High mood tasks should NOT include 'Rest and recuperate'"
assert_not_contains "$high_tasks" "Study survival guides" "High mood tasks should NOT include 'Study survival guides'"

# Test 4: main function - No arguments
echo "--- Test 4: main function - No arguments ---"
output=$(bash ../src/serendipity_spinner.sh 2>&1)
exit_code=$?
assert_exit_code 1 "$exit_code" "Script should exit with error for no arguments"
assert_contains "$output" "Usage: ../src/serendipity_spinner.sh <mood>" "Output should contain usage message"

# Test 5: main function - Invalid mood
echo "--- Test 5: main function - Invalid mood ---"
output=$(bash ../src/serendipity_spinner.sh "unknown" 2>&1)
exit_code=$?
assert_exit_code 1 "$exit_code" "Script should exit with error for invalid mood"
assert_contains "$output" "Error: Invalid mood 'unknown'" "Output should indicate invalid mood"

# Test 6: main function - Low mood (mocked shuf picks first from filtered list)
echo "--- Test 6: main function - Low mood (mocked shuf) ---"
output=$(bash ../src/serendipity_spinner.sh "low")
exit_code=$?
assert_exit_code 0 "$exit_code" "Script should exit successfully for low mood"
assert_contains "$output" "Your Serendipity Spinner suggests:" "Output should suggest a task"
assert_contains "$output" "Clean and maintain weapons" "Output should suggest 'Clean and maintain weapons' (first low-mood task with mocked shuf after sorting)"
assert_not_contains "$output" "Fortify shelter defenses" "Output should NOT suggest 'Fortify' for low mood"

# Test 7: main function - Medium mood (mocked shuf picks first)
echo "--- Test 7: main function - Medium mood (mocked shuf) ---"
output=$(bash ../src/serendipity_spinner.sh "medium")
exit_code=$?
assert_exit_code 0 "$exit_code" "Script should exit successfully for medium mood"
assert_contains "$output" "Your Serendipity Spinner suggests:" "Output should suggest a task"
assert_contains "$output" "Clean and maintain weapons" "Output should suggest 'Clean and maintain weapons' (first medium-mood task with mocked shuf after sorting)"
assert_not_contains "$output" "Rest and recuperate" "Output should NOT suggest 'Rest and recuperate' for medium mood"

# Test 8: main function - High mood (mocked shuf picks first)
echo "--- Test 8: main function - High mood (mocked shuf) ---"
output=$(bash ../src/serendipity_spinner.sh "high")
exit_code=$?
assert_exit_code 0 "$exit_code" "Script should exit successfully for high mood"
assert_contains "$output" "Your Serendipity Spinner suggests:" "Output should suggest a task"
assert_contains "$output" "Fortify shelter defenses" "Output should suggest 'Fortify shelter defenses' (first high-mood task with mocked shuf after sorting)"
assert_not_contains "$output" "Study survival guides" "Output should NOT suggest 'Study survival guides' for high mood"

# Test 9: main function - Case insensitivity for mood
echo "--- Test 9: main function - Case insensitivity for mood ---"
output=$(bash ../src/serendipity_spinner.sh "HIGH")
exit_code=$?
assert_exit_code 0 "$exit_code" "Script should exit successfully for uppercase mood"
assert_contains "$output" "Your Serendipity Spinner suggests:" "Output should suggest a task for uppercase mood"
assert_contains "$output" "Fortify shelter defenses" "Output should suggest 'Fortify shelter defenses' for uppercase mood"

echo "All tests completed."
