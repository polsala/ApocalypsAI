#!/usr/bin/env bash

# test_disk_guardian.sh - tests for disk_guardian.sh

set -e

run_test() {
    local mock_output="$1"
    local expected_exit="$2"
    local expected_pattern="$3"

    # Create a temporary wrapper that defines a mock df function and runs the utility
    cat > /tmp/run_wrapper.sh <<'EOF'
#!/usr/bin/env bash
# Mock df to emit predetermined output
df() {
    echo "$MOCK_DF_OUTPUT"
}
export -f df
# Execute the utility with the optional threshold argument
bash "$(dirname "$0")/../src/disk_guardian.sh" "$THRESHOLD"
EOF
    chmod +x /tmp/run_wrapper.sh

    # Run the wrapper with the mock data
    MOCK_DF_OUTPUT="$mock_output" THRESHOLD=80 /tmp/run_wrapper.sh >output.txt 2>&1
    EXIT_CODE=$?
    if [[ "$EXIT_CODE" -ne "$expected_exit" ]]; then
        echo "FAIL: Expected exit $expected_exit, got $EXIT_CODE"
        cat output.txt
        exit 1
    fi
    if ! grep -q "$expected_pattern" output.txt; then
        echo "FAIL: Output does not contain expected pattern"
        cat output.txt
        exit 1
    fi
    echo "PASS"
}

# Test case 1: usage below threshold (should exit 0 and contain [OK])
run_test "Filesystem     1K-blocks    Used Available Use% Mounted on\n/dev/root       1000000  400000  600000  40% /" 0 "\\[OK\\]"

# Test case 2: usage above threshold (should exit 1 and contain [WARN])
run_test "Filesystem     1K-blocks    Used Available Use% Mounted on\n/dev/root       1000000  850000  150000  85% /" 1 "\\[WARN\\]"

echo "All tests passed."
