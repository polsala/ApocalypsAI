#!/bin/bash

# Mock rationale: We need to control the output of 'find' to ensure deterministic tests
# without actually creating files with specific timestamps, which can be tricky
# and non-portable across different file systems or time zones.
# This mock allows us to simulate 'find' behavior precisely.

# Create a temporary directory for mock executables
MOCK_BIN_DIR=$(mktemp -d)
trap "rm -rf $MOCK_BIN_DIR" EXIT # Clean up on exit

# Create a mock 'find' executable
cat << 'EOF' > "$MOCK_BIN_DIR/find"
#!/bin/bash
local_target_dir=""
local_age_days=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        -maxdepth) shift ;;
        -mindepth) shift ;;
        -mtime)
            local_age_days="$2"
            shift
            ;;
        -print0) ;;
        *)
            if [[ -z "$local_target_dir" ]]; then
                local_target_dir="$1"
            fi
            ;;
    esac
    shift
done

# Simulate find output based on age_days
# The paths are generic as the main script just prints them. The mock ensures
# the correct set of 'old' items is returned based on the age threshold.
if [[ "$local_age_days" == "+90" ]]; then
    echo -n "mock_dir/old_file.txt\0"
    echo -n "mock_dir/old_directory\0"
    echo -n "mock_dir/another_old_file.log\0"
elif [[ "$local_age_days" == "+30" ]]; then
    echo -n "mock_dir/recent_old_file.txt\0"
    echo -n "mock_dir/recent_old_directory\0"
elif [[ "$local_age_days" == "+365" ]]; then
    # No output for very old files in this mock scenario
    echo -n ""
else
    # Default mock output if age not specifically handled
    echo -n "mock_dir/default_old_file.txt\0"
fi
EOF
chmod +x "$MOCK_BIN_DIR/find"

# Save original PATH and prepend mock bin directory
OLD_PATH="$PATH"
export PATH="$MOCK_BIN_DIR:$PATH"

# Helper function to run the script and capture output
run_script() {
    bash src/dust_bunny_sweeper.sh "$@"
}

# Test 1: Default behavior (no args, should use default age 90 and current dir)
echo "Running Test 1: Default behavior (age 90 days, current dir)"
OUTPUT=$(run_script)
if echo "$OUTPUT" | grep -q "FILE: \"mock_dir/old_file.txt\"" && \
   echo "$OUTPUT" | grep -q "DIR:  \"mock_dir/old_directory\"" && \
   echo "$OUTPUT" | grep -q "FILE: \"mock_dir/another_old_file.log\"" && \
   ! echo "$OUTPUT" | grep -q "recent_old_file.txt"; then
    echo "Test 1 PASSED"
else
    echo "Test 1 FAILED"
    echo "Output: $OUTPUT"
    exit 1
fi

# Test 2: Custom age (30 days)
echo "Running Test 2: Custom age (30 days)"
OUTPUT=$(run_script -a 30)
if echo "$OUTPUT" | grep -q "FILE: \"mock_dir/recent_old_file.txt\"" && \
   echo "$OUTPUT" | grep -q "DIR:  \"mock_dir/recent_old_directory\"" && \
   ! echo "$OUTPUT" | grep -q "old_file.txt"; then
    echo "Test 2 PASSED"
else
    echo "Test 2 FAILED"
    echo "Output: $OUTPUT"
    exit 1
fi

# Test 3: Custom directory (age 90 days, /tmp/my_dust_heap)
echo "Running Test 3: Custom directory (age 90 days, /tmp/my_dust_heap)"
OUTPUT=$(run_script -d /tmp/my_dust_heap)
if echo "$OUTPUT" | grep -q "Sweeping for digital dust bunnies in '/tmp/my_dust_heap'" && \
   echo "$OUTPUT" | grep -q "FILE: \"mock_dir/old_file.txt\""; then
    echo "Test 3 PASSED"
else
    echo "Test 3 FAILED"
    echo "Output: $OUTPUT"
    exit 1
fi

# Test 4: Invalid age argument
echo "Running Test 4: Invalid age argument"
OUTPUT=$(run_script -a "abc" 2>&1) # Redirect stderr to stdout
if echo "$OUTPUT" | grep -q "Error: Age must be a positive integer."; then
    echo "Test 4 PASSED"
else
    echo "Test 4 FAILED"
    echo "Output: $OUTPUT"
    exit 1
fi

# Test 5: No old files (age 365 days)
echo "Running Test 5: No old files (age 365 days)"
OUTPUT=$(run_script -a 365)
if ! echo "$OUTPUT" | grep -q "FILE:" && \
   ! echo "$OUTPUT" | grep -q "DIR:"; then
    echo "Test 5 PASSED"
else
    echo "Test 5 FAILED"
    echo "Output: $OUTPUT"
    exit 1
fi

echo "All tests completed."

# Restore original PATH
export PATH="$OLD_PATH"
