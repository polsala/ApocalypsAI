#!/bin/bash

# Test script for nightly-doom-list-prioritizer

# Source the script to test functions directly, but run main logic via subprocess
# This allows mocking functions like get_random_comment
source src/doom_list_prioritizer.sh

# --- Test Utilities ---

# Function to assert equality
assert_equal() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "$expected" == "$actual" ]]; then
        echo "✅ PASS: $message"
    else
        echo "❌ FAIL: $message"
        echo "    Expected: '$expected'"
        echo "    Actual:   '$actual'"
        exit 1
    fi
}

# Function to assert contains
assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if [[ "$haystack" == *"$needle"* ]]; then
        echo "✅ PASS: $message"
    else
        echo "❌ FAIL: $message"
        echo "    Haystack: '$haystack'"
        echo "    Did not contain: '$needle'"
        exit 1
    fi
}

# --- Mocking for Deterministic Tests ---
# Mock rationale: The get_random_comment function in the main script uses RANDOM for selection.
# To make tests deterministic, we override this function here to always return the first comment
# from the relevant category array. This ensures consistent test results without relying on randomness.

# Override get_random_comment for deterministic testing
# This function is sourced, so we can redefine it.
get_random_comment() {
    local doom_level_for_comment=$1 # This is the highest individual keyword score, not the sum
    local comments_array_name

    if (( doom_level_for_comment >= 4 )); then
        comments_array_name="HIGH_DOOM_COMMENTS"
    elif (( doom_level_for_comment >= 2 )); then
        comments_array_name="MEDIUM_DOOM_COMMENTS"
    else
        comments_array_name="LOW_DOOM_COMMENTS"
    fi
    
    # Always pick the first comment for deterministic tests
    echo "${!comments_array_name:0:1}"
}


# --- Test Cases ---

echo "Running tests for nightly-doom-list-prioritizer..."

# Test 1: calculate_doom_factor - High Doom
test_task="Repair the temporal rift stabilizer"
read -r doom_factor highest_doom_level <<< "$(calculate_doom_factor "$test_task")"
assert_equal "5" "$doom_factor" "High doom factor for 'temporal rift'"
assert_equal "5" "$highest_doom_level" "Highest doom level for 'temporal rift'"

# Test 2: calculate_doom_factor - Medium Doom
test_task="Scavenge for water filters"
read -r doom_factor highest_doom_level <<< "$(calculate_doom_factor "$test_task")"
assert_equal "2" "$doom_factor" "Medium doom factor for 'water'"
assert_equal "2" "$highest_doom_level" "Highest doom level for 'water'"

# Test 3: calculate_doom_factor - Low Doom
test_task="Organize the canned goods"
read -r doom_factor highest_doom_level <<< "$(calculate_doom_factor "$test_task")"
assert_equal "1" "$doom_factor" "Low doom factor for 'organize'"
assert_equal "1" "$highest_doom_level" "Highest doom level for 'organize'"

# Test 4: calculate_doom_factor - Multiple Keywords (mixed)
test_task="Fortify the shelter and scavenge for food"
read -r doom_factor highest_doom_level <<< "$(calculate_doom_factor "$test_task")"
# shelter (4) + scavenge (3) + food (2) = 9
assert_equal "9" "$doom_factor" "Mixed doom factor for 'shelter', 'scavenge', 'food'"
assert_equal "4" "$highest_doom_level" "Highest doom level for 'shelter'"

# Test 5: calculate_doom_factor - No Keywords (default low)
test_task="Write a haiku about the void"
read -r doom_factor highest_doom_level <<< "$(calculate_doom_factor "$test_task")"
assert_equal "1" "$doom_factor" "Default low doom factor for no keywords"
assert_equal "1" "$highest_doom_level" "Default highest doom level for no keywords"

# Test 6: get_urgency_label
assert_equal "CRITICAL" "$(get_urgency_label 5)" "Urgency label CRITICAL for factor 5"
assert_equal "CRITICAL" "$(get_urgency_label 4)" "Urgency label CRITICAL for factor 4"
assert_equal "HIGH" "$(get_urgency_label 3)" "Urgency label HIGH for factor 3"
assert_equal "HIGH" "$(get_urgency_label 2)" "Urgency label HIGH for factor 2"
assert_equal "LOW" "$(get_urgency_label 1)" "Urgency label LOW for factor 1"
assert_equal "LOW" "$(get_urgency_label 0)" "Urgency label LOW for factor 0" # Should default to 1, but testing function directly

