#!/bin/bash

# Load shunit2
. shunit2

# Source the script to be tested
. src/pocket_dimension.sh

# Mock Docker commands
# Mock rationale: To make tests deterministic and offline, we replace actual Docker commands
# with functions that simulate their behavior and record calls, without interacting with the Docker daemon.
# This ensures tests run fast and consistently regardless of the host's Docker state.

MOCKED_DOCKER_CALLS=()
MOCKED_DOCKER_PS_OUTPUT=""
MOCKED_DOCKER_VOLUME_LS_OUTPUT=""

# Override the actual docker command
docker() {
  MOCKED_DOCKER_CALLS+=("$@")
  case "$1" in
    ps)
      if [[ "$@" == "ps -a --format {{.Names}}" ]]; then
        echo "$MOCKED_DOCKER_PS_OUTPUT"
      elif [[ "$@" == "ps --format {{.Names}}" ]]; then
        echo "$MOCKED_DOCKER_PS_OUTPUT" # For simplicity, assume same output for running/all
      elif [[ "$@" == "ps -a --filter name=^pd- --format table {{.Names}}\t{{.Image}}\t{{.Status}}" ]]; then
        # Mock rationale: Provide a fixed output for the 'list' command's specific docker ps call.
        # This ensures the 'list' test is deterministic and doesn't rely on actual Docker state.
        echo "NAMES               IMAGE           STATUS"
        echo "pd-my-test-dim      ubuntu:latest   Up 5 seconds"
        echo "pd-another-dim      alpine:latest   Exited (0) 2 minutes ago"
      else
        echo ""
      fi
      ;;
    volume)
      if [[ "$@" == "volume ls --format {{.Name}}" ]]; then
        echo "$MOCKED_DOCKER_VOLUME_LS_OUTPUT"
      else
        echo ""
      fi
      ;;
    *)
      # Default to success for other commands unless specifically mocked
      ;;
  esac
}

# Setup function for each test
setUp() {
  MOCKED_DOCKER_CALLS=()
  MOCKED_DOCKER_PS_OUTPUT=""
  MOCKED_DOCKER_VOLUME_LS_OUTPUT=""
}

# Test cases

test_create_success() {
  # Mock rationale: Simulate no existing container/volume for successful creation.
  MOCKED_DOCKER_PS_OUTPUT=""
  MOCKED_DOCKER_VOLUME_LS_OUTPUT=""

  cmd_create "my-test-dim" "ubuntu:latest"
  assertEquals "Expected 2 docker calls for create" 2 "${#MOCKED_DOCKER_CALLS[@]}"
  assertEquals "docker volume create pd-my-test-dim-vol" "${MOCKED_DOCKER_CALLS[0]}"
  assertContains "docker run -d --name pd-my-test-dim -v pd-my-test-dim-vol:/data ubuntu:latest tail -f /dev/null" "${MOCKED_DOCKER_CALLS[1]}"
}

test_create_missing_args() {
  # Mock rationale: Test argument validation without Docker interaction.
  assertFalse "create should fail without dimension name" "cmd_create"
  assertFalse "create should fail without image" "cmd_create my-test-dim"
}

test_create_already_exists() {
  # Mock rationale: Simulate an existing container to test error handling.
  MOCKED_DOCKER_PS_OUTPUT="pd-my-existing-dim"
  MOCKED_DOCKER_VOLUME_LS_OUTPUT="pd-my-existing-dim-vol"

  assertFalse "create should fail if dimension already exists" "cmd_create my-existing-dim ubuntu:latest"
  assertEquals "Expected no docker calls if dimension already exists" 0 "${#MOCKED_DOCKER_CALLS[@]}"
}

test_enter_success() {
  # Mock rationale: Simulate a running container for successful entry.
  MOCKED_DOCKER_PS_OUTPUT="pd-my-running-dim"

  cmd_enter "my-running-dim"
  assertEquals "Expected 1 docker call for enter" 1 "${#MOCKED_DOCKER_CALLS[@]}"
  assertContains "docker exec -it pd-my-running-dim bash" "${MOCKED_DOCKER_CALLS[0]}"
}

