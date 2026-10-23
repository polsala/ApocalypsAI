#!/usr/bin/env bash
set -euo pipefail

# Load the script without executing its main function
source ./src/disk_guardian.sh

# ---------- Test: usage below threshold ----------
get_root_usage() { echo 50; }
random_message() { echo "All is well!"; }

output=$(main 80)
expected="✅ Disk usage at 50% – All is calm."
if [[ "$output" == "$expected" ]]; then
    echo "PASS: below threshold"
else
    echo "FAIL: below threshold"
    echo "Got: $output"
    exit 1
fi

# ---------- Test: usage above threshold ----------
get_root_usage() { echo 90; }
random_message() { echo "The world is ending!"; }

output=$(main 80)
expected=$'⚠️  Disk usage at 90% – The world is ending!\n   ____\n  /____\\   *BOOM*'
if [[ "$output" == "$expected" ]]; then
    echo "PASS: above threshold"
else
    echo "FAIL: above threshold"
    echo "Got: $output"
    exit 1
fi
