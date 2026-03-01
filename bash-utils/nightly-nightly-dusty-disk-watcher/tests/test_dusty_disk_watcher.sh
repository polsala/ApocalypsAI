#!/usr/bin/env bash
# test_dusty_disk_watcher.sh - Simple tests for dusty_disk_watcher.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT_PATH="${SCRIPT_DIR}/src/dusty_disk_watcher.sh"

# Helper for assertions
assert_contains() {
    local output="$1"
    local expected="$2"
    if [[ "$output" != *"$expected"* ]]; then
        echo "Assertion failed: expected to find '$expected' in output"
        echo "Output was: $output"
        exit 1
    fi
}

# Test 1: High usage triggers warning
export DF_OUTPUT=$'Filesystem      Size  Used Avail Use% Mounted on\n/dev/root        20G   17G   3G  85% /'
output=$("$SCRIPT_PATH" 80)
assert_contains "$output" "Warning! Disk usage at 85%"

# Test 2: Low usage shows all clear
export DF_OUTPUT=$'Filesystem      Size  Used Avail Use% Mounted on\n/dev/root        20G   9G   11G  45% /'
output=$("$SCRIPT_PATH" 80)
assert_contains "$output" "All clear. Disk usage at 45%"

echo "All tests passed."
