#!/usr/bin/env bash
set -euo pipefail

# Helper to run the guardian with a mocked df output
run_guardian() {
    local mock_output="$1"
    local threshold="${2:-80}"
    # Define a mock df function that prints the supplied output
    df() {
        echo "$mock_output"
    }
    export -f df
    # Capture the script output
    output=$(bash ../src/disk_guardian.sh "$threshold")
    echo "$output"
}

# Test when usage is above the threshold – expect one of the warning emojis
test_above_threshold() {
    local mock="Filesystem Size Used Avail Use% Mounted on
/dev/root 100G 85G 15G 85% /"
    output=$(run_guardian "$mock" 80)
    if [[ "$output" == ⚠️* || "$output" == 🔥* || "$output" == ☢️* || "$output" == 🌪️* || "$output" == 🧟* ]]; then
        echo "PASS: above threshold warning"
    else
        echo "FAIL: expected warning, got '$output'"
        exit 1
    fi
}

# Test when usage is below the threshold – expect the clear message
test_below_threshold() {
    local mock="Filesystem Size Used Avail Use% Mounted on
/dev/root 100G 30G 70G 30% /"
    output=$(run_guardian "$mock" 80)
    if [[ "$output" == "✅ All clear: disk usage is 30%" ]]; then
        echo "PASS: below threshold clear"
    else
        echo "FAIL: expected clear message, got '$output'"
        exit 1
    fi
}

# Execute tests
test_above_threshold
test_below_threshold
