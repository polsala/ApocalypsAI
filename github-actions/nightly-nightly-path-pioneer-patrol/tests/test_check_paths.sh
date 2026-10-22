#!/bin/bash

# Mock rationale: This test script directly calls the 'check_paths.sh' script
# and pipes simulated file paths to its stdin, mimicking how GitHub Actions
# would provide the list of changed files. This allows for deterministic,
# offline testing without needing actual Git repositories or GitHub API calls.

SCRIPT_TO_TEST="../src/check_paths.sh"

# Function to run a test case
run_test() {
  local test_name="$1"
  local expected_to_fail="$2"
  shift 2
  local input_files=("$@")

  echo "--- Running $test_name ---"
  OUTPUT=$(printf "%s\n" "${input_files[@]}" | bash "$SCRIPT_TO_TEST" 2>&1)
  STATUS=$?

  if [[ "$expected_to_fail" == "true" ]]; then
    if [[ "$STATUS" -ne 0 ]]; then
      echo "$test_name PASSED: Script failed as expected."
    else
      echo "$test_name FAILED: Expected script to fail, but it passed."
      echo "Output: $OUTPUT"
      exit 1
    fi
  else
    if [[ "$STATUS" -eq 0 ]]; then
      echo "$test_name PASSED."
    else
      echo "$test_name FAILED: Expected script to pass, but it failed."
      echo "Output: $OUTPUT"
      exit 1
    fi
  fi
  echo ""
}

# --- Test Cases ---

# Test 1: Valid V2 path (python-utils)
run_test "Test 1: Valid V2 path (python-utils)" "false" \
  "python-utils/nightly-my-awesome-tool/README.md" \
  "python-utils/nightly-my-awesome-tool/src/main.py" \
  "python-utils/nightly-my-awesome-tool/tests/test_main.py"

# Test 2: Valid V2 path (rust-utils)
run_test "Test 2: Valid V2 path (rust-utils)" "false" \
  "rust-utils/nightly-rusty-gadget/README.md" \
  "rust-utils/nightly-rusty-gadget/src/lib.rs"

# Test 3: Legacy 'utils/' path - EXPECTED TO FAIL
run_test "Test 3: Legacy 'utils/' path - EXPECTED TO FAIL" "true" \
  "utils/nightly-old-style-util/README.md" \
  "utils/nightly-old-style-util/src/script.sh"

# Test 4: Invalid utility name (no 'nightly-' prefix) - EXPECTED TO FAIL
run_test "Test 4: Invalid utility name (no 'nightly-' prefix) - EXPECTED TO FAIL" "true" \
  "python-utils/my-bad-tool/README.md"

# Test 5: Invalid utility name (camelCase instead of kebab-case) - EXPECTED TO FAIL
run_test "Test 5: Invalid utility name (camelCase) - EXPECTED TO FAIL" "true" \
  "python-utils/nightlyCamelCaseTool/README.md"

# Test 6: Unrecognized top-level directory - EXPECTED TO FAIL
run_test "Test 6: Unrecognized top-level directory - EXPECTED TO FAIL" "true" \
  "my-custom-dir/nightly-tool/README.md"

# Test 7: Multiple valid utilities
run_test "Test 7: Multiple valid utilities" "false" \
  "python-utils/nightly-tool-a/README.md" \
  "python-utils/nightly-tool-a/src/a.py" \
  "rust-utils/nightly-tool-b/README.md" \
  "rust-utils/nightly-tool-b/src/b.rs"

# Test 8: Mixed valid and invalid - EXPECTED TO FAIL
run_test "Test 8: Mixed valid and invalid - EXPECTED TO FAIL" "true" \
  "python-utils/nightly-good-tool/README.md" \
  "utils/nightly-bad-tool/README.md" # Invalid

# Test 9: Valid utility name with numbers
run_test "Test 9: Valid utility name with numbers" "false" \
  "python-utils/nightly-tool-v2/README.md"

# Test 10: Valid utility name with multiple hyphens
run_test "Test 10: Valid utility name with multiple hyphens" "false" \
  "python-utils/nightly-super-duper-tool/README.md"

echo "All tests completed."
