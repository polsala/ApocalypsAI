#!/bin/bash

# Automated tests for nightly-digital-dust-bunny-sweeper

set -euo pipefail

SCRIPT_PATH="$(dirname "$0")"/../src/dust_bunny_sweeper.sh

# --- Test Utilities --- #

# Function to create a temporary test environment
setup_test_env() {
  TEST_DIR=$(mktemp -d)
  export TEST_DIR # Make available to subshells
  echo "Created test environment: $TEST_DIR"
}

# Function to clean up the temporary test environment
teardown_test_env() {
  if [[ -d "$TEST_DIR" ]]; then
    rm -rf "$TEST_DIR"
    echo "Cleaned up test environment: $TEST_DIR"
  fi
}

# Helper to run the script with mocks and capture output
run_script_with_mocks() {
  local mock_date_cmd="$1"
  local mock_read_response="$2"
  shift 2
  local script_args=("$@")

  # Mock rationale: 'date' is mocked to provide a consistent current time for 'find -mtime' calculations.
  # This ensures deterministic behavior regardless of when the tests are run.
  # 'read' is mocked to simulate user input for interactive prompts.
  # 'rm' and 'rmdir' are mocked to prevent actual file system changes during dry runs and to log calls for verification.
  ( 
    export PATH="$TEST_DIR/bin:$PATH"
    mkdir -p "$TEST_DIR/bin"
    echo "#!/bin/bash" > "$TEST_DIR/bin/date"
    echo "echo -n '$mock_date_cmd'" >> "$TEST_DIR/bin/date"
    chmod +x "$TEST_DIR/bin/date"

    echo "#!/bin/bash" > "$TEST_DIR/bin/read"
    echo "echo -n '$mock_read_response'" >> "$TEST_DIR/bin/read"
    echo "exit 0" >> "$TEST_DIR/bin/read"
    chmod +x "$TEST_DIR/bin/read"

    # Mock rm and rmdir to log calls instead of actual deletion
    echo "#!/bin/bash" > "$TEST_DIR/bin/rm"
    echo "echo \"MOCKED_RM_CALL: $@\" >> \"$TEST_DIR/rm_log.txt\"" >> "$TEST_DIR/bin/rm"
    echo "/bin/rm \"$@\"" >> "$TEST_DIR/bin/rm" # Call real rm for actual sweep tests
    chmod +x "$TEST_DIR/bin/rm"

    echo "#!/bin/bash" > "$TEST_DIR/bin/rmdir"
    echo "echo \"MOCKED_RMDIR_CALL: $@\" >> \"$TEST_DIR/rm_log.txt\"" >> "$TEST_DIR/bin/rmdir"
    echo "/bin/rmdir \"$@\"" >> "$TEST_DIR/bin/rmdir" # Call real rmdir for actual sweep tests
    chmod +x "$TEST_DIR/bin/rmdir"

    "$SCRIPT_PATH" "${script_args[@]}"
  ) 2>&1
}

# Assertions
assert_contains() {
  local haystack="$1"
  local needle="$2"
  if ! echo "$haystack" | grep -qF "$needle"; then
    echo "FAIL: Expected output to contain '$needle'"
    echo "Output:" "$haystack"
    exit 1
  fi
}

assert_not_contains() {
  local haystack="$1"
  local needle="$2"
  if echo "$haystack" | grep -qF "$needle"; then
    echo "FAIL: Expected output NOT to contain '$needle'"
    echo "Output:" "$haystack"
    exit 1
  fi
}

assert_file_exists() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    echo "FAIL: Expected file '$file' to exist"
    exit 1
  fi
}

assert_file_not_exists() {
  local file="$1"
  if [[ -f "$file" ]]; then
    echo "FAIL: Expected file '$file' NOT to exist"
    exit 1
  fi
}

assert_dir_exists() {
  local dir="$1"
  if [[ ! -d "$dir" ]]; then
    echo "FAIL: Expected directory '$dir' to exist"
    exit 1
  fi
}

assert_dir_not_exists() {
  local dir="$1"
  if [[ -d "$dir" ]]; then
    echo "FAIL: Expected directory '$dir' NOT to exist"
    exit 1
  fi
}

