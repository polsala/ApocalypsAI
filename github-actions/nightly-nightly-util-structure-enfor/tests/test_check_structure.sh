#!/bin/bash

# Mock rationale: This test script directly invokes src/check_structure.sh with simulated file paths
# and directory structures. It avoids actual Git operations or GitHub API calls by creating
# temporary files and directories, making it deterministic and offline.

# Source the script to be tested
SCRIPT_TO_TEST="$(dirname "$0")"/../src/check_structure.sh

# Function to run the test script and capture output/exit code
run_check() {
    local new_files_str="$1"
    local check_paths_str="$2"
    local expected_exit_code="$3"
    local test_name="$4"

    echo "--- Running Test: $test_name ---"
    output=$(bash "$SCRIPT_TO_TEST" "$new_files_str" "$check_paths_str" 2>&1)
    actual_exit_code=$?

    if [[ "$actual_exit_code" -eq "$expected_exit_code" ]]; then
        echo "PASS: $test_name (Exit code: $actual_exit_code)"
    else
        echo "FAIL: $test_name (Expected exit code: $expected_exit_code, Got: $actual_exit_code)"
        echo "Output:"
        echo "$output"
        exit 1
    fi
    echo ""
}

# --- Test Setup ---
# Create a temporary directory for testing
TEST_DIR=$(mktemp -d)
cd "$TEST_DIR"

# Define classifier paths for testing
TEST_CHECK_PATHS="utils/,python-utils/,rust-utils/"

# --- Test Cases ---

# Test 1: No new utility directories (empty new_files_str)
run_check "" "$TEST_CHECK_PATHS" 0 "No new files, should pass"

# Test 2: New utility directory with correct structure
mkdir -p python-utils/my-awesome-util/tests
touch python-utils/my-awesome-util/README.md
touch python-utils/my-awesome-util/src/main.py
run_check "python-utils/my-awesome-util/README.md python-utils/my-awesome-util/src/main.py" "$TEST_CHECK_PATHS" 0 "Correct structure, should pass"

# Test 3: New utility directory missing README.md
mkdir -p rust-utils/missing-readme/tests
touch rust-utils/missing-readme/src/lib.rs
run_check "rust-utils/missing-readme/src/lib.rs" "$TEST_CHECK_PATHS" 1 "Missing README.md, should fail"

# Test 4: New utility directory missing tests/ directory
mkdir -p utils/missing-tests
touch utils/missing-tests/README.md
touch utils/missing-tests/script.sh
run_check "utils/missing-tests/README.md utils/missing-tests/script.sh" "$TEST_CHECK_PATHS" 1 "Missing tests/ directory, should fail"

# Test 5: New utility directory missing both README.md and tests/
mkdir -p python-utils/missing-both
touch python-utils/missing-both/main.py
run_check "python-utils/missing-both/main.py" "$TEST_CHECK_PATHS" 1 "Missing both, should fail"

# Test 6: Multiple new utility directories, some passing, some failing
mkdir -p rust-utils/good-util/tests
touch rust-utils/good-util/README.md
touch rust-utils/good-util/src/main.rs

mkdir -p utils/bad-util-no-readme/tests
touch utils/bad-util-no-readme/script.sh

mkdir -p python-utils/bad-util-no-tests
touch python-utils/bad-util-no-tests/README.md
touch python-utils/bad-util-no-tests/app.py

run_check "rust-utils/good-util/README.md rust-utils/good-util/src/main.rs utils/bad-util-no-readme/script.sh python-utils/bad-util-no-tests/README.md python-utils/bad-util-no-tests/app.py" "$TEST_CHECK_PATHS" 1 "Mixed good and bad, should fail"

# Test 7: New files outside of check-paths (should be ignored)
mkdir -p other-dir
touch other-dir/some-file.txt
run_check "other-dir/some-file.txt" "$TEST_CHECK_PATHS" 0 "Files outside check-paths, should pass"

# Test 8: New files directly in a classifier path (not a utility dir) - should be ignored
touch python-utils/top-level-file.txt
run_check "python-utils/top-level-file.txt" "$TEST_CHECK_PATHS" 0 "File directly in classifier path, should pass"

# Test 9: New utility directory with nested files, ensuring root is correctly identified
mkdir -p python-utils/nested-util/sub/dir/tests
touch python-utils/nested-util/README.md
touch python-utils/nested-util/sub/dir/main.py
run_check "python-utils/nested-util/README.md python-utils/nested-util/sub/dir/main.py" "$TEST_CHECK_PATHS" 0 "Nested files, correct root, should pass"

# Test 10: No new utility directories within check-paths, but other new files exist
mkdir -p docs
touch docs/new-doc.md
run_check "docs/new-doc.md" "$TEST_CHECK_PATHS" 0 "New files outside check-paths, should pass"

# --- Cleanup ---
cd -
rm -rf "$TEST_DIR"

echo "All tests completed."
