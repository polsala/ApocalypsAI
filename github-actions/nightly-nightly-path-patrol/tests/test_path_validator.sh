#!/bin/bash

# Mock rationale: We need to simulate the output of the 'gh pr view' command
# without actually making network requests. This function replaces the real 'gh'
# command during testing to provide deterministic, offline results.
mock_gh() {
  local pr_number="$1"
  local json_flag="$2"
  local jq_filter="$3"

  case "$pr_number" in
    "101") # Valid utility
      echo "python-utils/nightly-valid-util/README.md"
      echo "python-utils/nightly-valid-util/src/main.py"
      echo "python-utils/nightly-valid-util/tests/test_main.py"
      ;;
    "102") # Missing README
      echo "rust-utils/nightly-no-readme/src/main.rs"
      echo "rust-utils/nightly-no-readme/tests/test_main.rs"
      ;;
    "103") # Missing src
      echo "bash-utils/nightly-no-src/README.md"
      echo "bash-utils/nightly-no-src/tests/test_main.sh"
      ;;
    "104") # Missing tests
      echo "go-utils/nightly-no-tests/README.md"
      echo "go-utils/nightly-no-tests/src/main.go"
      ;;
    "105") # No nightly- prefix
      echo "python-utils/invalid-prefix/README.md"
      echo "python-utils/invalid-prefix/src/main.py"
      echo "python-utils/invalid-prefix/tests/test_main.py"
      ;;
    "106") # Multiple utilities, one invalid
      echo "python-utils/nightly-good-one/README.md"
      echo "python-utils/nightly-good-one/src/main.py"
      echo "python-utils/nightly-good-one/tests/test_main.py"
      echo "rust-utils/nightly-bad-one/src/main.rs" # Missing README
      echo "rust-utils/nightly-bad-one/tests/test_main.rs"
      ;;
    "107") # No utility files added
      echo ""
      ;;
    "108") # Legacy path valid
      echo "utils/nightly-legacy-util/README.md"
      echo "utils/nightly-legacy-util/src/main.py"
      echo "utils/nightly-legacy-util/tests/test_main.py"
      ;;
    "109") # Empty src directory
      echo "python-utils/nightly-empty-src/README.md"
      echo "python-utils/nightly-empty-src/tests/test_main.py"
      ;;
    "110") # Empty tests directory
      echo "python-utils/nightly-empty-tests/README.md"
      echo "python-utils/nightly-empty-tests/src/main.py"
      ;;
    *)
      echo "Error: Unknown PR number for mock_gh: $pr_number" >&2
      exit 1
      ;;
  esac
}

# Override the 'gh' command for testing
export -f gh
# Ensure the original gh command is not called
gh() { mock_gh "$@"; }

# Store original PATH to restore later
OLD_PATH="$PATH"
# Add current directory to PATH so our mock 'gh' is found
export PATH="$(pwd):$PATH"

# Setup: Create dummy files and directories for testing
setup_test_env() {
  local test_dir="$1"
  mkdir -p "$test_dir"
  cd "$test_dir" || exit 1

  # Create dummy utility structures
  mkdir -p python-utils/nightly-valid-util/src
  mkdir -p python-utils/nightly-valid-util/tests
  touch python-utils/nightly-valid-util/README.md
  touch python-utils/nightly-valid-util/src/main.py
  touch python-utils/nightly-valid-util/tests/test_main.py

  mkdir -p rust-utils/nightly-no-readme/src
  mkdir -p rust-utils/nightly-no-readme/tests
  touch rust-utils/nightly-no-readme/src/main.rs
  touch rust-utils/nightly-no-readme/tests/test_main.rs

  mkdir -p bash-utils/nightly-no-src/tests
  touch bash-utils/nightly-no-src/README.md
  # src/ is intentionally missing
  touch bash-utils/nightly-no-src/tests/test_main.sh

  mkdir -p go-utils/nightly-no-tests/src
  touch go-utils/nightly-no-tests/README.md
  touch go-utils/nightly-no-tests/src/main.go
  # tests/ is intentionally missing

  mkdir -p python-utils/invalid-prefix/src
  mkdir -p python-utils/invalid-prefix/tests
  touch python-utils/invalid-prefix/README.md
  touch python-utils/invalid-prefix/src/main.py
  touch python-utils/invalid-prefix/tests/test_main.py

  mkdir -p python-utils/nightly-good-one/src
  mkdir -p python-utils/nightly-good-one/tests
  touch python-utils/nightly-good-one/README.md
  touch python-utils/nightly-good-one/src/main.py
  touch python-utils/nightly-good-one/tests/test_main.py

  mkdir -p rust-utils/nightly-bad-one/src
  mkdir -p rust-utils/nightly-bad-one/tests
  # README.md is intentionally missing
  touch rust-utils/nightly-bad-one/src/main.rs
  touch rust-utils/nightly-bad-one/tests/test_main.rs

  mkdir -p utils/nightly-legacy-util/src
  mkdir -p utils/nightly-legacy-util/tests
  touch utils/nightly-legacy-util/README.md
  touch utils/nightly-legacy-util/src/main.py
  touch utils/nightly-legacy-util/tests/test_main.py

  mkdir -p python-utils/nightly-empty-src/src
  mkdir -p python-utils/nightly-empty-src/tests
  touch python-utils/nightly-empty-src/README.md
  touch python-utils/nightly-empty-src/tests/test_main.py
  # src/ is empty

  mkdir -p python-utils/nightly-empty-tests/src
  mkdir -p python-utils/nightly-empty-tests/tests
  touch python-utils/nightly-empty-tests/README.md
  touch python-utils/nightly-empty-tests/src/main.py
  # tests/ is empty

  # Create the validator script itself for testing
  mkdir -p github-actions/nightly-path-patrol/src
  cp ../../src/path_validator.sh github-actions/nightly-path-patrol/src/path_validator.sh
  chmod +x github-actions/nightly-path-patrol/src/path_validator.sh
}

# Cleanup: Remove temporary files and directories
cleanup_test_env() {
  cd - > /dev/null || exit 1 # Go back to original directory
  rm -rf "$1"
  export PATH="$OLD_PATH" # Restore original PATH
  unset -f gh # Unset the mock function
}

# Test function
run_test() {
  local test_name="$1"
  local pr_number="$2"
  local expected_exit_code="$3"
  local temp_dir="temp_test_dir_$(echo "$test_name" | tr ' ' '_')"

  echo "Running test: $test_name (PR #$pr_number, Expected: $expected_exit_code)"
  setup_test_env "$temp_dir"

  # Run the validator script
  github-actions/nightly-path-patrol/src/path_validator.sh "$pr_number" "mock_token" > /dev/null 2>&1 # Suppress output for cleaner test logs
  local actual_exit_code=$?

  if [ "$actual_exit_code" -eq "$expected_exit_code" ]; then
    echo "PASS: $test_name"
  else
    echo "FAIL: $test_name (Expected: $expected_exit_code, Got: $actual_exit_code)"
    cleanup_test_env "$temp_dir"
    exit 1
  fi

  cleanup_test_env "$temp_dir"
}

# Run all tests
run_test "Valid utility" "101" 0
run_test "Missing README.md" "102" 1
run_test "Missing src/ directory" "103" 1
run_test "Missing tests/ directory" "104" 1
run_test "Missing nightly- prefix" "105" 1
run_test "Multiple utilities, one invalid" "106" 1
run_test "No utility files added" "107" 0
run_test "Valid legacy utility" "108" 0
run_test "Empty src directory" "109" 1
run_test "Empty tests directory" "110" 1

echo "All tests passed!"
