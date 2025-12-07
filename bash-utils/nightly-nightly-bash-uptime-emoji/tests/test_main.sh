#!/usr/bin/env bash
# Tests for nightly-bash-uptime-emoji
# These tests are deterministic and do not rely on the actual system uptime.

set -euo pipefail

SCRIPT_PATH="../src/main.sh"

run_test() {
    local input="$1"
    local expected_emoji="$2"
    local output
    output=$($SCRIPT_PATH "$input")
    if [[ "$output" != *"$expected_emoji"* ]]; then
        echo "FAIL: Input '$input' – expected emoji '$expected_emoji' but got: $output"
        exit 1
    else
        echo "PASS: Input '$input' produced expected emoji '$expected_emoji'"
    fi
}

# Mocked uptime strings and their expected emojis
run_test "up 2 hours, 15 minutes" "🌅"
run_test "up 8 hours, 0 minutes" "☀️"
run_test "up 14 hours, 30 minutes" "🌇"
run_test "up 20 hours, 5 minutes" "🌙"

echo "All tests passed."
