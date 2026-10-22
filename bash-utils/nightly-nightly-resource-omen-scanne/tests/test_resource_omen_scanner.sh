#!/bin/bash

# Source the script to test its functions
# This allows us to override functions defined in resource_omen_scanner.sh
. src/resource_omen_scanner.sh

# --- Mocking System Commands ---
# Mock rationale: These functions replace actual system commands (top, free, df)
# to provide deterministic output for testing purposes, avoiding reliance on
# the host system's real-time resource usage.

MOCK_CPU_IDLE="90" # Default idle, meaning 10% used
MOCK_MEM_TOTAL="1024" # 1GB
MOCK_MEM_USED="100" # 100MB used
MOCK_DISK_USED="50" # 50% used

# Override get_cpu_idle function
get_cpu_idle() {
    echo "$MOCK_CPU_IDLE"
}

# Override get_mem_used function
get_mem_used() {
    local total_mem="$MOCK_MEM_TOTAL"
    local used_mem="$MOCK_MEM_USED"
    if [[ "$total_mem" -gt 0 ]]; then
        echo $(( (used_mem * 100) / total_mem ))
    else
        echo "0"
    fi
}

# Override get_disk_used function
get_disk_used() {
    echo "$MOCK_DISK_USED"
}

# Override pick_omen function to make it deterministic
# Mock rationale: This ensures that the omen messages are predictable for testing,
# rather than relying on the randomness of $RANDOM.
pick_omen() {
    local -n omens_array="$1"
    echo "${omens_array[0]}" # Always pick the first omen for deterministic tests
}

# --- Test Helper Functions ---
assert_contains() {
    local expected_substring="$1"
    local actual_string="$2"
    local test_name="$3"
    if echo "$actual_string" | grep -q "$expected_substring"; then
        echo "✅ PASS: $test_name"
    else
        echo "❌ FAIL: $test_name"
        echo "  Expected to contain: '$expected_substring'"
        echo "  Actual output: '$actual_string'"
        exit 1
    fi
}

assert_not_contains() {
    local unexpected_substring="$1"
    local actual_string="$2"
    local test_name="$3"
    if ! echo "$actual_string" | grep -q "$unexpected_substring"; then
        echo "✅ PASS: $test_name"
    else
        echo "❌ FAIL: $test_name"
        echo "  Expected NOT to contain: '$unexpected_substring'"
        echo "  Actual output: '$actual_string'"
        exit 1
    fi
}

# --- Test Cases ---

echo "Running tests for nightly-resource-omen-scanner..."

# Test 1: No omens triggered (all resources below default thresholds)
test_no_omens() {
    MOCK_CPU_IDLE="95" # 5% used
    MOCK_MEM_USED="50" # ~5% used
    MOCK_DISK_USED="20" # 20% used
    local output=$(main 80 80 90 /dev/null 2>&1) # Pass dummy log file to avoid actual file ops
    assert_contains "All systems nominal. The void slumbers... for now." "$output" "No omens triggered"
    assert_not_contains "CPU OMEN" "$output" "No CPU omen when below threshold"
    assert_not_contains "MEMORY OMEN" "$output" "No MEMORY omen when below threshold"
    assert_not_contains "DISK OMEN" "$output" "No DISK omen when below threshold"
    if main 80 80 90 /dev/null > /dev/null; then
        echo "✅ PASS: No omens triggered (exit code 0)"
    else
        echo "❌ FAIL: No omens triggered (exit code not 0)"
        exit 1
    fi
}
test_no_omens

# Test 2: CPU omen triggered
test_cpu_omen() {
    MOCK_CPU_IDLE="10" # 90% used
    MOCK_MEM_USED="50" # ~5% used
    MOCK_DISK_USED="20" # 20% used
    local output=$(main 80 80 90 /dev/null 2>&1)
    assert_contains "CPU OMEN: The CPU core hums with an unnatural fervor, a sign of impending digital maelstrom!" "$output" "CPU omen triggered"
    assert_not_contains "MEMORY OMEN" "$output" "No MEMORY omen when CPU triggered"
    assert_not_contains "DISK OMEN" "$output" "No DISK omen when CPU triggered"
    if main 80 80 90 /dev/null > /dev/null; then
        echo "❌ FAIL: CPU omen triggered (exit code 0, expected 1)"
        exit 1
    else
        echo "✅ PASS: CPU omen triggered (exit code 1)"
    fi
}
test_cpu_omen

