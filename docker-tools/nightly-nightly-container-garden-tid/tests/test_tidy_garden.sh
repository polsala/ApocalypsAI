#!/bin/bash

# Mock rationale: We need to test the script's logic without actually interacting
# with a live Docker daemon, which would make tests non-deterministic and require
# a complex setup. By mocking the 'docker' command, we can control its output
# and simulate various scenarios (e.g., no items to prune, items to prune, successful prune).

# --- Test Setup ---

# Create a temporary directory for our mock 'docker' executable
MOCK_BIN_DIR=$(mktemp -d)
export PATH="$MOCK_BIN_DIR:$PATH"

# Create the mock 'docker' executable
cat << 'EOF' > "$MOCK_BIN_DIR/docker"
#!/bin/bash

# This is a mock 'docker' command for testing purposes.
# It simulates the output of various docker commands.

case "$1 $2 $3" in
  "images -f dangling=true")
    if [ -f "$MOCK_BIN_DIR/mock_dangling_images" ]; then
      cat "$MOCK_BIN_DIR/mock_dangling_images"
    else
      # Simulate no dangling images
      exit 1 # docker images returns non-zero if no matching images
    fi
    ;;
  "ps -a -f")
    if [ -f "$MOCK_BIN_DIR/mock_exited_containers" ]; then
      cat "$MOCK_BIN_DIR/mock_exited_containers"
    else
      # Simulate no exited containers
      exit 1 # docker ps returns non-zero if no matching containers
    fi
    ;;
  "volume ls -f")
    if [ -f "$MOCK_BIN_DIR/mock_dangling_volumes" ]; then
      cat "$MOCK_BIN_DIR/mock_dangling_volumes"
    else
      # Simulate no dangling volumes
      exit 1 # docker volume ls returns non-zero if no matching volumes
    fi
    ;;
  "network ls -f")
    if [ -f "$MOCK_BIN_DIR/mock_unused_networks" ]; then
      cat "$MOCK_BIN_DIR/mock_unused_networks"
    else
      # Simulate no unused networks
      exit 1 # docker network ls returns non-zero if no matching networks
    fi
    ;;
  "system prune -f")
    echo "Total reclaimed space: 123.4MB"
    ;;
  "volume prune -f")
    echo "Total reclaimed space: 10.0MB"
    ;;
  *)
    echo "Mock Docker: Unknown command: $@" >&2
    exit 1
    ;;
esac
EOF
chmod +x "$MOCK_BIN_DIR/docker"

# Source the script to be tested
SCRIPT_TO_TEST="$(dirname "$0")"/../src/tidy_garden.sh

# --- Test Functions ---

run_test () {
  local test_name="$1"
  local expected_output_regex="$2"
  local args="$3"
  local setup_commands="$4"
  
  echo "Running test: $test_name"
  
  # Clean up previous mock files
  rm -f "$MOCK_BIN_DIR/mock_dangling_images"
  rm -f "$MOCK_BIN_DIR/mock_exited_containers"
  rm -f "$MOCK_BIN_DIR/mock_dangling_volumes"
  rm -f "$MOCK_BIN_DIR/mock_unused_networks"
  
  # Execute setup commands if provided
  if [ -n "$setup_commands" ]; then
    eval "$setup_commands"
  fi

  # Run the script and capture output
  OUTPUT=$(bash "$SCRIPT_TO_TEST" $args 2>&1)
  
  # Check if output matches expected regex
  if [[ "$OUTPUT" =~ $expected_output_regex ]]; then
    echo "✅ PASS: $test_name"
  else
    echo "❌ FAIL: $test_name"
    echo "Expected regex: $expected_output_regex"
    echo "Actual output:"
    echo "$OUTPUT"
    exit 1
  fi
}

# --- Test Cases ---

# Test Case 1: Dry run with no items to prune
run_test \
  "Dry run - No items to prune" \
  "Your garden looks remarkably tidy! No major pruning needed at this moment." \
  "" \
  ""

# Test Case 2: Dry run with some items to prune
run_test \
  "Dry run - With items to prune" \
  "Dangling Images \(forgotten seeds\).*testimage:latest \(10MB\).*Exited Containers \(withered blossoms\).*my-old-container \(Exited 5 minutes ago\).*Dangling Volumes \(unclaimed soil plots\).*my_dangling_volume" \
  "" \
  "echo 'testimage:latest (10MB)' > \"$MOCK_BIN_DIR/mock_dangling_images\"; \
   echo 'my-old-container (Exited 5 minutes ago)' > \"$MOCK_BIN_DIR/mock_exited_containers\"; \
   echo 'my_dangling_volume' > \"$MOCK_BIN_DIR/mock_dangling_volumes\""

# Test Case 3: Prune mode - successful pruning
run_test \
  "Prune mode - Successful pruning" \
  "Time to get pruning! Clearing out the digital weeds from your container garden.*Total reclaimed space: 123.4MB.*Your container garden is now sparkling clean!" \
  "--prune" \
  ""

# Test Case 4: No Docker client available
# Mock rationale: Simulate a scenario where 'docker' command is not found.
# This requires temporarily removing the mock_bin_dir from PATH and then restoring it.

# Temporarily remove mock_bin_dir from PATH for this specific test
ORIGINAL_PATH="$PATH"
export PATH=$(echo "$PATH" | sed -e "s|:$MOCK_BIN_DIR||g" -e "s|$MOCK_BIN_DIR:||g" -e "s|$MOCK_BIN_DIR||g")

# Run the script and capture output
OUTPUT=$(bash "$SCRIPT_TO_TEST" 2>&1)

# Check if output matches expected regex
if [[ "$OUTPUT" =~ "Error: Docker client not found." ]]; then
  echo "✅ PASS: No Docker client available"
else
  echo "❌ FAIL: No Docker client available"
  echo "Expected regex: Error: Docker client not found."
  echo "Actual output:"
  echo "$OUTPUT"
  exit 1
fi

# Restore original PATH
export PATH="$ORIGINAL_PATH"

# --- Cleanup ---
rm -rf "$MOCK_BIN_DIR"

echo "\nAll tests completed."