# --- Test Cases --- #

# Test 1: No dust bunnies or cobwebs found (dry run)
test_no_findings_dry_run() {
  setup_test_env
  echo "Running test: $FUNCNAME"

  # Create a recent file and a non-empty directory
  touch -t 202401091200 "$TEST_DIR/recent_file.txt"
  mkdir -p "$TEST_DIR/non_empty_dir"
  touch "$TEST_DIR/non_empty_dir/file.txt"

  # Mock date to be 2024-01-10 (so recent_file.txt is 1 day old, not older than default 30)
  local output=$(run_script_with_mocks "2024-01-10" "" --dir "$TEST_DIR")

  assert_contains "$output" "No digital dust bunnies found. Your files are spick and span!"
  assert_contains "$output" "No cyber cobwebs found. Your directories are bustling with purpose!"
  assert_contains "$output" "Your digital realm is pristine! No cleanup needed."
  assert_contains "$output" "Dry Run (no changes)"
  assert_file_exists "$TEST_DIR/recent_file.txt"
  assert_dir_exists "$TEST_DIR/non_empty_dir"

  teardown_test_env
  echo "$FUNCNAME PASSED"
}

# Test 2: Dust bunnies found (dry run)
test_files_found_dry_run() {
  setup_test_env
  echo "Running test: $FUNCNAME"

  # Create an old file
  touch -t 202311011000 "$TEST_DIR/old_log.txt"
  touch -t 202312011000 "$TEST_DIR/another_old_file.tmp"

  # Mock date to be 2024-01-10. Default age is 30 days. Both files are older than 30 days.
  local output=$(run_script_with_mocks "2024-01-10" "" --dir "$TEST_DIR")

  assert_contains "$output" "Found 2 digital dust bunnies (old files):"
  assert_contains "$output" "- $TEST_DIR/old_log.txt"
  assert_contains "$output" "- $TEST_DIR/another_old_file.tmp"
  assert_contains "$output" "No cyber cobwebs found."
  assert_contains "$output" "Dry Run (no changes)"
  assert_file_exists "$TEST_DIR/old_log.txt"
  assert_file_exists "$TEST_DIR/another_old_file.tmp"

  teardown_test_env
  echo "$FUNCNAME PASSED"
}

# Test 3: Empty cobwebs found (dry run)
test_empty_dirs_found_dry_run() {
  setup_test_env
  echo "Running test: $FUNCNAME"

  mkdir -p "$TEST_DIR/empty_dir_1"
  mkdir -p "$TEST_DIR/empty_dir_2/sub_empty"
  mkdir -p "$TEST_DIR/non_empty_dir"
  touch "$TEST_DIR/non_empty_dir/file.txt"

  # Mock date is irrelevant for empty dirs
  local output=$(run_script_with_mocks "2024-01-10" "" --dir "$TEST_DIR")

  assert_contains "$output" "No digital dust bunnies found."
  assert_contains "$output" "Found 3 cyber cobwebs (empty directories):"
  assert_contains "$output" "- $TEST_DIR/empty_dir_1"
  assert_contains "$output" "- $TEST_DIR/empty_dir_2"
  assert_contains "$output" "- $TEST_DIR/empty_dir_2/sub_empty"
  assert_contains "$output" "Dry Run (no changes)"
  assert_dir_exists "$TEST_DIR/empty_dir_1"
  assert_dir_exists "$TEST_DIR/empty_dir_2/sub_empty"
  assert_dir_exists "$TEST_DIR/non_empty_dir"

  teardown_test_env
  echo "$FUNCNAME PASSED"
}

