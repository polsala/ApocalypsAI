#!/usr/bin/env bash

# Tests for nightly-disk-guardian

set -euo pipefail

SCRIPT="../src/main.sh"

# Test case 1: usage below threshold – expect calm message
export MOCK_DF=$'Filesystem      Size  Used Avail Use% Mounted on\n/dev/root        20G   10G   10G  50% /'
output=$($SCRIPT 80)
expected="✅ All is calm. Disk usage at 50% ."
if [[ "$output" != "$expected" ]]; then
    echo "FAIL: low usage – expected '$expected' but got '$output'"
    exit 1
fi

# Test case 2: usage above threshold – expect a warning containing the usage percent
export MOCK_DF=$'Filesystem      Size  Used Avail Use% Mounted on\n/dev/root        20G   18G   2G  90% /'
# Force deterministic random choice
RANDOM=0
output=$($SCRIPT 80)
if [[ "$output" != *"90%"* ]]; then
    echo "FAIL: high usage – expected warning containing '90%' but got '$output'"
    exit 1
fi

echo "All tests passed."
