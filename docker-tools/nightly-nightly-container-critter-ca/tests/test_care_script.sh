#!/bin/bash

# Mock rationale: We need to test the script's logic without actually interacting
# with a live Docker daemon. Mocking `docker` commands allows us to simulate
# different Docker states (running, stopped, not found) and verify the script's
# output and behavior.

# Source the script to test
. src/care_script.sh

# --- Mock Docker commands ---
MOCKED_DOCKER_PS_OUTPUT=""
MOCKED_DOCKER_RESTART_SUCCESS=0
MOCKED_DOCKER_PRUNE_SUCCESS=0

docker() {
  local cmd=$1
  shift
  case "$cmd" in
    "ps")
      echo "$MOCKED_DOCKER_PS_OUTPUT"
      ;;
    "restart")
      if [ "$MOCKED_DOCKER_RESTART_SUCCESS" -eq 0 ]; then
        echo "Container $1 restarted"
        return 0
      else
        echo "Error restarting container $1" >&2
        return 1
      fi
      ;;
    "system")
      local subcmd=$1
      shift
      if [ "$subcmd" = "prune" ]; then
        if [ "$MOCKED_DOCKER_PRUNE_SUCCESS" -eq 0 ]; then
          echo "Total reclaimed space: 100MB"
          return 0
        else
          echo "Error pruning system" >&2
          return 1
        fi
      fi
      ;;
    *)
      echo "Unknown docker command: $cmd" >&2
      return 1
      ;;
  esac
}

# --- Test Helper Functions ---
assert_contains() {
  local expected="$1"
  local actual="$2"
  if [[ "$actual" == *"$expected"* ]]; then
    echo "PASS: Output contains '$expected'"
  else
    echo "FAIL: Output does not contain '$expected'. Actual: '$actual'"
    exit 1
  fi
}

assert_not_contains() {
  local expected="$1"
  local actual="$2"
  if [[ "$actual" != *"$expected"* ]]; then
    echo "PASS: Output does not contain '$expected'"
  else
    echo "FAIL: Output contains '$expected'. Actual: '$actual'"
    exit 1
  fi
}

# --- Test Cases ---

# Test 1: Health check with no pet containers
test_no_pet_containers() {
  echo "--- Running Test: No Pet Containers ---"
  PET_CONTAINERS=""
  PRUNE_ENABLED="false" # Disable prune for this test
  REFRESH_ENABLED="false"
  output=$(main 2>&1)
  assert_contains "No PET_CONTAINERS specified for health check." "$output"
  assert_not_contains "Critter" "$output"
  assert_contains "Pruning is disabled." "$output"
  echo ""
}

# Test 2: Health check with healthy containers
test_healthy_containers() {
  echo "--- Running Test: Healthy Containers ---"
  PET_CONTAINERS="my_app,my_db"
  PRUNE_ENABLED="false"
  REFRESH_ENABLED="false"
  MOCKED_DOCKER_PS_OUTPUT="Up 5 hours (healthy)\nUp 2 days" # Mock output for 'my_app' and 'my_db'
  output=$(main 2>&1)
  assert_contains "Critter 'my_app' is healthy: Up 5 hours (healthy)" "$output"
  assert_contains "Critter 'my_db' is healthy: Up 2 days" "$output"
  assert_contains "Pruning is disabled." "$output"
  echo ""
}

# Test 3: Health check with unwell container and refresh disabled
test_unwell_no_refresh() {
  echo "--- Running Test: Unwell Container (Refresh Disabled) ---"
  PET_CONTAINERS="unwell_app"
  PRUNE_ENABLED="false"
  REFRESH_ENABLED="false"
  MOCKED_DOCKER_PS_OUTPUT="Exited (1) 2 minutes ago" # Mock output for 'unwell_app'
  output=$(main 2>&1)
  assert_contains "Critter 'unwell_app' is unwell: Exited (1) 2 minutes ago" "$output"
  assert_not_contains "Attempting to refresh" "$output"
  assert_contains "Pruning is disabled." "$output"
  echo ""
}

# Test 4: Health check with unwell container and refresh enabled (success)
test_unwell_with_refresh_success() {
  echo "--- Running Test: Unwell Container (Refresh Enabled, Success) ---"
  PET_CONTAINERS="unwell_app"
  PRUNE_ENABLED="false"
  REFRESH_ENABLED="true"
  MOCKED_DOCKER_PS_OUTPUT="Exited (1) 2 minutes ago"
  MOCKED_DOCKER_RESTART_SUCCESS=0 # Simulate successful restart
  output=$(main 2>&1)
  assert_contains "Critter 'unwell_app' is unwell: Exited (1) 2 minutes ago" "$output"
  assert_contains "Attempting to refresh unwell critter 'unwell_app'..." "$output"
  assert_contains "Critter 'unwell_app' refreshed successfully." "$output"
  assert_contains "Pruning is disabled." "$output"
  echo ""
}

# Test 5: Health check with unwell container and refresh enabled (failure)
test_unwell_with_refresh_failure() {
  echo "--- Running Test: Unwell Container (Refresh Enabled, Failure) ---"
  PET_CONTAINERS="unwell_app"
  PRUNE_ENABLED="false"
  REFRESH_ENABLED="true"
  MOCKED_DOCKER_PS_OUTPUT="Exited (1) 2 minutes ago"
  MOCKED_DOCKER_RESTART_SUCCESS=1 # Simulate failed restart
  output=$(main 2>&1)
  assert_contains "Critter 'unwell_app' is unwell: Exited (1) 2 minutes ago" "$output"
  assert_contains "Attempting to refresh unwell critter 'unwell_app'..." "$output"
  assert_contains "Failed to refresh critter 'unwell_app'." "$output"
  assert_contains "Pruning is disabled." "$output"
  echo ""
}

# Test 6: Pruning enabled
test_pruning_enabled() {
  echo "--- Running Test: Pruning Enabled ---"
  PET_CONTAINERS="" # No pets for this test
  PRUNE_ENABLED="true"
  REFRESH_ENABLED="false"
  MOCKED_DOCKER_PRUNE_SUCCESS=0 # Simulate successful prune
  output=$(main 2>&1)
  assert_contains "Grooming the Docker environment (pruning unused images, volumes, networks)..." "$output"
  assert_contains "Grooming complete." "$output"
  echo ""
}

# Test 7: Pruning disabled
test_pruning_disabled() {
  echo "--- Running Test: Pruning Disabled ---"
  PET_CONTAINERS=""
  PRUNE_ENABLED="false"
  REFRESH_ENABLED="false"
  output=$(main 2>&1)
  assert_contains "Pruning is disabled." "$output"
  assert_not_contains "Grooming the Docker environment" "$output"
  echo ""
}

# Test 8: Container not found
test_container_not_found() {
  echo "--- Running Test: Container Not Found ---"
  PET_CONTAINERS="non_existent_critter"
  PRUNE_ENABLED="false"
  REFRESH_ENABLED="false"
  MOCKED_DOCKER_PS_OUTPUT="" # Simulate container not found
  output=$(main 2>&1)
  assert_contains "Critter 'non_existent_critter' not found." "$output"
  echo ""
}

# Run all tests
test_no_pet_containers
test_healthy_containers
test_unwell_no_refresh
test_unwell_with_refresh_success
test_unwell_with_refresh_failure
test_pruning_enabled
test_pruning_disabled
test_container_not_found

echo "All tests completed."
