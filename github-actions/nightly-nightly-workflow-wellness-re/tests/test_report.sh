#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Mock rationale: We need to simulate the output of the 'gh' CLI tool
# without actually making network requests or depending on a live GitHub repository.
# This mock function will return predefined JSON data, allowing for deterministic testing.
mock_gh() {
    local cmd="$1"
    local subcmd="$2"
    # We ignore other arguments for simplicity in this mock, as the JSON is fixed.
    # In a more complex test suite, you might parse args to return different data.

    if [[ "$cmd" == "run" && "$subcmd" == "list" ]]; then
        cat <<EOF
[
  {
    "databaseId": 1,
    "name": "Build and Test",
    "status": "completed",
    "conclusion": "success",
    "createdAt": "2023-01-01T10:00:00Z",
    "updatedAt": "2023-01-01T10:05:00Z",
    "url": "https://github.com/owner/repo/actions/runs/1"
  },
  {
    "databaseId": 2,
    "name": "Deploy Production",
    "status": "completed",
    "conclusion": "failure",
    "createdAt": "2023-01-01T11:00:00Z",
    "updatedAt": "2023-01-01T11:15:00Z",
    "url": "https://github.com/owner/repo/actions/runs/2"
  },
  {
    "databaseId": 3,
    "name": "Build and Test",
    "status": "completed",
    "conclusion": "failure",
    "createdAt": "2023-01-01T12:00:00Z",
    "updatedAt": "2023-01-01T12:03:00Z",
    "url": "https://github.com/owner/repo/actions/runs/3"
  },
  {
    "databaseId": 4,
    "name": "Deploy Production",
    "status": "completed",
    "conclusion": "failure",
    "createdAt": "2023-01-01T13:00:00Z",
    "updatedAt": "2023-01-01T13:18:00Z",
    "url": "https://github.com/owner/repo/actions/runs/4"
  },
  {
    "databaseId": 5,
    "name": "Build and Test",
    "status": "completed",
    "conclusion": "success",
    "createdAt": "2023-01-01T14:00:00Z",
    "updatedAt": "2023-01-01T14:04:00Z",
    "url": "https://github.com/owner/repo/actions/runs/5"
  },
  {
    "databaseId": 6,
    "name": "Deploy Production",
    "status": "completed",
    "conclusion": "failure",
    "createdAt": "2023-01-01T15:00:00Z",
    "updatedAt": "2023-01-01T15:20:00Z",
    "url": "https://github.com/owner/repo/actions/runs/6"
  },
  {
    "databaseId": 7,
    "name": "Lint Code",
    "status": "completed",
    "conclusion": "success",
    "createdAt": "2023-01-01T16:00:00Z",
    "updatedAt": "2023-01-01T16:01:00Z",
    "url": "https://github.com/owner/repo/actions/runs/7"
  }
]
EOF
    else
        echo "Error: Mock 'gh' received unexpected command: $@" >&2
        return 1
    fi
}

# Override the 'gh' command with our mock function for testing
export -f gh

# Mock rationale: We need to simulate the 'jq' command being available.
# For this test, we assume 'jq' is installed in the test environment.
# If 'jq' were not guaranteed, we'd mock it similarly to 'gh'.

# Function to run the script and capture its stdout output (excluding ::set-output line)
run_script() {
    local token="$1"
    local repo="$2"
    local max_runs="$3"
    local long_run_threshold="$4"
    local failure_threshold="$5"

    local temp_stdout_file=$(mktemp)

    # Set GH_TOKEN for the script execution and run the script
    # We redirect stdout to a temporary file, then filter out the ::set-output line.
    GH_TOKEN="$token" bash ../src/report.sh "$repo" "$max_runs" "$long_run_threshold" "$failure_threshold" > "$temp_stdout_file" 2>&1
    
    # Read the content, filter out the ::set-output line, and return the rest.
    local script_output=$(grep -v '^::set-output' "$temp_stdout_file")
    rm "$temp_stdout_file"
    echo "$script_output"
}

# Test 1: Default thresholds (long-run > 10m, frequent failure >= 3)
echo "--- Running Test 1: Default thresholds ---"
OUTPUT=$(run_script "mock_token" "owner/repo" "100" "10" "3")

# Assertions for Test 1
# Expected long-running workflows: Deploy Production (15m, 18m, 20m)
if echo "$OUTPUT" | grep -q "Workflow: Deploy Production, Duration: 15m"; then
    echo "Test 1 (Long-Running 15m) PASSED"
else
    echo "Test 1 (Long-Running 15m) FAILED" && exit 1
fi

if echo "$OUTPUT" | grep -q "Workflow: Deploy Production, Duration: 18m"; then
    echo "Test 1 (Long-Running 18m) PASSED"
else
    echo "Test 1 (Long-Running 18m) FAILED" && exit 1
fi

if echo "$OUTPUT" | grep -q "Workflow: Deploy Production, Duration: 20m"; then
    echo "Test 1 (Long-Running 20m) PASSED"
else
    echo "Test 1 (Long-Running 20m) FAILED" && exit 1
fi

# Expected frequent failures: Deploy Production (3 failures)
if echo "$OUTPUT" | grep -q "Workflow: Deploy Production, Failures in last 100 runs: 3"; then
    echo "Test 1 (Frequent Failure Deploy Production) PASSED"
else
    echo "Test 1 (Frequent Failure Deploy Production) FAILED" && exit 1
fi

# Build and Test has 1 failure, should NOT be in frequent failures section
if echo "$OUTPUT" | grep -q "Frequently Failing Workflows.*Build and Test, Failures in last 100 runs: 1"; then
    echo "Test 1 (Build and Test NOT Frequent Failure) FAILED (unexpectedly found)" && exit 1
else
    echo "Test 1 (Build and Test NOT Frequent Failure) PASSED"
fi


# Test 2: Custom thresholds (long-run > 4m, frequent failure >= 4)
echo "--- Running Test 2: Custom thresholds ---"
OUTPUT=$(run_script "mock_token" "owner/repo" "100" "4" "4")

# Assertions for Test 2
# Expected long-running workflows: Build and Test (5m), Deploy Production (15m, 18m, 20m)
if echo "$OUTPUT" | grep -q "Workflow: Build and Test, Duration: 5m"; then
    echo "Test 2 (Long-Running 5m) PASSED"
else
    echo "Test 2 (Long-Running 5m) FAILED" && exit 1
fi

if echo "$OUTPUT" | grep -q "Workflow: Deploy Production, Duration: 15m"; then
    echo "Test 2 (Long-Running 15m) PASSED"
else
    echo "Test 2 (Long-Running 15m) FAILED" && exit 1
fi

# Deploy Production still has 3 failures, should NOT be frequent with threshold 4
if echo "$OUTPUT" | grep -q "Frequently Failing Workflows.*Deploy Production, Failures in last 100 runs: 3"; then
    echo "Test 2 (Deploy Production NOT Frequent Failure) FAILED (unexpectedly found)" && exit 1
else
    echo "Test 2 (Deploy Production NOT Frequent Failure) PASSED"
fi

echo "All tests completed successfully."