test_enter_not_running() {
  # Mock rationale: Simulate no running container to test error handling.
  MOCKED_DOCKER_PS_OUTPUT="pd-other-dim" # Not the one we're trying to enter

  assertFalse "enter should fail if dimension not running" "cmd_enter my-non-running-dim"
  assertEquals "Expected no docker calls if dimension not running" 0 "${#MOCKED_DOCKER_CALLS[@]}"
}

test_run_success() {
  # Mock rationale: Simulate a running container for successful command execution.
  MOCKED_DOCKER_PS_OUTPUT="pd-my-running-dim"

  cmd_run "my-running-dim" "ls -la /data"
  assertEquals "Expected 1 docker call for run" 1 "${#MOCKED_DOCKER_CALLS[@]}"
  assertContains "docker exec pd-my-running-dim bash -c ls -la /data" "${MOCKED_DOCKER_CALLS[0]}"
}

test_snapshot_success() {
  # Mock rationale: Simulate an existing container for successful snapshot.
  MOCKED_DOCKER_PS_OUTPUT="pd-my-snap-dim"

  cmd_snapshot "my-snap-dim" "my-snap-dim:v1"
  assertEquals "Expected 1 docker call for snapshot" 1 "${#MOCKED_DOCKER_CALLS[@]}"
  assertEquals "docker commit pd-my-snap-dim my-snap-dim:v1" "${MOCKED_DOCKER_CALLS[0]}"
}

test_list_dimensions() {
  # Mock rationale: The 'docker' function is mocked to return a predefined table for the specific 'list' command's ps call.
  # This test verifies that the `cmd_list` function correctly calls docker and formats the output.
  
  local output=$(cmd_list)
  assertContains "Active Pocket Dimensions:" "$output"
  assertContains "my-test-dim" "$output"
  assertContains "ubuntu:latest" "$output"
  assertContains "Up 5 seconds" "$output"
  assertContains "another-dim" "$output"
  assertContains "alpine:latest" "$output"
  assertContains "Exited (0) 2 minutes ago" "$output"
  assertEquals "Expected 1 docker call for list" 1 "${#MOCKED_DOCKER_CALLS[@]}"
}

test_destroy_success() {
  # Mock rationale: Simulate existing container and volume for successful destruction.
  MOCKED_DOCKER_PS_OUTPUT="pd-my-destroy-dim"
  MOCKED_DOCKER_VOLUME_LS_OUTPUT="pd-my-destroy-dim-vol"

  cmd_destroy "my-destroy-dim"
  assertEquals "Expected 3 docker calls for destroy" 3 "${#MOCKED_DOCKER_CALLS[@]}"
  assertEquals "docker stop pd-my-destroy-dim" "${MOCKED_DOCKER_CALLS[0]}"
  assertEquals "docker rm pd-my-destroy-dim" "${MOCKED_DOCKER_CALLS[1]}"
  assertEquals "docker volume rm pd-my-destroy-dim-vol" "${MOCKED_DOCKER_CALLS[2]}"
}

test_destroy_non_existent() {
  # Mock rationale: Simulate no existing container/volume to test graceful handling.
  MOCKED_DOCKER_PS_OUTPUT=""
  MOCKED_DOCKER_VOLUME_LS_OUTPUT=""

  # Capture stderr to check for warnings
  local stderr_output=$(cmd_destroy my-non-existent-dim 2>&1 >/dev/null)
  assertEquals "Expected 0 docker calls if nothing exists to destroy" 0 "${#MOCKED_DOCKER_CALLS[@]}"
  assertContains "Warning: Dimension 'my-non-existent-dim' (container 'pd-my-non-existent-dim') does not exist." "$stderr_output"
}

test_help_message() {
  # Mock rationale: No Docker interaction needed for help message.
  local output=$(cmd_help)
  assertContains "Usage: pocket-dimension-manager <command> [arguments]" "$output"
  assertContains "Commands:" "$output"
}

test_unknown_command() {
  # Mock rationale: No Docker interaction needed for unknown command.
  assertFalse "unknown command should fail" "pocket-dimension-manager unknown-cmd"
  assertEquals "Expected no docker calls for unknown command" 0 "${#MOCKED_DOCKER_CALLS[@]}"
}

# Run shunit2
. shunit2_test_runner