# Test 3: Memory omen triggered
test_mem_omen() {
    MOCK_CPU_IDLE="95" # 5% used
    MOCK_MEM_USED="900" # ~87% used
    MOCK_DISK_USED="20" # 20% used
    local output=$(main 80 80 90 /dev/null 2>&1)
    assert_contains "MEMORY OMEN: Memory's grasp loosens, and whispers of the void consume precious bytes." "$output" "Memory omen triggered"
    assert_not_contains "CPU OMEN" "$output" "No CPU omen when MEM triggered"
    assert_not_contains "DISK OMEN" "$output" "No DISK omen when MEM triggered"
    if main 80 80 90 /dev/null > /dev/null; then
        echo "❌ FAIL: Memory omen triggered (exit code 0, expected 1)"
        exit 1
    else
        echo "✅ PASS: Memory omen triggered (exit code 1)"
    fi
}
test_mem_omen

# Test 4: Disk omen triggered
test_disk_omen() {
    MOCK_CPU_IDLE="95" # 5% used
    MOCK_MEM_USED="50" # ~5% used
    MOCK_DISK_USED="95" # 95% used
    local output=$(main 80 80 90 /dev/null 2>&1)
    assert_contains "DISK OMEN: The digital earth groans, its storage capacity nearing a critical mass." "$output" "Disk omen triggered"
    assert_not_contains "CPU OMEN" "$output" "No CPU omen when DISK triggered"
    assert_not_contains "MEMORY OMEN" "$output" "No DISK omen when DISK triggered"
    if main 80 80 90 /dev/null > /dev/null; then
        echo "❌ FAIL: Disk omen triggered (exit code 0, expected 1)"
        exit 1
    else
        echo "✅ PASS: Disk omen triggered (exit code 1)"
    fi
}
test_disk_omen

# Test 5: Multiple omens triggered
test_multiple_omens() {
    MOCK_CPU_IDLE="10" # 90% used
    MOCK_MEM_USED="900" # ~87% used
    MOCK_DISK_USED="95" # 95% used
    local output=$(main 80 80 90 /dev/null 2>&1)
    assert_contains "CPU OMEN" "$output" "Multiple omens: CPU"
    assert_contains "MEMORY OMEN" "$output" "Multiple omens: MEMORY"
    assert_contains "DISK OMEN" "$output" "Multiple omens: DISK"
    if main 80 80 90 /dev/null > /dev/null; then
        echo "❌ FAIL: Multiple omens triggered (exit code 0, expected 1)"
        exit 1
    else
        echo "✅ PASS: Multiple omens triggered (exit code 1)"
    fi
}
test_multiple_omens

# Test 6: Custom thresholds
test_custom_thresholds() {
    MOCK_CPU_IDLE="70" # 30% used
    MOCK_MEM_USED="300" # ~29% used
    MOCK_DISK_USED="40" # 40% used
    local output=$(main 20 20 30 /dev/null 2>&1) # Set low thresholds
    assert_contains "CPU OMEN" "$output" "Custom thresholds: CPU"
    assert_contains "MEMORY OMEN" "$output" "Custom thresholds: MEMORY"
    assert_contains "DISK OMEN" "$output" "Custom thresholds: DISK"
    if main 20 20 30 /dev/null > /dev/null; then
        echo "❌ FAIL: Custom thresholds triggered (exit code 0, expected 1)"
        exit 1
    else
        echo "✅ PASS: Custom thresholds triggered (exit code 1)"
    fi
}
test_custom_thresholds

# Test 7: Logging to a file
test_logging() {
    local log_file="test_omen_log.txt"
    rm -f "$log_file" # Clean up previous log
    MOCK_CPU_IDLE="10" # 90% used
    MOCK_MEM_USED="50" # ~5% used
    MOCK_DISK_USED="20" # 20% used
    main 80 80 90 "$DEFAULT_DISK_PATH" "$log_file" > /dev/null
    assert_contains "CPU OMEN" "$(cat "$log_file")" "Logging: CPU omen in log file"
    assert_contains "Report logged to $log_file" "$(main 80 80 90 "$DEFAULT_DISK_PATH" "$log_file")" "Logging: confirmation message"
    rm -f "$log_file" # Clean up
}
test_logging

echo "All tests completed."