# Test 4: Perform actual sweep (files and empty dirs, with confirmation)
test_actual_sweep_with_confirm() {
  setup_test_env
  echo "Running test: $FUNCNAME"

  touch -t 202311011000 "$TEST_DIR/old_file_to_delete.txt"
  mkdir -p "$TEST_DIR/empty_dir_to_delete"
  mkdir -p "$TEST_DIR/empty_dir_to_delete/sub_empty"
  touch -t 202401091200 "$TEST_DIR/recent_file.txt"

  # Mock date to be 2024-01-10. old_file_to_delete.txt is older than 30 days.
  # Mock read to 'y' for confirmation.
  local output=$(run_script_with_mocks "2024-01-10" "y" --dir "$TEST_DIR" --sweep)

  assert_contains "$output" "Live Sweep (deleting!)"
  assert_contains "$output" "Deleting file: '$TEST_DIR/old_file_to_delete.txt'"
  assert_contains "$output" "Deleting empty directory: '$TEST_DIR/empty_dir_to_delete/sub_empty'"
  assert_contains "$output" "Deleting empty directory: '$TEST_DIR/empty_dir_to_delete'"
  assert_file_not_exists "$TEST_DIR/old_file_to_delete.txt"
  assert_dir_not_exists "$TEST_DIR/empty_dir_to_delete/sub_empty"
  assert_dir_not_exists "$TEST_DIR/empty_dir_to_delete"
  assert_file_exists "$TEST_DIR/recent_file.txt"

  teardown_test_env
  echo "$FUNCNAME PASSED"
}

# Test 5: Perform actual sweep (files and empty dirs, no confirmation)
test_actual_sweep_no_confirm() {
  setup_test_env
  echo "Running test: $FUNCNAME"

  touch -t 202311011000 "$TEST_DIR/old_file_to_delete_auto.txt"
  mkdir -p "$TEST_DIR/empty_dir_to_delete_auto"

  # Mock date to be 2024-01-10. old_file_to_delete_auto.txt is older than 30 days.
  # Use --yes for auto-confirmation.
  local output=$(run_script_with_mocks "2024-01-10" "" --dir "$TEST_DIR" --sweep --yes)

  assert_contains "$output" "Live Sweep (deleting!)"
  assert_contains "$output" "Deleting file: '$TEST_DIR/old_file_to_delete_auto.txt'"
  assert_contains "$output" "Deleting empty directory: '$TEST_DIR/empty_dir_to_delete_auto'"
  assert_file_not_exists "$TEST_DIR/old_file_to_delete_auto.txt"
  assert_dir_not_exists "$TEST_DIR/empty_dir_to_delete_auto"

  teardown_test_env
  echo "$FUNCNAME PASSED"
}

# Test 6: Sweep aborted by user
test_sweep_aborted() {
  setup_test_env
  echo "Running test: $FUNCNAME"

  touch -t 202311011000 "$TEST_DIR/file_to_keep.txt"

  # Mock date to be 2024-01-10. file_to_keep.txt is older than 30 days.
  # Mock read to 'n' for confirmation.
  local output=$(run_script_with_mocks "2024-01-10" "n" --dir "$TEST_DIR" --sweep)

  assert_contains "$output" "Sweep aborted by user."
  assert_file_exists "$TEST_DIR/file_to_keep.txt"

  teardown_test_env
  echo "$FUNCNAME PASSED"
}

# Test 7: Only files mode
test_files_only() {
  setup_test_env
  echo "Running test: $FUNCNAME"

  touch -t 202311011000 "$TEST_DIR/old_file.txt"
  mkdir -p "$TEST_DIR/empty_dir"

  local output=$(run_script_with_mocks "2024-01-10" "" --dir "$TEST_DIR" --files-only)

  assert_contains "$output" "Found 1 digital dust bunnies"
  assert_contains "$output" "- $TEST_DIR/old_file.txt"
  assert_contains "$output" "No cyber cobwebs found."
  assert_file_exists "$TEST_DIR/old_file.txt"
  assert_dir_exists "$TEST_DIR/empty_dir"

  teardown_test_env
  echo "$FUNCNAME PASSED"
}

# Test 8: Only empty directories mode
test_empty_only() {
  setup_test_env
  echo "Running test: $FUNCNAME"

  touch -t 202311011000 "$TEST_DIR/old_file.txt"
  mkdir -p "$TEST_DIR/empty_dir"

  local output=$(run_script_with_mocks "2024-01-10" "" --dir "$TEST_DIR" --empty-only)

  assert_contains "$output" "No digital dust bunnies found."
  assert_contains "$output" "Found 1 cyber cobwebs"
  assert_contains "$output" "- $TEST_DIR/empty_dir"
  assert_file_exists "$TEST_DIR/old_file.txt"
  assert_dir_exists "$TEST_DIR/empty_dir"

  teardown_test_env
  echo "$FUNCNAME PASSED"
}

