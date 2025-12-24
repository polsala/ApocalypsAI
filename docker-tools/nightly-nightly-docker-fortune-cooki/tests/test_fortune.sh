#!/usr/bin/env bash

set -e

# Resolve the directory of this test script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}") && pwd)"

# Run the fortune script with a fixed index (0) to get a deterministic output
output=$(bash "$SCRIPT_DIR/../src/fortune.sh" 0)

expected="You will find unexpected treasure today."

if [[ "$output" == "$expected" ]]; then
    echo "PASS"
    exit 0
else
    echo "FAIL: expected '$expected' but got '$output'"
    exit 1
fi
