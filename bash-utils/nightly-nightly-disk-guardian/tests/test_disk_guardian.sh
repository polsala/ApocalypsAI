#!/usr/bin/env bash
set -euo pipefail

# Path to the utility script
SCRIPT_PATH="../src/disk-guardian.sh"

# Helper to run the script with a mocked df output and verify expectations
run_test() {
    local mock_df="$1"
    local expected_exit="$2"
    local expected_substr="$3"

    export MOCK_DF="$mock_df"
    output=$($SCRIPT_PATH 2>&1) || true
    exit_code=$?
    unset MOCK_DF

    if [[ $exit_code -ne $expected_exit ]]; then
        echo "FAIL: Expected exit $expected_exit, got $exit_code"
        echo "Output: $output"
        exit 1
    fi
    if [[ -n "$expected_substr" && "$output" != *"$expected_substr"* ]]; then
        echo "FAIL: Expected output to contain '$expected_substr'"
        echo "Output: $output"
        exit 1
    fi
    echo "PASS"
}

# Test 1: Low usage (30%) – should be safe
run_test "Filesystem Size Used Avail Use% Mounted on\n/dev/root 20G 6G 14G 30% /" 0 "✅ Disk usage is safe"

# Test 2: High usage (85%) – should trigger warning
run_test "Filesystem Size Used Avail Use% Mounted on\n/dev/root 20G 17G 3G 85% /" 2 "used!"

echo "All tests passed."
