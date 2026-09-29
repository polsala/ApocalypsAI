#!/bin/bash

# Path to the script being tested
SCRIPT_PATH="./src/cosmic-vitality-check.sh"

# --- Mocking functions ---
# Mock rationale: We need to control the output of system commands like `top`, `free`, and `df`
# to simulate different system resource states (e.g., high CPU, low memory, full disk)
# without actually affecting the host system or relying on its current state.
# This allows for deterministic and isolated testing.

# Create a temporary directory for mocks
MOCK_BIN_DIR=$(mktemp -d)
export PATH="$MOCK_BIN_DIR:$PATH" # Prepend mock directory to PATH

# Mock `top` command
cat << 'EOF' > "$MOCK_BIN_DIR/top"
#!/bin/bash
if [[ "$1" == "-bn1" ]]; then
    echo "top - 12:00:00 up 1 day, 0 users, load average: 0.00, 0.00, 0.00"
    echo "Tasks:   1 total,   0 running,   1 sleeping,   0 stopped,   0 zombie"
    echo "%Cpu(s): 0.0 us, 0.0 sy, 0.0 ni, ${MOCK_CPU_IDLE:-99.0} id, 0.0 wa, 0.0 hi, 0.0 si, 0.0 st"
    echo "MiB Mem :   1000.0 total,    900.0 free,    100.0 used,      0.0 buff/cache"
    echo "MiB Swap:   1000.0 total,   1000.0 free,      0.0 used.    900.0 avail Mem"
fi
EOF
chmod +x "$MOCK_BIN_DIR/top"

# Mock `free` command
cat << 'EOF' > "$MOCK_BIN_DIR/free"
#!/bin/bash
if [[ "$1" == "-m" ]]; then
    echo "              total        used        free      shared  buff/cache   available"
    echo "Mem:       ${MOCK_MEM_TOTAL:-1000}    ${MOCK_MEM_USED:-100}     ${MOCK_MEM_FREE:-900}         0         0         0"
    echo "Swap:        1000          0        1000"
fi
EOF
chmod +x "$MOCK_BIN_DIR/free"

# Mock `df` command
cat << 'EOF' > "$MOCK_BIN_DIR/df"
#!/bin/bash
if [[ "$1" == "-h" && "$2" == "/" ]]; then
    echo "Filesystem      Size  Used Avail Use% Mounted on"
    echo "/dev/sda1        100G ${MOCK_DISK_USED:-10G} ${MOCK_DISK_AVAIL:-90G} ${MOCK_DISK_PERCENT:-10}% /"
fi
EOF
chmod +x "$MOCK_BIN_DIR/df"

# --- Test functions ---

run_test() {
    local test_name="$1"
    local expected_output_regex="$2"
    local expected_exit_code="$3"
    local cpu_idle="$4"
    local mem_total="$5"
    local mem_used="$6"
    local disk_used="$7"
    local disk_avail="$8"
    local disk_percent="$9"

    echo "--- Running Test: $test_name ---"

    # Set mock environment variables
    export MOCK_CPU_IDLE="${cpu_idle}"
    export MOCK_MEM_TOTAL="${mem_total}"
    export MOCK_MEM_USED="${mem_used}"
    export MOCK_MEM_FREE=$(echo "$mem_total - $mem_used" | bc) # Calculate free mem for mock
    export MOCK_DISK_USED="${disk_used}"
    export MOCK_DISK_AVAIL="${disk_avail}"
    export MOCK_DISK_PERCENT="${disk_percent}"

    # Run the script and capture output and exit code
    output=$(bash "$SCRIPT_PATH" 2>&1)
    exit_code=$?

    # Assertions
    if echo "$output" | grep -Eq "$expected_output_regex"; then
        echo "PASS: Output matches expected regex."
    else
        echo "FAIL: Output does NOT match expected regex."
        echo "Expected regex: $expected_output_regex"
        echo "Actual output:"
        echo "$output"
        return 1
    fi

    if [ "$exit_code" -eq "$expected_exit_code" ]; then
        echo "PASS: Exit code is $exit_code."
    else
        echo "FAIL: Exit code is $exit_code, expected $expected_exit_code."
        return 1
    fi

    echo ""
    return 0
}

# --- Test Cases ---
all_tests_passed=0

# Test 1: All resources healthy
run_test "Healthy System" "Cosmic Vitality Status: OPTIMAL" 0 \
    "90.0" "1000" "100" "10G" "90G" "10" || all_tests_passed=1

# Test 2: High CPU usage
run_test "High CPU" "CPU Cores are humming a bit too intensely!" 1 \
    "10.0" "1000" "100" "10G" "90G" "10" || all_tests_passed=1

# Test 3: High Memory usage
run_test "High Memory" "Memory Streams are overflowing!" 1 \
    "90.0" "1000" "900" "10G" "90G" "10" || all_tests_passed=1

# Test 4: High Disk usage
run_test "High Disk" "Aetheric Storage is nearing capacity!" 1 \
    "90.0" "1000" "100" "95G" "5G" "95" || all_tests_passed=1

# Test 5: Moderate CPU (ATTENTIVE)
run_test "Moderate CPU" "CPU Cores are resonating strongly." 0 \
    "60.0" "1000" "100" "10G" "90G" "10" || all_tests_passed=1

# Test 6: Moderate Memory (ATTENTIVE)
run_test "Moderate Memory" "Memory Streams are flowing briskly." 0 \
    "90.0" "1000" "500" "10G" "90G" "10" || all_tests_passed=1

# Test 7: Moderate Disk (ATTENTIVE)
run_test "Moderate Disk" "Aetheric Storage is comfortably full." 0 \
    "90.0" "1000" "100" "60G" "40G" "60" || all_tests_passed=1

# Test 8: Combination of issues (should be CRITICAL)
run_test "Combined Critical Issues" "CPU Cores are humming a bit too intensely!.*Memory Streams are overflowing!" 1 \
    "10.0" "1000" "900" "10G" "90G" "10" || all_tests_passed=1

# Test 9: All moderate (should be ATTENTIVE)
run_test "All Moderate Issues" "Cosmic Vitality Status: ATTENTIVE" 0 \
    "60.0" "1000" "500" "60G" "40G" "60" || all_tests_passed=1

# Clean up mock directory
rm -rf "$MOCK_BIN_DIR"

if [ "$all_tests_passed" -eq 0 ]; then
    echo "All tests passed successfully!"
    exit 0
else
    echo "Some tests failed."
    exit 1
fi