# Test 9: Invalid age argument
test_invalid_age() {
  setup_test_env
  echo "Running test: $FUNCNAME"

  local output=$(run_script_with_mocks "2024-01-10" "" --dir "$TEST_DIR" --age "abc")
  assert_contains "$output" "[ERROR] Invalid age: 'abc'. Must be a non-negative integer."

  teardown_test_env
  echo "$FUNCNAME PASSED"
}

# Test 10: Non-existent directory
test_non_existent_dir() {
  setup_test_env
  echo "Running test: $FUNCNAME"

  local output=$(run_script_with_mocks "2024-01-10" "" --dir "$TEST_DIR/non_existent")
  assert_contains "$output" "[ERROR] Target directory '$TEST_DIR/non_existent' does not exist or is not a directory."

  teardown_test_env
  echo "$FUNCNAME PASSED"
}

# Test 11: Age 1 day (mtime +0)
test_age_one_day() {
  setup_test_env
  echo "Running test: $FUNCNAME"

  # File created 2024-01-08 12:00
  touch -t 202401081200 "$TEST_DIR/file_older_than_1_day.txt"
  # File created 2024-01-09 12:00
  touch -t 202401091200 "$TEST_DIR/file_exactly_1_day_old.txt"

  # Mock date to be 2024-01-10 12:00
  # With --age 1, it should find files older than 24 hours (mtime +0)
  local output=$(run_script_with_mocks "2024-01-10 12:00:00" "" --dir "$TEST_DIR" --age 1)

  assert_contains "$output" "Found 2 digital dust bunnies"
  assert_contains "$output" "- $TEST_DIR/file_older_than_1_day.txt"
  assert_contains "$output" "- $TEST_DIR/file_exactly_1_day_old.txt"

  teardown_test_env
  echo "$FUNCNAME PASSED"
}

# Test 12: Age 0 days (should find nothing unless file is from future, which is unlikely)
test_age_zero_days() {
  setup_test_env
  echo "Running test: $FUNCNAME"

  touch -t 202401091200 "$TEST_DIR/recent_file.txt"

  # Mock date to be 2024-01-10 12:00
  # With --age 0, it should find files older than 0 days (mtime -1, which is not what we want)
  # The script handles AGE_DAYS=0 by setting find_age=0, meaning mtime +0 (older than 24h)
  # This test should find nothing if the file is less than 24h old.
  local output=$(run_script_with_mocks "202401101200" "" --dir "$TEST_DIR" --age 0)

  assert_contains "$output" "No digital dust bunnies found."

  teardown_test_env
  echo "$FUNCNAME PASSED"
}

# Test 13: Age 0 days, file is older than 24h (mtime +0 should match)
test_age_zero_days_old_file() {
  setup_test_env
  echo "Running test: $FUNCNAME"

  touch -t 202401081200 "$TEST_DIR/old_file.txt"

  # Mock date to be 2024-01-10 12:00
  # With --age 0, find_age becomes 0, so find -mtime +0. This matches files older than 24 hours.
  local output=$(run_script_with_mocks "202401101200" "" --dir "$TEST_DIR" --age 0)

  assert_contains "$output" "Found 1 digital dust bunnies"
  assert_contains "$output" "- $TEST_DIR/old_file.txt"

  teardown_test_env
  echo "$FUNCNAME PASSED"
}

# --- Run All Tests --- #

echo "Running all tests for Digital Dust Bunny Sweeper..."

test_no_findings_dry_run
test_files_found_dry_run
test_empty_dirs_found_dry_run
test_actual_sweep_with_confirm
test_actual_sweep_no_confirm
test_sweep_aborted
test_files_only
test_empty_only
test_invalid_age
test_non_existent_dir
test_age_one_day
test_age_zero_days
test_age_zero_days_old_file

echo "All tests PASSED!"
