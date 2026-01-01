#!/bin/sh

# Automated tests for nightly-container-pet-sitter

# Mock rationale: These tests are designed to be deterministic and offline.
# They mock the 'docker' command to simulate various container states and outputs
# without requiring a live Docker daemon or actual containers.

# --- Test Setup ---

# Create a temporary directory for test logs
TEST_LOG_DIR=$(mktemp -d)
TEST_LOG_FILE="$TEST_LOG_DIR/pet_sitter_test.log"

# Mock docker command
mock_docker_calls=()
mock_docker() {
  mock_docker_calls+=("$@")
  case "$1" in
    "inspect")
      # Mock rationale: Simulate docker inspect output for different container states.
      # The -f '{{.ID}} {{.State.Status}}' format is expected.
      container_name="$3"
      case "$container_name" in
        "running-pet")
          echo "mock_id_running running"
          ;;
        "exited-pet")
          echo "mock_id_exited exited"
          ;;
        "paused-pet")
          echo "mock_id_paused paused"
          ;;
        "nonexistent-pet")
          return 1 # Simulate container not found
          ;;
        *)
          echo "mock_id_unknown unknown"
          ;;
      esac
      ;;
    "stats")
      # Mock rationale: Simulate docker stats output for resource usage.
      # The --format "{{.CPUPerc}}\t{{.MemUsage}}" is expected.
      echo "0.50%\t128MiB / 1.952GiB"
      ;;
    "start")
      # Mock rationale: Simulate docker start command. Just return success.
      echo "Container started: $2"
      ;;
    *)
      echo "Mock docker received unknown command: $@" >&2
      return 1
      ;;
  esac
}

# Override the docker command with our mock function
docker() {
  mock_docker "$@"
}

# --- Test Cases ---

run_test() {
  test_name="$1"
  expected_output_regex="$2"
  shift 2
  test_args="$@"

  echo "\n--- Running Test: $test_name ---"
  mock_docker_calls=() # Reset mock calls for each test
  
  # Run the pet_sitter.sh script in a subshell with a short interval
  # and redirect its output to a temporary log file.
  # We use 'timeout' to ensure the script doesn't run indefinitely in test.
  ( 
    export PET_CONTAINERS="$test_args"
    export RESTART_ON_STOP="${RESTART_ON_STOP:-false}"
    export CHECK_INTERVAL_SECONDS="1"
    timeout 3s sh src/pet_sitter.sh > "$TEST_LOG_FILE" 2>&1
  ) || true # Allow timeout to exit gracefully without failing the test script

  if grep -Eq "$expected_output_regex" "$TEST_LOG_FILE"; then
    echo "PASS: $test_name"
  else
    echo "FAIL: $test_name"
    echo "Expected regex: '$expected_output_regex'"
    echo "Actual output (from $TEST_LOG_FILE):"
    cat "$TEST_LOG_FILE"
    echo "Mock Docker Calls: ${mock_docker_calls[@]}"
    exit 1
  fi
}

# Test 1: No PET_CONTAINERS set
run_test "No PET_CONTAINERS" "ERROR: PET_CONTAINERS environment variable is not set." ""

# Test 2: Running container, no restart needed
RESTART_ON_STOP="false" run_test "Running container (no restart)" "Pet 'running-pet' is happily purring.*CPU: 0.50%, Mem: 128MiB / 1.952GiB" "running-pet"

# Test 3: Exited container, auto-restart disabled
RESTART_ON_STOP="false" run_test "Exited container (auto-restart disabled)" "Pet 'exited-pet' found sleeping.\n  Auto-restart is disabled for 'exited-pet'. It remains asleep." "exited-pet"

# Test 4: Exited container, auto-restart enabled
RESTART_ON_STOP="true" run_test "Exited container (auto-restart enabled)" "Pet 'exited-pet' found sleeping.\n  Attempting to wake up 'exited-pet'...\n  Successfully woke up 'exited-pet'. It's now running." "exited-pet"

# Test 5: Paused container
RESTART_ON_STOP="false" run_test "Paused container" "Pet 'paused-pet' is paused. Consider unpausing it." "paused-pet"

# Test 6: Non-existent container
RESTART_ON_STOP="false" run_test "Non-existent container" "WARNING: Pet 'nonexistent-pet' not found or Docker daemon inaccessible. Skipping." "nonexistent-pet"

# Test 7: Multiple containers, mixed states
RESTART_ON_STOP="true" run_test "Multiple containers, mixed states" \
  "Pet 'running-pet' is happily purring.*Pet 'exited-pet' found sleeping.*Successfully woke up 'exited-pet'.*Pet 'nonexistent-pet' not found" \
  "running-pet,exited-pet,nonexistent-pet"

# --- Test Teardown ---

# Clean up temporary log directory
rm -rf "$TEST_LOG_DIR"

echo "\nAll tests completed."
