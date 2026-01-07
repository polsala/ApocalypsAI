#!/usr/bin/env bash
set -e

SCRIPT="../src/emoji_clock.sh"

# Test case 1: 13:00 should yield 🕐 13:00
TIME_OVERRIDE=13:00 bash "$SCRIPT" > output1
if [[ "$(cat output1)" != "🕐 13:00" ]]; then
  echo "FAIL: Expected 🕐 13:00, got $(cat output1)"
  exit 1
fi

# Test case 2: 00:15 should yield 🕛 00:15
TIME_OVERRIDE=00:15 bash "$SCRIPT" > output2
if [[ "$(cat output2)" != "🕛 00:15" ]]; then
  echo "FAIL: Expected 🕛 00:15, got $(cat output2)"
  exit 1
fi

echo "All tests passed."
