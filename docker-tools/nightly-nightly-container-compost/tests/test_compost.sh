#!/bin/bash

# Test script for compost.sh

# Set up a temporary directory for mock files
TEST_DIR=$(mktemp -d)
export TEST_DIR

# Mock rationale: We cannot run actual Docker commands in a CI/CD environment or for deterministic tests.
# We need to control the output of 'docker' commands to simulate different scenarios (e.g., no stale items, items to prune).
# This mock function replaces the actual 'docker' command used by compost.sh.

mock_docker_cmd() {
  local subcommand="$1"
  shift
  local args="$@"

  case "$subcommand" in
    ps)
      if [[ "$args" == *"--filter status=exited --filter until=24h"* ]]; then
        cat "${TEST_DIR}/mock_docker_ps_stale.txt"
      elif [[ "$args" == *"--filter status=exited --filter until=72h"* ]]; then
        cat "${TEST_DIR}/mock_docker_ps_stale_72h.txt"
      else
        cat "${TEST_DIR}/mock_docker_ps_all.txt"
      fi
      ;;
    images)
      if [[ "$args" == *"-f dangling=true"* ]]; then
        cat "${TEST_DIR}/mock_docker_images_dangling.txt"
      else
        cat "${TEST_DIR}/mock_docker_images_all.txt"
      fi
      ;;
    volume)
      if [[ "$args" == *"ls -f dangling=true"* ]]; then
        cat "${TEST_DIR}/mock_docker_volumes_dangling.txt"
      else
        cat "${TEST_DIR}/mock_docker_volumes_all.txt"
      fi
      ;;
    container|image|volume|builder)
      # For prune commands, just echo what would be run
      echo "MOCK: ${subcommand} ${args}"
      ;;
    *)
      echo "MOCK: Unknown docker command: ${subcommand} ${args}" >&2
      return 1
      ;;
  esac
}

# Override the docker_cmd variable in compost.sh for testing
export docker_cmd="mock_docker_cmd"

# Helper function to run compost.sh with specific arguments and capture output
run_compost_script() {
  bash src/compost.sh "$@"
}

# --- Test Cases ---

# Test 1: Dry run with no stale items
echo "Running Test 1: Dry run with no stale items..."

# Mock data for no stale items
cat > "${TEST_DIR}/mock_docker_ps_stale.txt" << EOF

EOF
cat > "${TEST_DIR}/mock_docker_ps_stale_72h.txt" << EOF

EOF
cat > "${TEST_DIR}/mock_docker_images_dangling.txt" << EOF

EOF
cat > "${TEST_DIR}/mock_docker_volumes_dangling.txt" << EOF

EOF
cat > "${TEST_DIR}/mock_docker_ps_all.txt" << EOF
CONTAINER ID   IMAGE     COMMAND    CREATED   STATUS    PORTS     NAMES
EOF
cat > "${TEST_DIR}/mock_docker_images_all.txt" << EOF
REPOSITORY   TAG       IMAGE ID   CREATED   SIZE
EOF
cat > "${TEST_DIR}/mock_docker_volumes_all.txt" << EOF
DRIVER    VOLUME NAME
EOF

OUTPUT=$(run_compost_script --dry-run)

if echo "$OUTPUT" | grep -q "No stale exited containers found." && \
   echo "$OUTPUT" | grep -q "No dangling images found." && \
   echo "$OUTPUT" | grep -q "No dangling volumes found." && \
   echo "$OUTPUT" | grep -q "*** DRY RUN MODE ENABLED ***" && \
   echo "$OUTPUT" | grep -q "Dry run complete."; then
  echo "Test 1 PASSED"
else
  echo "Test 1 FAILED"
  echo "Output:" "$OUTPUT"
  exit 1
fi

# Test 2: Dry run with stale items
echo "Running Test 2: Dry run with stale items..."

# Mock data for stale items
cat > "${TEST_DIR}/mock_docker_ps_stale.txt" << EOF
CONTAINER ID   NAMES          STATUS                        CREATED
1a2b3c4d5e6f   old_container  Exited (0) 2 days ago         2 days ago
EOF
cat > "${TEST_DIR}/mock_docker_ps_stale_72h.txt" << EOF

EOF
cat > "${TEST_DIR}/mock_docker_images_dangling.txt" << EOF
IMAGE ID       REPOSITORY   TAG       SIZE
fedcba987654   <none>       <none>    100MB
EOF
cat > "${TEST_DIR}/mock_docker_volumes_dangling.txt" << EOF
NAME           DRIVER
dangling_vol   local
EOF

OUTPUT=$(run_compost_script --dry-run)

if echo "$OUTPUT" | grep -q "old_container" && \
   echo "$OUTPUT" | grep -q "fedcba987654" && \
   echo "$OUTPUT" | grep -q "dangling_vol" && \
   echo "$OUTPUT" | grep -q "*** DRY RUN MODE ENABLED ***" && \
   echo "$OUTPUT" | grep -q "Dry run complete."; then
  echo "Test 2 PASSED"
else
  echo "Test 2 FAILED"
  echo "Output:" "$OUTPUT"
  exit 1
fi

# Test 3: Live run with stale items (check prune commands are 'mocked' to be called)
echo "Running Test 3: Live run with stale items..."

OUTPUT=$(run_compost_script)

if echo "$OUTPUT" | grep -q "MOCK: container prune -f --filter \"until=24h\"" && \
   echo "$OUTPUT" | grep -q "MOCK: image prune -f" && \
   echo "$OUTPUT" | grep -q "MOCK: volume prune -f" && \
   echo "$OUTPUT" | grep -q "MOCK: builder prune -f" && \
   echo "$OUTPUT" | grep -q "*** LIVE COMPOSTING MODE ***"; then
  echo "Test 3 PASSED"
else
  echo "Test 3 FAILED"
  echo "Output:" "$OUTPUT"
  exit 1
fi

# Test 4: Live run with custom container age
echo "Running Test 4: Live run with custom container age (72 hours)..."

OUTPUT=$(run_compost_script --container-age-hours 72)

if echo "$OUTPUT" | grep -q "MOCK: container prune -f --filter \"until=72h\"" && \
   echo "$OUTPUT" | grep -q "Stale Exited Containers (older than 72 hours)"; then
  echo "Test 4 PASSED"
else
  echo "Test 4 FAILED"
  echo "Output:" "$OUTPUT"
  exit 1
fi

# Test 5: Live run with specific pruning skipped
echo "Running Test 5: Live run with --no-prune-images and --no-prune-volumes..."

OUTPUT=$(run_compost_script --no-prune-images --no-prune-volumes)

if echo "$OUTPUT" | grep -q "MOCK: container prune -f --filter \"until=24h\"" && \
   echo "$OUTPUT" | grep -q "MOCK: builder prune -f" && \
   echo "$OUTPUT" | grep -q "Skipping dangling image composting." && \
   echo "$OUTPUT" | grep -q "Skipping dangling volume composting."; then
  echo "Test 5 PASSED"
else
  echo "Test 5 FAILED"
  echo "Output:" "$OUTPUT"
  exit 1
fi

# Cleanup
rm -rf "$TEST_DIR"

echo "All tests completed."
