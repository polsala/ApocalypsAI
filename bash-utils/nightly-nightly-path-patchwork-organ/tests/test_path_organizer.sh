#!/bin/bash

# Automated tests for Nightly PATH Patchwork Organizer

# --- Test Setup ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
UTIL_SCRIPT="$SCRIPT_DIR/../src/path_organizer.sh"
TEMP_DIR=""

# Function to set up test environment
setup_test_env() {
    TEMP_DIR=$(mktemp -d 2>/dev/null || mktemp -d -t 'path_test')
    if [[ ! -d "$TEMP_DIR" ]]; then
        echo "Failed to create temporary directory."
        exit 1
    fi
    # Mock rationale: Create dummy directories to simulate existing paths for testing.
    mkdir -p "$TEMP_DIR/existing1"
    mkdir -p "$TEMP_DIR/existing2"
    mkdir -p "$TEMP_DIR/a"
    mkdir -p "$TEMP_DIR/b"
    mkdir -p "$TEMP_DIR/c"
    mkdir -p "$TEMP_DIR/d"
    mkdir -p "$TEMP_DIR/e"
}

# Function to clean up test environment
cleanup_test_env() {
    if [[ -d "$TEMP_DIR" ]]; then
        rm -rf "$TEMP_DIR"
    fi
}

# Register cleanup function to run on exit
trap cleanup_test_env EXIT

# --- Test Helper Functions ---

# Run a test case
run_test() {
    local test_name="$1"
    local mock_path="$2"
    local expected_output="$3"
    local options="$4"
    local actual_output

    echo -n "Running test: $test_name... "

    # Run the utility script with the mocked PATH and capture output
    # Mock rationale: PATH is explicitly set for the subshell running the utility,
    # and dummy directories are created in TEMP_DIR to simulate existence.
    # This makes the test deterministic and offline.
    actual_output=$(PATH="$mock_path" "$UTIL_SCRIPT" $options)

    if [[ "$actual_output" == "$expected_output" ]]; then
        echo "PASSED"
    else
        echo "FAILED"
        echo "  Mock PATH:    '$mock_path'"
        echo "  Expected:     '$expected_output'"
        echo "  Actual:       '$actual_output'"
        return 1
    fi
    return 0
}

# --- Test Cases ---

test_deduplicate_paths() {
    local mock_path="$TEMP_DIR/a:$TEMP_DIR/b:$TEMP_DIR/a:$TEMP_DIR/c"
    local expected_output="$TEMP_DIR/a:$TEMP_DIR/b:$TEMP_DIR/c"
    run_test "Deduplicate paths" "$mock_path" "$expected_output" "--dry-run"
}

test_remove_non_existent_paths() {
    local mock_path="$TEMP_DIR/existing1:$TEMP_DIR/non_existent:$TEMP_DIR/existing2"
    local expected_output="$TEMP_DIR/existing1:$TEMP_DIR/existing2"
    run_test "Remove non-existent paths" "$mock_path" "$expected_output" "--dry-run"
}

test_mixed_duplicates_and_non_existent() {
    local mock_path="$TEMP_DIR/a:$TEMP_DIR/b:$TEMP_DIR/non_existent:$TEMP_DIR/a:$TEMP_DIR/c:$TEMP_DIR/existing1:$TEMP_DIR/another_non_existent"
    local expected_output="$TEMP_DIR/a:$TEMP_DIR/b:$TEMP_DIR/c:$TEMP_DIR/existing1"
    run_test "Mixed duplicates and non-existent" "$mock_path" "$expected_output" "--dry-run"
}

test_no_changes_needed() {
    local mock_path="$TEMP_DIR/a:$TEMP_DIR/b:$TEMP_DIR/c"
    local expected_output="$TEMP_DIR/a:$TEMP_DIR/b:$TEMP_DIR/c"
    run_test "No changes needed" "$mock_path" "$expected_output" "--dry-run"
}

test_empty_path() {
    local mock_path=""
    local expected_output=""
    run_test "Empty PATH" "$mock_path" "$expected_output" "--dry-run"
}

test_path_with_empty_components() {
    local mock_path="$TEMP_DIR/a:::$TEMP_DIR/b:$TEMP_DIR/a"
    local expected_output="$TEMP_DIR/a:$TEMP_DIR/b"
    run_test "PATH with empty components" "$mock_path" "$expected_output" "--dry-run"
}

test_apply_command_output() {
    local mock_path="$TEMP_DIR/a:$TEMP_DIR/b:$TEMP_DIR/a:$TEMP_DIR/non_existent"
    local expected_output="export PATH=\"$TEMP_DIR/a:$TEMP_DIR/b\""
    run_test "Apply command output" "$mock_path" "$expected_output" "--apply"
}

test_dry_run_default() {
    local mock_path="$TEMP_DIR/a:$TEMP_DIR/b:$TEMP_DIR/a"
    local expected_output="$TEMP_DIR/a:$TEMP_DIR/b"
    # No options, should default to dry-run
    actual_output=$(PATH="$mock_path" "$UTIL_SCRIPT")
    if [[ "$actual_output" == "$expected_output" ]]; then
        echo "Running test: Dry-run default... PASSED"
    else
        echo "Running test: Dry-run default... FAILED"
        echo "  Mock PATH:    '$mock_path'"
        echo "  Expected:     '$expected_output'"
        echo "  Actual:       '$actual_output'"
        return 1
    fi
    return 0
}

# --- Main Test Runner ---
main() {
    setup_test_env
    echo "--- Running Nightly PATH Patchwork Organizer Tests ---"
    local failures=0

    test_deduplicate_paths || ((failures++))
    test_remove_non_existent_paths || ((failures++))
    test_mixed_duplicates_and_non_existent || ((failures++))
    test_no_changes_needed || ((failures++))
    test_empty_path || ((failures++))
    test_path_with_empty_components || ((failures++))
    test_apply_command_output || ((failures++))
    test_dry_run_default || ((failures++))

    echo "--- Test Summary ---"
    if [[ "$failures" -eq 0 ]]; then
        echo "All tests PASSED!"
    else
        echo "$failures test(s) FAILED."
        exit 1
    fi
}

main "$@"
