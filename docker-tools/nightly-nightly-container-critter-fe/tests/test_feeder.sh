#!/bin/bash

# Mock rationale: We need to simulate Docker commands without actually running Docker.
# These mocks allow us to control the output of `docker ps`, `docker inspect`, and `docker restart`
# to test different scenarios (running, exited, unhealthy, restart success/failure).

MOCK_CONTAINER_STATE_FILE="/tmp/mock_container_state.txt"
MOCK_CONTAINER_HEALTH_FILE="/tmp/mock_container_health.txt"

# --- MOCK FUNCTIONS ---
docker() {
  local cmd=$1
  shift
  case "$cmd" in
    "ps")
      # Mock rationale: Simulate `docker ps -a --format "{{.Names}}"` output.
      # We'll always return a fixed list of mock containers for auto-discovery tests.
      echo "mock-critter-1"
      echo "mock-critter-2"
      echo "critter-feeder" # Ensure self-exclusion works in auto-discovery
      ;;
    "inspect")
      # Mock rationale: Simulate `docker inspect` output based on predefined state files.
      local format_str=$1
      local container_name=$2
      
      if [ "$container_name" == "critter-feeder" ]; then
        # For the critter-feeder itself, always return running/healthy for self-exclusion check
        case "$format_str" in
          "--format='{{.State.Status}}'") echo "running";; # Mock rationale: Feeder is always running
          "--format='{{.State.Running}}'") echo "true";; # Mock rationale: Feeder is always running
          "--format='{{if .State.Health}}{{.State.Health.Status}}{{else}}n/a{{end}}'") echo "healthy";; # Mock rationale: Feeder is always healthy
          *) echo "Error: Unhandled mock inspect format for self: $format_str" >&2; return 1;;
        esac
        return 0
      fi

      local state=$(grep "^$container_name:" "$MOCK_CONTAINER_STATE_FILE" | cut -d':' -f2)
      local health=$(grep "^$container_name:" "$MOCK_CONTAINER_HEALTH_FILE" | cut -d':' -f2)

      if [ -z "$state" ]; then
        echo "" # Container not found
        return 1
      fi

      case "$format_str" in
        "--format='{{.State.Status}}'")
          echo "$state"
          ;;
        "--format='{{.State.Running}}'")
          if [ "$state" == "running" ]; then echo "true"; else echo "false"; fi
          ;;
        "--format='{{if .State.Health}}{{.State.Health.Status}}{{else}}n/a{{end}}'")
          echo "$health"
          ;;
        *) # Mock rationale: Catch any unexpected inspect formats
          echo "Error: Unhandled mock inspect format: $format_str" >&2
          return 1
          ;;
      esac
      ;;
    "restart")
      # Mock rationale: Simulate `docker restart` success/failure based on container name.
      local container_name=$1
      if [ "$container_name" == "mock-critter-1" ]; then
        # Simulate successful restart for critter-1
        echo "$container_name"
        # Update state to running after restart
        sed -i "s/^$container_name:.*/$container_name:running/" "$MOCK_CONTAINER_STATE_FILE"
        sed -i "s/^$container_name:.*/$container_name:healthy/" "$MOCK_CONTAINER_HEALTH_FILE"
        return 0
      elif [ "$container_name" == "mock-critter-2" ]; then
        # Simulate failed restart for critter-2
        echo "Error: Failed to restart $container_name" >&2
        return 1
      else
        echo "Error: Unhandled mock restart for $container_name" >&2
        return 1
      fi
      ;;
    *) # Mock rationale: Catch any unexpected docker commands
      echo "Error: Unhandled mock docker command: $cmd" >&2
      return 1
      ;;
  esac
}

# --- TEST SETUP ---
setup_test() {
  echo "Setting up test environment..."
  # Initial states for mock containers
  echo "mock-critter-1:exited" > "$MOCK_CONTAINER_STATE_FILE"
  echo "mock-critter-2:running" >> "$MOCK_CONTAINER_STATE_FILE" # This one will be unhealthy
  
  echo "mock-critter-1:n/a" > "$MOCK_CONTAINER_HEALTH_FILE"
  echo "mock-critter-2:unhealthy" >> "$MOCK_CONTAINER_HEALTH_FILE"

  # Source the actual script to make its functions available for testing
  source src/feeder.sh
}

