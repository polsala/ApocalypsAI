#!/bin/bash

# Test setup
TEST_DIR=$(mktemp -d)
WAYPOINTS_FILE="$TEST_DIR/waypoints.txt"
SCRIPT_PATH="$(dirname "$0")/../src/chrono_compass.sh"

# Mock date command for deterministic testing
# Mock rationale: The 'date' command's output changes with system time, making tests non-deterministic.
#                 Mocking it allows us to control the current date for consistent deadline calculations.
mock_date() {
    local args=($@)
    local format_arg=""
    local date_str=""

    for ((i=0; i<${#args[@]}; i++)); do
        case "${args[i]}" in
            -d)
                if ((i+1 < ${#args[@]})); then
                    date_str="${args[i+1]}"
                    i=$((i+1)) # Skip next arg
                fi
                ;;
            +*)
                format_arg="${args[i]}"
                ;;
        esac
    done

    if [[ "$format_arg" == "+%s" ]]; then
        if [[ -z "$date_str" ]]; then
            # This is for `date +%s`
            echo "1698436800" # 2023-10-27 12:00:00 UTC
        else
            # This is for `date -d "$date_str" +%s`
            case "$date_str" in
                "2023-10-27") echo "1698436800" ;;
                "2023-10-28") echo "1698523200" ;;
                "2023-10-29") echo "1698609600" ;;
                "2023-10-31") echo "1698782400" ;;
                "2023-11-04") echo "1699128000" ;;
                "2023-10-26") echo "1698350400" ;;
                "2023-10-20") echo "1697832000" ;;
                *) echo "Error: Unknown mock date for '$date_str'" >&2; return 1 ;;
            esac
        fi
    else
        # Fallback for other date commands if needed, though not expected in this script
        # For simplicity, if not +%s, just return an empty string or error
        echo "Error: Unhandled date command: $@" >&2
        return 1
    fi
}

# Override the date command for the test script
export -f date
date() { mock_date "$@"; }

# Helper function for assertions
assert_contains() {
    local expected="$1"
    local actual="$2"
    if echo "$actual" | grep -qF "$expected"; then
        echo "PASS: Output contains '$expected'"
    else
        echo "FAIL: Output does NOT contain '$expected'"
        echo "--- Actual Output ---"
        echo "$actual"
        echo "---------------------"
        exit 1
    fi
}

assert_not_contains() {
    local expected="$1"
    local actual="$2"
    if echo "$actual" | grep -qF "$expected"; then
        echo "FAIL: Output unexpectedly contains '$expected'"
        echo "--- Actual Output ---"
        echo "$actual"
        echo "---------------------"
        exit 1
    else
        echo "PASS: Output does NOT contain '$expected'"
    fi
}

# Test 1: Basic scan with no waypoints and no recent files
echo "--- Running Test 1: Basic scan, no waypoints, no recent files ---"
mkdir "$TEST_DIR/project_a"
OUTPUT=$(bash "$SCRIPT_PATH" "$TEST_DIR/project_a")
assert_contains "No recent disturbances detected." "$OUTPUT"
assert_contains "No waypoint file specified." "$OUTPUT"
rm -rf "$TEST_DIR/project_a"
echo ""

# Test 2: Scan with recent files (lookback 1 day)
echo "--- Running Test 2: Scan with recent files (lookback 1 day) ---"
mkdir "$TEST_DIR/project_b"
touch -d "2023-10-27 10:00:00" "$TEST_DIR/project_b/file_today.txt" # Modified today
touch -d "2023-10-26 15:00:00" "$TEST_DIR/project_b/file_yesterday.txt" # Modified yesterday
touch -d "2023-10-20 08:00:00" "$TEST_DIR/project_b/file_old.txt" # Modified a week ago

OUTPUT=$(bash "$SCRIPT_PATH" --lookback 1 "$TEST_DIR/project_b") # Lookback 1 day
assert_contains "file_today.txt" "$OUTPUT"
assert_not_contains "file_yesterday.txt" "$OUTPUT" # Should not be included with lookback 1
assert_not_contains "file_old.txt" "$OUTPUT"
rm -rf "$TEST_DIR/project_b"
echo ""

