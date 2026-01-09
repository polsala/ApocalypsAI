#!/usr/bin/env bash
set -euo pipefail

# Helper for assertions
assert_eq() {
  local expected="$1"
  local actual="$2"
  local test_desc="$3"
  if [[ "$expected" == "$actual" ]]; then
    echo "[PASS] $test_desc"
  else
    echo "[FAIL] $test_desc"
    echo "  Expected: $expected"
    echo "  Got     : $actual"
    exit 1
  fi
}

# Make sure the script is executable
chmod +x ../src/decode.sh

# Test 1: Default ROT13
output=$(../src/decode.sh "Uryyb Jbeyq!")
assert_eq "Hello World!" "$output" "Default ROT13 decoding"

# Test 2: Custom shift of 5 (decode)
output=$(../src/decode.sh 5 "fgh CDE")
assert_eq "abc XYZ" "$output" "Custom shift 5 decoding"

# Test 3: Reading from stdin with default shift
output=$(echo "Gur dhvpx oebja sbk whzcf bire gur ynml qbt" | ../src/decode.sh)
assert_eq "The quick brown fox jumps over the lazy dog" "$output" "STDIN input with ROT13"

echo "All tests passed."
