#!/bin/bash

# Mock rationale: We need to simulate different Docker daemon states and container uptimes
# without actually running Docker containers or requiring a live Docker daemon.
# This allows for deterministic and offline testing of the monitor.sh script's logic.

# Define a mock docker function
mock_docker_cmd() {
    local subcommand=$1
    shift
    case "$subcommand" in
        "info")
            if [ "$MOCK_DOCKER_INFO_FAIL" = "true" ]; then
                return 1 # Simulate failure
            fi
            echo "Client:"
            echo " Server:"
            ;;
        "ps")
            echo -e "$MOCK_DOCKER_PS_OUTPUT"
            ;;
        *)
            echo "Error: Unknown docker subcommand '$subcommand' in mock." >&2
            exit 1
            ;;
    esac
}
export -f mock_docker_cmd # Export the function so it's available in subshells

# Function to run monitor.sh with mocked environment variables and docker command
run_monitor_with_mock() {
    local mock_ps_output="$1"
    local recent_threshold_minutes="${2:-5}"
    local long_running_threshold_days="${3:-30}"
    local mock_docker_info_fail="${4:-false}"

    # Run monitor.sh in a subshell with mocked environment
    ( # Start subshell
        export RECENT_START_THRESHOLD_MINUTES="$recent_threshold_minutes"
        export LONG_RUNNING_THRESHOLD_DAYS="$long_running_threshold_days"
        export MOCK_DOCKER_PS_OUTPUT="$mock_ps_output"
        export MOCK_DOCKER_INFO_FAIL="$mock_docker_info_fail"
        # Alias docker to our mock function within this subshell
        alias docker='mock_docker_cmd'
        # Execute the actual script
        bash src/monitor.sh
    ) 2>&1 # Capture both stdout and stderr from the subshell
}

# --- Test Cases ---

# Test 1: No containers running
echo "--- Running Test Case 1: No containers ---"
output=$(run_monitor_with_mock "")
if ! echo "$output" | grep -q "ANOMALY" && ! echo "$output" | grep -q "NORMAL"; then
    echo "Test 1 PASSED: Correctly handled no containers (no anomaly/normal reports)."
else
    echo "Test 1 FAILED: Unexpected output for no containers."
    echo "$output"
    exit 1
fi
echo ""

# Test 2: Container recently started
echo "--- Running Test Case 2: Recently started container ---"
output=$(run_monitor_with_mock "my-app\tUp 3 minutes" 5 1)
if echo "$output" | grep -q "ANOMALY: Container 'my-app' has recently started. Uptime: 3 minutes"; then
    echo "Test 2 PASSED: Detected recently started container."
else
    echo "Test 2 FAILED: Did not detect recently started container."
    echo "$output"
    exit 1
fi
echo ""

# Test 3: Container excessively long-running
echo "--- Running Test Case 3: Long-running container ---"
output=$(run_monitor_with_mock "old-service\tUp 40 days" 5 30)
if echo "$output" | grep -q "ANOMALY: Container 'old-service' is excessively long-running. Uptime: 40 days"; then
    echo "Test 3 PASSED: Detected long-running container."
else
    echo "Test 3 FAILED: Did not detect long-running container."
    echo "$output"
    exit 1
fi
echo ""

# Test 4: Normal running container
echo "--- Running Test Case 4: Normal running container ---"
output=$(run_monitor_with_mock "stable-db\tUp 10 days" 5 30)
if echo "$output" | grep -q "NORMAL: Container 'stable-db' is stable. Uptime: 10 days"; then
    echo "Test 4 PASSED: Detected normal running container."
else
    echo "Test 4 FAILED: Did not detect normal running container."
    echo "$output"
    exit 1
fi
echo ""

# Test 5: Mixed containers
echo "--- Running Test Case 5: Mixed containers ---"
MOCK_PS_OUTPUT="recent-web\tUp 1 minute\nold-cache\tUp 50 days\napi-gateway\tUp 12 hours"
output=$(run_monitor_with_mock "$MOCK_PS_OUTPUT" 10 40)
if echo "$output" | grep -q "ANOMALY: Container 'recent-web' has recently started. Uptime: 1 minute" && \
   echo "$output" | grep -q "ANOMALY: Container 'old-cache' is excessively long-running. Uptime: 50 days" && \
   echo "$output" | grep -q "NORMAL: Container 'api-gateway' is stable. Uptime: 12 hours"; then
    echo "Test 5 PASSED: Correctly handled mixed container states."
else
    echo "Test 5 FAILED: Did not correctly handle mixed container states."
    echo "$output"
    exit 1
fi
echo ""

# Test 6: Different time units (seconds, hours)
echo "--- Running Test Case 6: Different time units ---"
MOCK_PS_OUTPUT="quick-job\tUp 30 seconds\nhourly-task\tUp 2 hours"
output=$(run_monitor_with_mock "$MOCK_PS_OUTPUT" 1 1)
if echo "$output" | grep -q "ANOMALY: Container 'quick-job' has recently started. Uptime: 30 seconds" && \
   echo "$output" | grep -q "NORMAL: Container 'hourly-task' is stable. Uptime: 2 hours"; then
    echo "Test 6 PASSED: Correctly handled seconds and hours."
else
    echo "Test 6 FAILED: Did not correctly handle seconds and hours."
    echo "$output"
    exit 1
fi
echo ""

# Test 7: Docker daemon not accessible (mock docker info failure)
echo "--- Running Test Case 7: Docker daemon not accessible ---"
output=$(run_monitor_with_mock "" 5 30 true) # Pass true for mock_docker_info_fail
if echo "$output" | grep -q "ERROR: Docker daemon not accessible. Ensure /var/run/docker.sock is mounted correctly."; then
    echo "Test 7 PASSED: Correctly reported Docker daemon not accessible."
else
    echo "Test 7 FAILED: Did not report Docker daemon not accessible."
    echo "$output"
    exit 1
fi
echo ""

echo "All tests completed."
