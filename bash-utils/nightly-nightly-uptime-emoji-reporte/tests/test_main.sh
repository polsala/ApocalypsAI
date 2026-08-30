#!/usr/bin/env bash
set -euo pipefail

SCRIPT="../src/main.sh"

# Test case 1: mock 10 hours (36000 seconds)
output=$(UPTIME_MOCK=36000 "$SCRIPT")
expected="🌱 System uptime: 10h – Fresh and ready!"
if [[ "$output" != "$expected" ]]; then
  echo "FAIL: Expected '$expected' got '$output'"
  exit 1
fi

# Test case 2: mock 48 hours (172800 seconds)
output=$(UPTIME_MOCK=172800 "$SCRIPT")
expected="🌤 System uptime: 48h – Running smoothly."
if [[ "$output" != "$expected" ]]; then
  echo "FAIL: Expected '$expected' got '$output'"
  exit 1
fi

# Test case 3: mock 100 hours (360000 seconds)
output=$(UPTIME_MOCK=360000 "$SCRIPT")
expected="🔥 System uptime: 100h – Time to consider a reboot."
if [[ "$output" != "$expected" ]]; then
  echo "FAIL: Expected '$expected' got '$output'"
  exit 1
fi

echo "All tests passed."
