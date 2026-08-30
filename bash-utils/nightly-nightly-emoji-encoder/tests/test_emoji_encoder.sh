#!/usr/bin/env bash
set -e

# Helper to compare expected vs actual
assert_equal() {
  local expected="$1"
  local actual="$2"
  local test_name="$3"
  if [[ "$expected" != "$actual" ]]; then
    echo "[FAIL] $test_name"
    echo "  Expected: $expected"
    echo "  Got     : $actual"
    exit 1
  else
    echo "[PASS] $test_name"
  fi
}

# Test 1: Argument input
output=$(../src/emoji_encoder.sh "ab cz")
expected="🍎🐝 🌟🦓"
assert_equal "$expected" "$output" "Argument input encoding"

# Test 2: Stdin input
output=$(echo "hello" | ../src/emoji_encoder.sh)
expected="🍯🍋🍋🍊🍏"
assert_equal "$expected" "$output" "Stdin input encoding"

# Test 3: Mixed characters (numbers and punctuation stay unchanged)
output=$(../src/emoji_encoder.sh "a1! b")
expected="🍎1! 🌟🍋"
assert_equal "$expected" "$output" "Mixed characters handling"

echo "All tests passed."