# --- TEST CLEANUP ---
cleanup_test() {
  echo "Cleaning up test environment..."
  rm -f "$MOCK_CONTAINER_STATE_FILE" "$MOCK_CONTAINER_HEALTH_FILE"
  unset -f docker # Unset mock docker function
  unset FEED_INTERVAL CRITTER_NAMES # Clear environment variables
}

# --- TEST CASES ---

test_critter_feeder_explicit_names() {
  echo "--- Running test_critter_feeder_explicit_names (CRITTER_NAMES set) ---"
  setup_test

  # Set environment variables for the script under test
  export CRITTER_NAMES="mock-critter-1 mock-critter-2" # Explicitly monitor these

  # Call the single-round function directly and capture output
  local output=$(perform_single_round 2>&1)
  
  # Check if critter-1 was restarted
  if echo "$output" | grep -q "Successfully fed (restarted) critter 'mock-critter-1'."; then
    echo "PASS: Critter-1 (exited) was successfully restarted."
  else
    echo "FAIL: Critter-1 (exited) was NOT restarted."
    echo "Output: $output"
    cleanup_test
    exit 1
  fi

  # Check if critter-2 (unhealthy) restart was attempted and failed
  if echo "$output" | grep -q "Critter 'mock-critter-2' seems unwell (running, unhealthy). Attempting to feed (restart)..." && \
     echo "$output" | grep -q "Failed to feed (restart) critter 'mock-critter-2'. It might be beyond help."; then
    echo "PASS: Critter-2 (unhealthy) restart was attempted and failed as expected."
  else
    echo "FAIL: Critter-2 (unhealthy) restart scenario failed."
    echo "Output: $output"
    cleanup_test
    exit 1
  fi

  # Verify critter-feeder was not monitored (self-exclusion is not directly tested here as CRITTER_NAMES is set)
  # The `perform_single_round` function's `containers_to_check` variable will only contain the explicitly named critters.
  if echo "$output" | grep -q "critter-feeder' status:"; then
    echo "FAIL: Critter-feeder itself was monitored, which should not happen when CRITTER_NAMES is set."
    echo "Output: $output"
    cleanup_test
    exit 1
  else
    echo "PASS: Critter-feeder was correctly excluded from monitoring (not in CRITTER_NAMES).
"
  fi

  cleanup_test
}

test_critter_feeder_auto_discovery() {
  echo "--- Running test_critter_feeder_auto_discovery (CRITTER_NAMES unset) ---"
  setup_test
  # Unset CRITTER_NAMES to enable auto-discovery
  unset CRITTER_NAMES

  local output=$(perform_single_round 2>&1)

  # Check if critter-1 was restarted
  if echo "$output" | grep -q "Successfully fed (restarted) critter 'mock-critter-1'."; then
    echo "PASS: Auto-discovery: Critter-1 (exited) was successfully restarted."
  else
    echo "FAIL: Auto-discovery: Critter-1 (exited) was NOT restarted."
    echo "Output: $output"
    cleanup_test
    exit 1
  fi

  # Check if critter-2 (unhealthy) restart was attempted and failed
  if echo "$output" | grep -q "Critter 'mock-critter-2' seems unwell (running, unhealthy). Attempting to feed (restart)..." && \
     echo "$output" | grep -q "Failed to feed (restart) critter 'mock-critter-2'. It might be beyond help."; then
    echo "PASS: Auto-discovery: Critter-2 (unhealthy) restart was attempted and failed as expected."
  else
    echo "FAIL: Auto-discovery: Critter-2 (unhealthy) restart scenario failed."
    echo "Output: $output"
    cleanup_test
    exit 1
  fi

  # Verify critter-feeder was not monitored (self-exclusion)
  if echo "$output" | grep -q "critter-feeder' status:"; then
    echo "FAIL: Auto-discovery: Critter-feeder itself was monitored, self-exclusion failed."
    echo "Output: $output"
    cleanup_test
    exit 1
  else
    echo "PASS: Auto-discovery: Critter-feeder was correctly excluded from monitoring."
  fi

  cleanup_test
}


# --- MAIN TEST EXECUTION ---
test_critter_feeder_explicit_names
test_critter_feeder_auto_discovery

echo "All tests completed."
