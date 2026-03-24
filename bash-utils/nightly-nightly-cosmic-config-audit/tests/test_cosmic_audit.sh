#!/bin/bash

# Automated tests for nightly-cosmic-config-audit

set -euo pipefail

# --- Test Setup ---

TEST_DIR=$(mktemp -d -t cosmic-audit-test-XXXXXXXXXX)
CONFIG_LIST_FILE="$TEST_DIR/test_config_list.txt"
BASELINE_DIR="$TEST_DIR/test_baseline"

# Mock rationale: We need to ensure the script operates on known, controlled files
# and directories for deterministic testing. Using a temporary directory isolates
# the tests from the actual system and allows for easy cleanup. The `sha256sum`
# command is a standard utility and its behavior is predictable, so it's used directly
# against the temporary files rather than being mocked.

# Create dummy config files
TEST_FILE1="$TEST_DIR/dummy_config1.txt"
TEST_FILE2="$TEST_DIR/dummy_config2.txt"
TEST_FILE3="$TEST_DIR/dummy_config3.txt"

# --- Helper Functions ---

cleanup() {
    echo "Cleaning up test directory: $TEST_DIR"
    rm -rf "$TEST_DIR"
}

trap cleanup EXIT

assert_contains() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if ! echo "$actual" | grep -qF "$expected"; then
        echo "FAIL: $message"
        echo "  Expected to contain: '$expected'"
        echo "  Actual output: '$actual'"
        exit 1
    fi
}

assert_not_contains() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if echo "$actual" | grep -qF "$expected"; then
        echo "FAIL: $message"
        echo "  Expected NOT to contain: '$expected'"
        echo "  Actual output: '$actual'"
        exit 1
    fi
}

assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [ "$expected" != "$actual" ]; then
        echo "FAIL: $message"
        echo "  Expected: '$expected'"
        echo "  Actual: '$actual'"
        exit 1
    fi
}

# --- Test Cases ---

echo "Running tests for nightly-cosmic-config-audit..."

# Test 1: Init baseline with new files
echo "Test 1: Initializing baseline..."

echo "content1" > "$TEST_FILE1"
echo "content2" > "$TEST_FILE2"

cat <<EOF > "$CONFIG_LIST_FILE"
$TEST_FILE1
$TEST_FILE2
EOF

# Run init command
OUTPUT=$(bash src/cosmic_audit.sh init "$CONFIG_LIST_FILE" "$BASELINE_DIR" 2>&1)

assert_contains "Initializing baseline in '$BASELINE_DIR'" "$OUTPUT" "Init output should confirm baseline directory"
assert_contains "Done. Baseline saved to '$BASELINE_DIR/dummy_config1.txt.sha256'" "$OUTPUT" "Init should save baseline for file1"
assert_contains "Done. Baseline saved to '$BASELINE_DIR/dummy_config2.txt.sha256'" "$OUTPUT" "Init should save baseline for file2"

# Verify baseline files exist and contain correct checksums
if [ ! -f "$BASELINE_DIR/dummy_config1.txt.sha256" ] || [ ! -f "$BASELINE_DIR/dummy_config2.txt.sha256" ]; then
    echo "FAIL: Baseline files not created."
    exit 1
fi

EXPECTED_SHA1=$(sha256sum "$TEST_FILE1" | awk '{print $1}')
ACTUAL_SHA1=$(cat "$BASELINE_DIR/dummy_config1.txt.sha256")
assert_equals "$EXPECTED_SHA1" "$ACTUAL_SHA1" "Baseline checksum for file1 should be correct"

EXPECTED_SHA2=$(sha256sum "$TEST_FILE2" | awk '{print $1}')
ACTUAL_SHA2=$(cat "$BASELINE_DIR/dummy_config2.txt.sha256")
assert_equals "$EXPECTED_SHA2" "$ACTUAL_SHA2" "Baseline checksum for file2 should be correct"

echo "Test 1 Passed."

# Test 2: Audit with no changes
echo "Test 2: Auditing with no changes..."
OUTPUT=$(bash src/cosmic_audit.sh audit "$CONFIG_LIST_FILE" "$BASELINE_DIR" 2>&1)

assert_contains "Auditing '$TEST_FILE1'... OK" "$OUTPUT" "Audit should report OK for file1"
assert_contains "Auditing '$TEST_FILE2'... OK" "$OUTPUT" "Audit should report OK for file2"
assert_contains "Audit complete." "$OUTPUT" "Audit should complete"