# Test 7: get_random_comment (mocked to be deterministic)
assert_equal "${HIGH_DOOM_COMMENTS[0]}" "$(get_random_comment 5)" "Deterministic high doom comment"
assert_equal "${MEDIUM_DOOM_COMMENTS[0]}" "$(get_random_comment 3)" "Deterministic medium doom comment"
assert_equal "${LOW_DOOM_COMMENTS[0]}" "$(get_random_comment 1)" "Deterministic low doom comment"

# Test 8: End-to-end with multiple tasks, piped input
echo "--- End-to-end test with piped input ---"
input_tasks=$(cat <<EOF
Organize the canned goods
Repair the temporal rift stabilizer
Scavenge for water filters
Fortify the shelter perimeter
Investigate the strange hum from sector 7
Recharge the solar lanterns
Clean the mutant-proof windows
EOF
)

# Run the main script with mocked get_random_comment
output=$(echo "$input_tasks" | src/doom_list_prioritizer.sh)

assert_contains "$output" "Doom Factor: 5 | Urgency: CRITICAL | Comment: The fabric of reality is fraying. This cannot wait. | Task: Repair the temporal rift stabilizer" "Output contains high doom task"
assert_contains "$output" "Doom Factor: 4 | Urgency: CRITICAL | Comment: The fabric of reality is fraying. This cannot wait. | Task: Investigate the strange hum from sector 7" "Output contains high doom task (investigate)"
assert_contains "$output" "Doom Factor: 3 | Urgency: HIGH     | Comment: Don't let the temporal distortions distract you. | Task: Fortify the shelter perimeter" "Output contains medium doom task (fortify)"
assert_contains "$output" "Doom Factor: 2 | Urgency: HIGH     | Comment: Don't let the temporal distortions distract you. | Task: Scavenge for water filters" "Output contains medium doom task (scavenge water)"
assert_contains "$output" "Doom Factor: 1 | Urgency: LOW      | Comment: Even in the apocalypse, some things can wait... probably. | Task: Organize the canned goods" "Output contains low doom task (organize)"
assert_contains "$output" "Doom Factor: 1 | Urgency: LOW      | Comment: Even in the apocalypse, some things can wait... probably. | Task: Recharge the solar lanterns" "Output contains low doom task (recharge)"
assert_contains "$output" "Doom Factor: 1 | Urgency: LOW      | Comment: Even in the apocalypse, some things can wait... probably. | Task: Clean the mutant-proof windows" "Output contains low doom task (clean)"

# Test 9: Ensure correct sorting (highest doom first)
first_line=$(echo "$output" | head -n 2 | tail -n 1) # Skip header
second_line=$(echo "$output" | head -n 3 | tail -n 1)
third_line=$(echo "$output" | head -n 4 | tail -n 1)

assert_contains "$first_line" "Doom Factor: 5" "First task is highest doom"
assert_contains "$second_line" "Doom Factor: 4" "Second task is next highest doom"
assert_contains "$third_line" "Doom Factor: 3" "Third task is next highest doom"


# Test 10: Empty input
echo "--- Test with empty input ---"
empty_output=$(echo "" | src/doom_list_prioritizer.sh)
assert_equal "--- Doom List Prioritization Report ---" "$empty_output" "Empty input produces only header"

# Test 11: Input file
echo "--- Test with input file ---"
temp_file="temp_tasks.txt"
cat <<EOF > "$temp_file"
Repair the temporal rift stabilizer
Organize the canned goods
EOF
file_output=$(src/doom_list_prioritizer.sh "$temp_file")
rm "$temp_file"

assert_contains "$file_output" "Doom Factor: 5 | Urgency: CRITICAL | Comment: The fabric of reality is fraying. This cannot wait. | Task: Repair the temporal rift stabilizer" "File input: high doom task"
assert_contains "$file_output" "Doom Factor: 1 | Urgency: LOW      | Comment: Even in the apocalypse, some things can wait... probably. | Task: Organize the canned goods" "File input: low doom task"
first_file_line=$(echo "$file_output" | head -n 2 | tail -n 1)
assert_contains "$first_file_line" "Doom Factor: 5" "File input: First task is highest doom"


echo "All tests passed!"
