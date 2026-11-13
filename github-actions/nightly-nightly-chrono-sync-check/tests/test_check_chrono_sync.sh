#!/bin/bash

# Source the script to be tested
SCRIPT_TO_TEST="../src/check_chrono_sync.sh"

# Helper function to run a test case
run_test() {
    local test_name="$1"
    local mock_workflow_epoch="$2"
    local mock_commit_epoch="$3"
    local max_stale_hours="$4"
    local fail_on_stale="$5"
    local fail_on_future="$6"
    local expected_exit_code="$7"
    local expected_is_stale="$8"
    local expected_is_future="$9"
    local expected_output_contains="${10}"

    echo "--- Running Test: $test_name ---"

    # Mock rationale: We're setting environment variables that the script checks
    # instead of calling `date` or `git log`. This makes tests deterministic and offline.
    EPOCH_SECONDS="$mock_workflow_epoch" \
    MOCKED_COMMIT_EPOCH="$mock_commit_epoch" \
    bash "$SCRIPT_TO_TEST" "$max_stale_hours" "$fail_on_stale" "$fail_on_future" > test_output.log 2>&1
    local actual_exit_code=$?
    local output=$(cat test_output.log)

    echo "Actual Exit Code: $actual_exit_code"
    echo "Output:"
    echo "$output"

    # Extract outputs
    local actual_is_stale=$(echo "$output" | grep "::set-output name=is-stale::" | sed -E 's/.*::set-output name=is-stale::(true|false).*/\1/')
    local actual_is_future=$(echo "$output" | grep "::set-output name=is-future::" | sed -E 's/.*::set-output name=is-future::(true|false).*/\1/')

    if [[ "$actual_exit_code" -ne "$expected_exit_code" ]]; then
        echo "FAIL: $test_name - Expected exit code $expected_exit_code, got $actual_exit_code"
        return 1
    fi
    if [[ "$actual_is_stale" != "$expected_is_stale" ]]; then
        echo "FAIL: $test_name - Expected is-stale '$expected_is_stale', got '$actual_is_stale'"
        return 1
    fi
    if [[ "$actual_is_future" != "$expected_is_future" ]]; then
        echo "FAIL: $test_name - Expected is-future '$expected_is_future', got '$actual_is_future'"
        return 1
    fi
    if [[ -n "$expected_output_contains" && ! "$output" =~ "$expected_output_contains" ]]; then
        echo "FAIL: $test_name - Expected output to contain '$expected_output_contains', but it did not."
        return 1
    fi

    echo "PASS: $test_name"
    return 0
}

# --- Test Cases ---

# Test 1: Commit is fresh (within max-stale-hours)
# Workflow: 2023-10-27 10:00:00 UTC (epoch 1698391200)
# Commit:   2023-10-27 09:00:00 UTC (epoch 1698387600) - 1 hour old
run_test "Fresh commit" \
    1698391200 1698387600 \
    24 false true \
    0 false false "Time difference: 3600 seconds (1.00 hours)" || exit 1

# Test 2: Commit is stale, but not failing
# Workflow: 2023-10-27 10:00:00 UTC (epoch 1698391200)
# Commit:   2023-10-26 09:00:00 UTC (epoch 1698304800) - 25 hours old
run_test "Stale commit (warn only)" \
    1698391200 1698304800 \
    24 false true \
    0 true false "Latest commit is stale! It's 24.00 hours old" || exit 1

# Test 3: Commit is stale and failing
# Workflow: 2023-10-27 10:00:00 UTC (epoch 1698391200)
# Commit:   2023-10-26 09:00:00 UTC (epoch 1698304800) - 25 hours old
run_test "Stale commit (fail)" \
    1698391200 1698304800 \
    24 true true \
    1 true false "::error::Commit timestamp is too old" || exit 1

# Test 4: Commit is in the future and failing (default)
# Workflow: 2023-10-27 10:00:00 UTC (epoch 1698391200)
# Commit:   2023-10-27 11:00:00 UTC (epoch 1698394800) - 1 hour in future
run_test "Future commit (fail)" \
    1698391200 1698394800 \
    24 false true \
    1 false true "::error::Commit timestamp is in the future" || exit 1

# Test 5: Commit is in the future, but not failing
# Workflow: 2023-10-27 10:00:00 UTC (epoch 1698391200)
# Commit:   2023-10-27 11:00:00 UTC (epoch 1698394800) - 1 hour in future
run_test "Future commit (warn only)" \
    1698391200 1698394800 \
    24 false false \
    0 false true "Temporal Anomaly Detected! Latest commit is in the future" || exit 1

# Test 6: Edge case - commit exactly max-stale-hours old (should not be stale)
# Workflow: 2023-10-27 10:00:00 UTC (epoch 1698391200)
# Commit:   2023-10-26 10:00:00 UTC (epoch 1698304800) - exactly 24 hours old
run_test "Edge case: Exactly stale limit" \
    1698391200 1698304800 \
    24 false true \
    0 false false "Time difference: 86400 seconds (24.00 hours)" || exit 1

# Test 7: Custom max-stale-hours
# Workflow: 2023-10-27 10:00:00 UTC (epoch 1698391200)
# Commit:   2023-10-27 06:00:00 UTC (epoch 1698376800) - 4 hours old
run_test "Custom max-stale-hours (fresh)" \
    1698391200 1698376800 \
    5 false true \
    0 false false "Time difference: 14400 seconds (4.00 hours)" || exit 1

# Test 8: Custom max-stale-hours (stale)
# Workflow: 2023-10-27 10:00:00 UTC (epoch 1698391200)
# Commit:   2023-10-27 04:00:00 UTC (epoch 1698369600) - 6 hours old
run_test "Custom max-stale-hours (stale)" \
    1698391200 1698369600 \
    5 false true \
    0 true false "Latest commit is stale! It's 6.00 hours old" || exit 1

# Test 9: Commit is exactly 0 hours old (current commit)
# Workflow: 2023-10-27 10:00:00 UTC (epoch 1698391200)
# Commit:   2023-10-27 10:00:00 UTC (epoch 1698391200) - 0 hours old
run_test "Current commit" \
    1698391200 1698391200 \
    24 false true \
    0 false false "Time difference: 0 seconds (0.00 hours)" || exit 1

echo "All tests passed!"
rm test_output.log
