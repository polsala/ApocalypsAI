#!/usr/bin/env bash
# Tests for nightly-uptime-emoji-report

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
UTIME="$SCRIPT_DIR/uptime-emoji.sh"

run_test() {
    local seconds=$1
    local expected_emoji=$2
    local output
    output=$("$UTIME" "$seconds")
    if [[ "$output" != *"$expected_emoji"* ]]; then
        echo "FAIL: seconds=$seconds expected emoji $expected_emoji got '$output'"
        exit 1
    else
        echo "PASS: seconds=$seconds -> $expected_emoji"
    fi
}

run_test 0 "🐣"
run_test 3599 "🐣"
run_test 3600 "🌞"
run_test 21599 "🌞"
run_test 21600 "🌤"
run_test 86399 "🌤"
run_test 86400 "🌥"
run_test 259199 "🌥"
run_test 259200 "🌙"

echo "All tests passed."
