#!/bin/bash

# ApocalypsAI - Nightly System Health Check Tests

# Source the script to be tested
# Mock rationale: Sourcing the script allows us to call its functions and variables.
# In a real test environment, we might use a temporary file or a more robust testing framework.
. src/main.sh

# --- Mocking Functions ---

# Mock for df command
df() {
    echo "Filesystem     1K-blocks     Used Available Use% Mounted on"
    echo "/dev/sda1      10000000   9000000   1000000  90% /"
}

# Mock for free command
free() {
    echo "              total        used        free     shared    buffers     cached"
    echo "Mem:        1000000      900000      100000      10000      10000      90000"
    echo "Swap:        500000      100000      400000"
}

# Mock for ps command
ps() {
    echo "USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND"
    echo "root           1  0.0  0.1 123456 7890 ?        Ss   Jan01   0:01 /sbin/init"
    # Add more lines to simulate a higher process count if needed for testing
    for i in $(seq 2 1001); do
        echo "user$i       $i  0.0  0.0 12345  6789 pts/0    R+   10:00   0:00 bash"
    done
}

# --- Test Cases ---

run_test() {
    local test_name="$1"
    local expected_output="$2"
    local actual_output="$(eval "$3" | grep -v "^\s*$" | tail -n +3 | head -n -2)" # Extract relevant lines, excluding header and footer

    echo "Running test: $test_name"
    if [[ "$actual_output" == *"$expected_output"* ]]; then
        echo "  ✅ PASSED"
    else
        echo "  ❌ FAILED"
        echo "    Expected: $expected_output"
        echo "    Actual:   $actual_output"
        return 1
    fi
    return 0
}

# Test 1: High Disk Usage
run_test "High Disk Usage" "Disk space is critically low!" "./src/main.sh"
if [ $? -ne 0 ]; then exit 1; fi

# Test 2: Normal Memory Usage (adjusting mock for this test)
free() {
    echo "              total        used        free     shared    buffers     cached"
    echo "Mem:        1000000      500000      500000      10000      10000      90000"
    echo "Swap:        500000      100000      400000"
}
run_test "Normal Memory Usage" "Memory usage is within acceptable limits."
if [ $? -ne 0 ]; then exit 1; fi

# Test 3: High Memory Usage (adjusting mock for this test)
free() {
    echo "              total        used        free     shared    buffers     cached"
    echo "Mem:        1000000      950000       50000      10000      10000      90000"
    echo "Swap:        500000      100000      400000"
}
run_test "High Memory Usage" "Memory is almost full!"
if [ $? -ne 0 ]; then exit 1; fi

# Test 4: High Process Count
run_test "High Process Count" "An alarming number of processes are running"
if [ $? -ne 0 ]; then exit 1; fi

# Test 5: Commands not found (simulating missing utilities)
original_df=$df
original_free=$free
original_ps=$ps

df() { echo "command not found: df"; return 127; }
free() { echo "command not found: free"; return 127; }
ps() { echo "command not found: ps"; return 127; }

run_test "Missing Commands" "Could not check disk space."
if [ $? -ne 0 ]; then exit 1; fi

# Restore original functions
df=$original_df
free=$original_free
ps=$original_ps

echo "\nAll tests passed! The system is as stable as a pre-apocalypse server room."
exit 0
