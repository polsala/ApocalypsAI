#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)
NOTIFIER="$SCRIPT_DIR/moon_notifier.sh"

run_and_check() {
  local date=$1
  local expected=$2
  output=$(MOON_DATE="$date" "$NOTIFIER")
  if [[ "$output" != *"$expected"* ]]; then
    echo "FAIL: For date $date expected '$expected' in output."
    echo "Output was:"
    echo "$output"
    exit 1
  else
    echo "PASS: $date -> $expected"
  fi
}

# Known full moon: 2023-09-29
run_and_check "2023-09-29" "Full Moon"

# Known last quarter: 2023-09-21
run_and_check "2023-09-21" "Last Quarter"

echo "All tests passed."
