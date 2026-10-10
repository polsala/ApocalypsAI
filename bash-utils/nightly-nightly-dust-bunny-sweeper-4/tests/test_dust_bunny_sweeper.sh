#!/bin/bash

# Test suite for nightly-dust-bunny-sweeper

# --- Test Setup & Teardown ---

TEST_DIR=""
SCRIPT_PATH="$(dirname "$0")"/../src/dust_bunny_sweeper.sh

# Mock rationale:
# We mock 'find' to control the list of files that the script "discovers"
# without actually scanning the real filesystem, ensuring deterministic test results.
# We mock 'rm' to prevent actual file deletion during tests,
# allowing us to verify which files *would* be removed without side effects.
# We mock 'read' to provide automated input for confirmation prompts,
# making tests non-interactive and deterministic.

# Variables for mocks
MOCKED_FIND_OUTPUT=""
MOCKED_RM_CALLS=""
MOCKED_READ_INPUT=""

# Mocked commands
find() {
  echo -e "$MOCKED_FIND_OUTPUT"
}

rm() {
  MOCKED_RM_CALLS+="rm $*\n"
}

read() {
  # Simulate user input for 'read -p' or 'read -n 1'
  if [[ "$1" == "-p" ]]; then
    # For prompt, just echo the input
    echo "$MOCKED_READ_INPUT"
  elif [[ "$1" == "-n" ]]; then
    # For single char, set REPLY
    REPLY="$MOCKED_READ_INPUT"
  fi
}

setup() {
  TEST_DIR=$(mktemp -d)
  export HOME="$TEST_DIR" # Mock HOME for config file location
  mkdir -p "$TEST_DIR/.config"
  MOCKED_FIND_OUTPUT=""
  MOCKED_RM_CALLS=""
  MOCKED_READ_INPUT=""
}

teardown() {
  rm -rf "$TEST_DIR"
}

# --- Assertion Helpers ---

assert_contains() {
  local expected="$1"
  local actual="$2"
  if ! echo "$actual" | grep -qF "$expected"; then
    echo "FAIL: Expected output to contain \"$expected\" but got:\n$actual"
    return 1
  fi
  return 0
}

assert_not_contains() {
  local expected="$1"
  local actual="$2"
  if echo "$actual" | grep -qF "$expected"; then
    echo "FAIL: Expected output NOT to contain \"$expected\" but got:\n$actual"
    return 1
  fi
  return 0
}

assert_equals() {
  local expected="$1"
  local actual="$2"
  if [[ "$expected" != "$actual" ]]; then
    echo "FAIL: Expected \"$expected\" but got \"$actual\""
    return 1
  fi
  return 0
}

# --- Test Cases ---

test_dry_run_identifies_files() {
  echo "Running test_dry_run_identifies_files..."
  MOCKED_FIND_OUTPUT="/tmp/old_log.txt\0/tmp/another_old_file.bak\0"

  output=$(bash "$SCRIPT_PATH" -d /tmp -a 1)

  assert_contains "Found 2 digital dust bunnies! Here's what they look like:" "$output"
  assert_contains "- /tmp/old_log.txt" "$output"
  assert_contains "- /tmp/another_old_file.bak" "$output"
  assert_contains "(This was a dry run. No files were actually deleted.)" "$output"
  assert_equals "" "$MOCKED_RM_CALLS"
}

test_actual_sweep_removes_files_with_confirmation() {
  echo "Running test_actual_sweep_removes_files_with_confirmation..."
  MOCKED_FIND_OUTPUT="/tmp/to_delete_1.log\0/tmp/to_delete_2.tmp\0"
  MOCKED_READ_INPUT="y"

  output=$(bash "$SCRIPT_PATH" -d /tmp -a 1 -n)

  assert_contains "Found 2 digital dust bunnies! Here's what they look like:" "$output"
  assert_contains "Sweeping digital dust bunnies... Poof! They're gone!" "$output"
  assert_contains "rm -v /tmp/to_delete_1.log /tmp/to_delete_2.tmp" "$MOCKED_RM_CALLS"
  assert_not_contains "(This was a dry run. No files were actually deleted.)" "$output"
}

test_actual_sweep_aborted_by_user() {
  echo "Running test_actual_sweep_aborted_by_user..."
  MOCKED_FIND_OUTPUT="/tmp/to_delete_3.log\0"
  MOCKED_READ_INPUT="n"

  output=$(bash "$SCRIPT_PATH" -d /tmp -a 1 -n)

  assert_contains "Found 1 digital dust bunnies! Here's what they look like:" "$output"
  assert_contains "Sweep aborted. The dust bunnies live to see another day. 🐰" "$output"
  assert_equals "" "$MOCKED_RM_CALLS"
}

test_no_old_files_found() {
  echo "Running test_no_old_files_found..."
  MOCKED_FIND_OUTPUT=""

  output=$(bash "$SCRIPT_PATH" -d /tmp -a 1)

  assert_contains "No digital dust bunnies found. Your system is sparkling clean! ✨" "$output"
  assert_equals "" "$MOCKED_RM_CALLS"
}

test_config_file_override() {
  echo "Running test_config_file_override..."
  local custom_config_file="$TEST_DIR/.config/custom_sweeper.conf"
  echo "SCAN_DIRS=\"/custom/dir1 /custom/dir2\"" > "$custom_config_file"
  echo "AGE_DAYS=10" >> "$custom_config_file"

  MOCKED_FIND_OUTPUT="/custom/dir1/old_file.txt\0"

  output=$(bash "$SCRIPT_PATH" -c "$custom_config_file")

  assert_contains "Loading configuration from $custom_config_file..." "$output"
  assert_contains "Directories: /custom/dir1 /custom/dir2" "$output"
  assert_contains "Age threshold: 10 days" "$output"
  assert_contains "- /custom/dir1/old_file.txt" "$output"
}

test_cli_args_override_config() {
  echo "Running test_cli_args_override_config..."
  local custom_config_file="$TEST_DIR/.config/another_sweeper.conf"
  echo "SCAN_DIRS=\"/config/dir\"" > "$custom_config_file"
  echo "AGE_DAYS=50" >> "$custom_config_file"

  MOCKED_FIND_OUTPUT="/cli/dir/cli_old_file.log\0"

  output=$(bash "$SCRIPT_PATH" -c "$custom_config_file" -d /cli/dir -a 5)

  assert_contains "Loading configuration from $custom_config_file..." "$output"
  assert_contains "Directories: /cli/dir" "$output" # CLI should override config
  assert_contains "Age threshold: 5 days" "$output" # CLI should override config
  assert_contains "- /cli/dir/cli_old_file.log" "$output"
}

test_multiple_cli_dirs() {
  echo "Running test_multiple_cli_dirs..."
  MOCKED_FIND_OUTPUT="/dirA/file1\0/dirB/file2\0"

  output=$(bash "$SCRIPT_PATH" -d /dirA -d /dirB -a 1)

  assert_contains "Directories: /dirA /dirB" "$output"
  assert_contains "- /dirA/file1" "$output"
  assert_contains "- /dirB/file2" "$output"
}

# --- Test Runner ---

run_test() {
  local test_name="$1"
  setup
  if "$test_name"; then
    echo "PASS: $test_name"
  else
    echo "FAIL: $test_name"
    exit 1
  fi
  teardown
}

# Execute all tests
run_test test_dry_run_identifies_files
run_test test_actual_sweep_removes_files_with_confirmation
run_test test_actual_sweep_aborted_by_user
run_test test_no_old_files_found
run_test test_config_file_override
run_test test_cli_args_override_config
run_test test_multiple_cli_dirs

echo "All tests passed!"