# Check exit code for no changes
bash src/cosmic_audit.sh audit "$CONFIG_LIST_FILE" "$BASELINE_DIR" > /dev/null 2>&1
assert_equals "0" "$?" "Audit with no changes should exit with 0"

echo "Test 2 Passed."

# Test 3: Audit with a changed file
echo "Test 3: Auditing with a changed file..."
echo "new content1" > "$TEST_FILE1" # Modify file1

OUTPUT=$(bash src/cosmic_audit.sh audit "$CONFIG_LIST_FILE" "$BASELINE_DIR" 2>&1)

assert_contains "Auditing '$TEST_FILE1'... CHANGED" "$OUTPUT" "Audit should report CHANGED for file1"
assert_contains "Auditing '$TEST_FILE2'... OK" "$OUTPUT" "Audit should report OK for file2"

# Check exit code for changes
bash src/cosmic_audit.sh audit "$CONFIG_LIST_FILE" "$BASELINE_DIR" > /dev/null 2>&1
assert_equals "1" "$?" "Audit with changes should exit with 1"

echo "Test 3 Passed."

# Test 4: Audit with a new file (no baseline)
echo "Test 4: Auditing with a new file (no baseline)..."
echo "content3" > "$TEST_FILE3"
cat <<EOF > "$CONFIG_LIST_FILE"
$TEST_FILE1
$TEST_FILE2
$TEST_FILE3
EOF

OUTPUT=$(bash src/cosmic_audit.sh audit "$CONFIG_LIST_FILE" "$BASELINE_DIR" 2>&1)

assert_contains "Auditing '$TEST_FILE3'... NO BASELINE" "$OUTPUT" "Audit should report NO BASELINE for new file"

# Check exit code for no baseline
bash src/cosmic_audit.sh audit "$CONFIG_LIST_FILE" "$BASELINE_DIR" > /dev/null 2>&1
assert_equals "1" "$?" "Audit with no baseline should exit with 1"

echo "Test 4 Passed."

# Test 5: Audit with a file removed from system
echo "Test 5: Auditing with a file removed from system..."
rm "$TEST_FILE1"

OUTPUT=$(bash src/cosmic_audit.sh audit "$CONFIG_LIST_FILE" "$BASELINE_DIR" 2>&1)

assert_contains "Auditing '$TEST_FILE1'... FILE NOT FOUND" "$OUTPUT" "Audit should report FILE NOT FOUND for removed file"

# Check exit code for file not found
bash src/cosmic_audit.sh audit "$CONFIG_LIST_FILE" "$BASELINE_DIR" > /dev/null 2>&1
assert_equals "1" "$?" "Audit with file not found should exit with 1"

echo "Test 5 Passed."

# Test 6: Init with non-existent config list
echo "Test 6: Init with non-existent config list..."
rm "$CONFIG_LIST_FILE"
OUTPUT=$(bash src/cosmic_audit.sh init "$CONFIG_LIST_FILE" "$BASELINE_DIR" 2>&1 || true)
assert_contains "Error: Configuration file list not found at '$CONFIG_LIST_FILE'" "$OUTPUT" "Init should error if config list not found"
assert_equals "1" "$?" "Init with non-existent config list should exit with 1"
echo "Test 6 Passed."

# Test 7: Audit with non-existent config list
echo "Test 7: Audit with non-existent config list..."
OUTPUT=$(bash src/cosmic_audit.sh audit "$CONFIG_LIST_FILE" "$BASELINE_DIR" 2>&1 || true)
assert_contains "Error: Configuration file list not found at '$CONFIG_LIST_FILE'" "$OUTPUT" "Audit should error if config list not found"
assert_equals "1" "$?" "Audit with non-existent config list should exit with 1"
echo "Test 7 Passed."

# Test 8: Audit with non-existent baseline directory
echo "Test 8: Audit with non-existent baseline directory..."
rm -rf "$BASELINE_DIR"
OUTPUT=$(bash src/cosmic_audit.sh audit "$CONFIG_LIST_FILE" "$BASELINE_DIR" 2>&1 || true)
assert_contains "Error: Baseline directory not found at '$BASELINE_DIR'. Please run 'init' first." "$OUTPUT" "Audit should error if baseline dir not found"
assert_equals "1" "$?" "Audit with non-existent baseline dir should exit with 1"
echo "Test 8 Passed."

echo "All tests passed!"
