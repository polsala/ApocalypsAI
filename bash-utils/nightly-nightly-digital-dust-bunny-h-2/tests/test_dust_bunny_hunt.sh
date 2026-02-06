#!/bin/bash

# Test script for nightly-digital-dust-bunny-hunt

# --- Setup ---
TEST_DIR=$(mktemp -d -t dust-bunny-test-XXXX)
export PATH="$TEST_DIR:$PATH" # Add test dir to PATH for mock commands

# Mock rationale: We need to control the output of 'find' to simulate different file system states
# without actually creating many files or relying on the real filesystem's age. This mock 'find'
# will return predefined paths based on the directory and age requested, ensuring deterministic test results.
cat << 'EOF' > "$TEST_DIR/find"
#!/bin/bash
# Mock find command
dir="$1"
type_flag="$2"
mtime_flag="$3" # This will be like -mtime +90 (based on DEFAULT_AGE_DAYS)

# Simulate files older than 90 days for the default age threshold
if [[ "$dir" == "/tmp/test_env/old_files" ]]; then
    echo "/tmp/test_env/old_files/ancient_log.log"
    echo "/tmp/test_env/old_files/very_old_archive.tar.gz"
    echo "/tmp/test_env/old_files/temp_report.tmp"
elif [[ "$dir" == "/tmp/test_env/new_files" ]]; then
    # No files older than 90 days in this mock directory
    :
elif [[ "$dir" == "/tmp/test_env/mixed_files" ]]; then
    echo "/tmp/test_env/mixed_files/super_old.bak"
    echo "/tmp/test_env/mixed_files/mid_age.txt"
fi
EOF
chmod +x "$TEST_DIR/find"

# Create dummy directories for the script to "scan" (even though find is mocked)
mkdir -p "/tmp/test_env/old_files"
mkdir -p "/tmp/test_env/new_files"
mkdir -p "/tmp/test_env/mixed_files"

# Copy the main script into the test environment
cp "$(dirname "$0")"/../src/dust_bunny_hunt.sh "$TEST_DIR/src/dust_bunny_hunt.sh"

# --- Test Functions ---

run_test() {
    local test_name="$1"
    local expected_output_regex="$2"
    local args=("${@:3}")
    local output
    local exit_code=0

    echo "--- Running Test: $test_name ---"
    output=$("$TEST_DIR/src/dust_bunny_hunt.sh" "${args[@]}" 2>&1)

    if echo "$output" | grep -qE "$expected_output_regex"; then
        echo "PASS: $test_name"
    else
        echo "FAIL: $test_name"
        echo "Expected regex: $expected_output_regex"
        echo "Actual output:\n$output"
        exit_code=1
    fi
    return $exit_code
}

# --- Tests ---

# Test 1: Single directory with old files
run_test "Single directory with old files" \
    "Total ancient digital dust bunnies found: 3" \
    "/tmp/test_env/old_files"

# Test 2: Single directory with no old files
run_test "Single directory with no old files" \
    "No ancient digital dust bunnies found here! ✨" \
    "/tmp/test_env/new_files"

# Test 3: Single directory with mixed files (some old, some new based on mock)
run_test "Single directory with mixed files" \
    "Total ancient digital dust bunnies found: 2" \
    "/tmp/test_env/mixed_files"

# Test 4: Multiple specified directories
run_test "Multiple specified directories" \
    "Total ancient digital dust bunnies found: 5" \
    "/tmp/test_env/old_files" "/tmp/test_env/mixed_files"

# Test 5: Help message display
run_test "Help message display" \
    "Usage: dust_bunny_hunt.sh \[DIRECTORY1\] \[DIRECTORY2\] ..." \
    "--help"

# Test 6: Non-existent directory (should warn and skip)
run_test "Non-existent directory handling" \
    "Warning: Directory '/tmp/non_existent_dir' not found or not a directory. Skipping." \
    "/tmp/non_existent_dir"

# --- Cleanup ---
rm -rf "$TEST_DIR"
rm -rf "/tmp/test_env" # Clean up dummy directories
echo "Cleanup complete."