# Test 3: Scan with recent files and longer lookback (2 days)
echo "--- Running Test 3: Scan with recent files and longer lookback (2 days) ---"
mkdir "$TEST_DIR/project_c"
touch -d "2023-10-27 10:00:00" "$TEST_DIR/project_c/file_today.txt"
touch -d "2023-10-26 15:00:00" "$TEST_DIR/project_c/file_yesterday.txt"
touch -d "2023-10-20 08:00:00" "$TEST_DIR/project_c/file_old.txt"

OUTPUT=$(bash "$SCRIPT_PATH" --lookback 2 "$TEST_DIR/project_c") # Lookback 2 days
assert_contains "file_today.txt" "$OUTPUT"
assert_contains "file_yesterday.txt" "$OUTPUT"
assert_not_contains "file_old.txt" "$OUTPUT"
rm -rf "$TEST_DIR/project_c"
echo ""

# Test 4: Scan with waypoints file - upcoming and past deadlines
echo "--- Running Test 4: Scan with waypoints file - upcoming and past deadlines ---"
mkdir "$TEST_DIR/project_d"
cat <<EOF > "$WAYPOINTS_FILE"
Task A|2023-10-27
Task B|2023-10-28
Task C|2023-10-29
Task D|2023-10-20
Task E|2023-11-04
Invalid Date|2023/10/30
EOF

OUTPUT=$(bash "$SCRIPT_PATH" --waypoints "$WAYPOINTS_FILE" "$TEST_DIR/project_d")
assert_contains "[TODAY!] Task A (Deadline: 2023-10-27)" "$OUTPUT"
assert_contains "[URGENT - 1 day left] Task B (Deadline: 2023-10-28)" "$OUTPUT"
assert_contains "[2 days left] Task C (Deadline: 2023-10-29)" "$OUTPUT"
assert_contains "Task E (Deadline: 2023-11-04)" "$OUTPUT" # More than 7 days
assert_not_contains "Task D" "$OUTPUT" # Past deadline
assert_contains "Warning: Invalid date format for task 'Invalid Date'. Expected YYYY-MM-DD." "$OUTPUT" # Error message for invalid date
rm -rf "$TEST_DIR/project_d"
echo ""

# Test 5: Waypoints file not found
echo "--- Running Test 5: Waypoints file not found ---"
mkdir "$TEST_DIR/project_e"
OUTPUT=$(bash "$SCRIPT_PATH" --waypoints "non_existent_file.txt" "$TEST_DIR/project_e")
assert_contains "Waypoint file 'non_existent_file.txt' not found." "$OUTPUT"
rm -rf "$TEST_DIR/project_e"
echo ""

# Test 6: No upcoming waypoints
echo "--- Running Test 6: No upcoming waypoints ---"
mkdir "$TEST_DIR/project_f"
cat <<EOF > "$WAYPOINTS_FILE"
Past Task|2023-10-20
Another Past Task|2023-10-25
EOF
OUTPUT=$(bash "$SCRIPT_PATH" --waypoints "$WAYPOINTS_FILE" "$TEST_DIR/project_f")
assert_contains "No upcoming waypoints on the temporal map." "$OUTPUT"
rm -rf "$TEST_DIR/project_f"
echo ""

# Test 7: Empty waypoints file
echo "--- Running Test 7: Empty waypoints file ---"
mkdir "$TEST_DIR/project_g"
touch "$WAYPOINTS_FILE"
OUTPUT=$(bash "$SCRIPT_PATH" --waypoints "$WAYPOINTS_FILE" "$TEST_DIR/project_g")
assert_contains "No upcoming waypoints on the temporal map." "$OUTPUT"
rm -rf "$TEST_DIR/project_g"
echo ""

# Test 8: Invalid directory
echo "--- Running Test 8: Invalid directory ---"
OUTPUT=$(bash "$SCRIPT_PATH" "non_existent_dir" 2>&1)
assert_contains "Error: Target directory 'non_existent_dir' does not exist." "$OUTPUT"
echo ""

# Test 9: No directory provided
echo "--- Running Test 9: No directory provided ---"
OUTPUT=$(bash "$SCRIPT_PATH" 2>&1)
assert_contains "Error: No target directory specified." "$OUTPUT"
assert_contains "Usage: $0 [OPTIONS] <directory>" "$OUTPUT"
echo ""

# Cleanup
rm -rf "$TEST_DIR"
unset -f date # Unset the mock date function
echo "All tests passed!"
