#!/bin/bash

# Test suite for nightly-bash-uptime-emoji
# Uses mock functions to simulate different uptime scenarios

set -euo pipefail

# Source the main script (but mock external commands)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MAIN_SCRIPT="$SCRIPT_DIR/src/main.sh"

# Mock functions
mock_uptime_seconds() {
  echo "$MOCK_UPTIME"
}

mock_command_exists() {
  case "$1" in
    uptime|awk|sed)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

# Test helper functions
run_test() {
  local test_name="$1"
  local expected_exit_code="$2"
  shift 2
  local args=("$@")
  
  echo "Running test: $test_name"
  
  # Mock external commands
  export -f mock_uptime_seconds
  export -f mock_command_exists
  
  # Run the script with mocked functions
  if MOCK_UPTIME=3600 bash -c "alias uptime='echo 1 day, 2:30' && alias awk='echo' && alias sed='echo' && source \"$MAIN_SCRIPT\" && main \"${args[@]}\"" 2>/dev/null; then
    actual_exit_code=0
  else
    actual_exit_code=$?
  fi
  
  if [[ $actual_exit_code -eq $expected_exit_code ]]; then
    echo "✅ PASS: $test_name"
  else
    echo "❌ FAIL: $test_name (expected exit code $expected_exit_code, got $actual_exit_code)"
    return 1
  fi
}

# Test the helper functions directly
test_format_uptime() {
  echo "Testing format_uptime function"
  
  # Source the main script to get access to functions
  source "$MAIN_SCRIPT"
  
  # Test format_uptime
  local result
  result=$(format_uptime 300)
  if [[ "$result" == "5 minute(s)" ]]; then
    echo "✅ PASS: format_uptime for 5 minutes"
  else
    echo "❌ FAIL: format_uptime for 5 minutes (got: $result)"
    return 1
  fi
  
  result=$(format_uptime 7260)
  if [[ "$result" == "2 hour(s), 1 minute(s)" ]]; then
    echo "✅ PASS: format_uptime for 2 hours 1 minute"
  else
    echo "❌ FAIL: format_uptime for 2 hours 1 minute (got: $result)"
    return 1
  fi
  
  result=$(format_uptime 172860)
  if [[ "$result" == "2 day(s), 0 hour(s), 1 minute(s)" ]]; then
    echo "✅ PASS: format_uptime for 2 days"
  else
    echo "❌ FAIL: format_uptime for 2 days (got: $result)"
    return 1
  fi
}

test_select_emoji() {
  echo "Testing select_emoji function"
  
  # Source the main script to get access to functions
  source "$MAIN_SCRIPT"
  
  # Test emoji selection based on uptime
  local emoji
  emoji=$(select_emoji 60 "")
  if [[ "$emoji" == "😴" ]]; then
    echo "✅ PASS: select_emoji for 1 minute"
  else
    echo "❌ FAIL: select_emoji for 1 minute (got: $emoji)"
    return 1
  fi
  
  emoji=$(select_emoji 3600 "")
  if [[ "$emoji" == "💪" ]]; then
    echo "✅ PASS: select_emoji for 1 hour"
  else
    echo "❌ FAIL: select_emoji for 1 hour (got: $emoji)"
    return 1
  fi
  
  emoji=$(select_emoji 604800 "")
  if [[ "$emoji" == "🤖" ]]; then
    echo "✅ PASS: select_emoji for 1 week"
  else
    echo "❌ FAIL: select_emoji for 1 week (got: $emoji)"
    return 1
  fi
  
  # Test custom emoji
  emoji=$(select_emoji 3600 "🚀")
  if [[ "$emoji" == "🚀" ]]; then
    echo "✅ PASS: select_emoji with custom emoji"
  else
    echo "❌ FAIL: select_emoji with custom emoji (got: $emoji)"
    return 1
  fi
}

test_validate_emoji() {
  echo "Testing validate_emoji function"
  
  # Source the main script to get access to functions
  source "$MAIN_SCRIPT"
  
  # Test valid emoji
  if validate_emoji "🚀"; then
    echo "✅ PASS: validate_emoji for valid emoji"
  else
    echo "❌ FAIL: validate_emoji for valid emoji"
    return 1
  fi
  
  # Test empty emoji
  if ! validate_emoji ""; then
    echo "✅ PASS: validate_emoji for empty emoji"
  else
    echo "❌ FAIL: validate_emoji for empty emoji should fail"
    return 1
  fi
  
  # Test too long emoji
  if ! validate_emoji "this_emoji_is_way_too_long_for_our_purposes"; then
    echo "✅ PASS: validate_emoji for too long emoji"
  else
    echo "❌ FAIL: validate_emoji for too long emoji should fail"
    return 1
  fi
}

# Main test execution
main_test() {
  echo "=== Running Test Suite for nightly-bash-uptime-emoji ==="
  echo
  
  # Test helper functions
  test_format_uptime
  echo
  test_select_emoji
  echo
  test_validate_emoji
  echo
  
  # Test script execution (basic functionality)
  echo "Testing script execution"
  
  # Test help option
  run_test "Help option" 0 --help
  echo
  
  # Test with custom emoji
  run_test "Custom emoji" 0 --emoji "🚀"
  echo
  
  # Test verbose mode
  run_test "Verbose mode" 0 --verbose
  echo
  
  # Test unknown option
  run_test "Unknown option" 1 --invalid
  echo
  
  echo "=== Test Suite Complete ==="
}

# Run the tests
main_test
