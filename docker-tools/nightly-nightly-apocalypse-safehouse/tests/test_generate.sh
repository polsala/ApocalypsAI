#!/usr/bin/env bash

# nightly‑apocalypse‑safehouse‑generator test suite
# This test runs the generator with a known seed and checks that the
# number of "Room" entries matches the requested count.

set -e

# Ensure script is executable
chmod +x src/generate.sh

# Run generator with deterministic seed
output=$(src/generate.sh --rooms 3 --seed 42)

# Count occurrences of "Room"
room_count=$(echo "$output" | grep -c "Room")

if [[ $room_count -ne 3 ]]; then
  echo "FAIL: Expected 3 rooms, got $room_count"
  echo "$output"
  exit 1
fi

# Simple sanity check: ensure top border starts with '+'
if [[ $(echo "$output" | head -n1) != "+"* ]]; then
  echo "FAIL: Output does not start with top border"
  exit 1
fi

echo "PASS"
