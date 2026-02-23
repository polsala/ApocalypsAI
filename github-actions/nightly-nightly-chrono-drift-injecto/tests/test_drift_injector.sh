#!/bin/bash

# Mock rationale: We need to test the script's logic without actually sleeping or relying on true randomness.
# We achieve this by setting MOCK_SLEEP and controlling the environment variables that act as inputs.
# The 'RANDOM_GEN' in the main script uses 'cksum' on a provided seed, making its output deterministic for a given seed.

SCRIPT_PATH="$(dirname "$0")"/../src/drift_injector.sh

# Helper function to run a test case
run_test() {
  local test_name="$1"
  local expected_exit_code="$2"
  local expected_output_regex="$3"
  local min_delay="$4"
  local max_delay="$5"
  local failure_chance="$6"
  local drift_seed="$7"

  echo "--- Test: ${test_name} ---"

  # Reset environment variables for each test
  unset INPUT_MIN_DELAY INPUT_MAX_DELAY INPUT_FAILURE_CHANCE INPUT_DRIFT_SEED

  # Set specific inputs for the test case
  export INPUT_MIN_DELAY="${min_delay}"
  export INPUT_MAX_DELAY="${max_delay}"
  export INPUT_FAILURE_CHANCE="${failure_chance}"
  export INPUT_DRIFT_SEED="${drift_seed}"
  export MOCK_SLEEP=1 # Activate mock sleep

  # Run the script and capture output/exit code
  OUTPUT=$(bash "$SCRIPT_PATH" 2>&1)
  ACTUAL_EXIT_CODE=$?

  # Check exit code
  if [ "$ACTUAL_EXIT_CODE" -ne "$expected_exit_code" ]; then
    echo "Test '${test_name}' FAILED: Expected exit code ${expected_exit_code}, got ${ACTUAL_EXIT_CODE}"
    echo "Output:\n${OUTPUT}"
    exit 1
  fi

  # Check output using regex
  if ! echo "${OUTPUT}" | grep -qE "${expected_output_regex}"; then
    echo "Test '${test_name}' FAILED: Output did not match expected regex"
    echo "Expected regex: ${expected_output_regex}"
    echo "Output:\n${OUTPUT}"
    exit 1
  fi

  echo "Test '${test_name}' PASSED"
  echo ""
}

# Test 1: Default values (min_delay=0, max_delay=5, failure_chance=0)
# Expected: Delay 0s, no failure. (cksum of empty string is 0, so 0 % 6 = 0)
run_test \
  "Default values - no delay, no failure" \
  0 \
  "Calculated delay: 0s.*Temporal flow stable" \
  "" "" "" ""

# Test 2: Specific delay, no failure (deterministic seed)
# Seed '12345' -> cksum 3464197025
# DELAY_RANGE = 10 - 5 = 5
# RANDOM_DELAY_OFFSET = 3464197025 % (5 + 1) = 1
# ACTUAL_DELAY = 5 + 1 = 6
run_test \
  "Specific delay (deterministic seed)" \
  0 \
  "Calculated delay: 6s.*MOCK_SLEEP: Would have slept for 6s.*Temporal flow stable" \
  "5" "10" "0" "12345"

# Test 3: Guaranteed failure (deterministic seed)
# Seed '12345' -> cksum 3464197025
# RANDOM_FAILURE_CHECK = (3464197025 / 100) % 100 = 34641970 % 100 = 70
# 70 < 100 is true, so it should fail.
run_test \
  "Guaranteed failure (deterministic seed)" \
  1 \
  "Injecting temporal anomaly: Workflow step failed due to Chrono-Drift!" \
  "0" "0" "100" "12345"

# Test 4: No failure despite high chance (deterministic seed)
# Seed '12345' -> cksum 3464197025
# RANDOM_FAILURE_CHECK = 70
# 70 < 10 is false, so it should NOT fail.
run_test \
  "No failure despite high chance (deterministic seed)" \
  0 \
  "Temporal flow stable" \
  "0" "0" "10" "12345"

# Test 5: Max delay is less than min delay, should cap delay_range at 0
# DELAY_RANGE = 5 - 10 = -5, capped to 0.
# ACTUAL_DELAY = MIN_DELAY + 0 = 10.
run_test \
  "Max delay < Min delay" \
  0 \
  "Calculated delay: 10s.*MOCK_SLEEP: Would have slept for 10s.*Temporal flow stable" \
  "10" "5" "0" "12345"

# Test 6: Zero delay, zero failure chance, specific seed
# Seed '67890' -> cksum 2643265507
# DELAY_RANGE = 0 - 0 = 0
# RANDOM_DELAY_OFFSET = 2643265507 % (0 + 1) = 0
# ACTUAL_DELAY = 0 + 0 = 0
run_test \
  "Zero delay, zero failure chance" \
  0 \
  "Calculated delay: 0s.*Temporal flow stable" \
  "0" "0" "0" "67890"

# Test 7: Failure chance 0, but seed makes RANDOM_FAILURE_CHECK high (should still not fail)
# Seed '12345' -> RANDOM_FAILURE_CHECK = 70. 70 < 0 is false.
run_test \
  "Failure chance 0, high random check" \
  0 \
  "Temporal flow stable" \
  "0" "0" "0" "12345"

echo "All tests PASSED!"
