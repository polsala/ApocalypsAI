#!/bin/bash

# Mock rationale: To ensure tests are deterministic and offline,
# the 'docker' and 'docker compose' commands are mocked.
# This simulates their execution without requiring a live Docker daemon,
# allowing verification of argument parsing and command flow.

# Setup mock environment
MOCK_BIN_DIR=$(mktemp -d)
export PATH="$MOCK_BIN_DIR:$PATH"

# Create mock docker command
cat << 'EOF' > "$MOCK_BIN_DIR/docker"
#!/bin/bash
# Echo all arguments to capture the full command
echo "MOCK_DOCKER: $@"

# Handle 'docker system prune' specifically
if [[ "$1" == "system" && "$2" == "prune" ]]; then
    echo "MOCK_DOCKER: System prune called."
    exit 0
fi

# If it's a 'docker compose' command, pass it to the mock_docker_compose
if [[ "$1" == "compose" ]]; then
    shift # Remove 'compose'
    "$MOCK_BIN_DIR/docker_compose" "$@"
    exit $?
fi

# For any other docker command, just exit successfully
exit 0
EOF
chmod +x "$MOCK_BIN_DIR/docker"

# Create mock docker compose command
cat << 'EOF' > "$MOCK_BIN_DIR/docker_compose"
#!/bin/bash
# Echo all arguments to capture the full command
echo "MOCK_DOCKER_COMPOSE: $@"

# Check for 'up' command
if [[ "$1" == "-f" && "$3" == "-p" && "$5" == "up" ]]; then
    echo "MOCK_DOCKER_COMPOSE: Project $4 up with file $2"
    exit 0
fi

# Check for 'down' command
if [[ "$1" == "-f" && "$3" == "-p" && "$5" == "down" ]]; then
    echo "MOCK_DOCKER_COMPOSE: Project $4 down with file $2"
    exit 0
fi

# Check for 'ps' command
if [[ "$1" == "-f" && "$3" == "-p" && "$5" == "ps" ]]; then
    echo "MOCK_DOCKER_COMPOSE: Project $4 ps with file $2"
    exit 0
fi

# If no specific mock matched, indicate failure
exit 1
EOF
chmod +x "$MOCK_BIN_DIR/docker_compose"

# Create a dummy docker-compose.yml for tests
DUMMY_COMPOSE_DIR=$(mktemp -d)
DUMMY_COMPOSE_FILE="$DUMMY_COMPOSE_DIR/docker-compose.yml"
echo "version: '3.8'\nservices:\n  web:\n    image: nginx" > "$DUMMY_COMPOSE_FILE"

DUMMY_CUSTOM_COMPOSE_FILE="$DUMMY_COMPOSE_DIR/custom-stack.yml"
echo "version: '3.8'\nservices:\n  db:\n    image: postgres" > "$DUMMY_CUSTOM_COMPOSE_FILE"

# Source the script to be tested
GARDEN_SCRIPT_PATH="$(dirname "$0")"/../src/garden.sh

# Test function
run_test() {
    local test_name="$1"
    local expected_output_regex="$2"
    shift 2
    local actual_output
    echo "--- Running test: $test_name ---"
    # Run the garden script with the provided arguments
    actual_output=$("$GARDEN_SCRIPT_PATH" "$@" 2>&1)
    echo "Actual Output:\n$actual_output"
    if [[ "$actual_output" =~ $expected_output_regex ]]; then
        echo "PASS: $test_name"
        return 0
    else
        echo "FAIL: $test_name"
        echo "Expected regex: $expected_output_regex"
        return 1
    fi
}

# Test cases
TEST_FAILED=0

# Test 1: No arguments, should show usage
run_test "No arguments" "Usage: garden <command>" || TEST_FAILED=1

# Test 2: grow command with default file
( # Run in subshell to isolate cd
    cd "$DUMMY_COMPOSE_DIR" || exit 1
    run_test "grow default compose file" "MOCK_DOCKER_COMPOSE: -f docker-compose.yml -p $(basename "$DUMMY_COMPOSE_DIR") up -d --build" grow || TEST_FAILED=1
)

# Test 3: grow command with custom file
( # Run in subshell to isolate cd
    cd "$DUMMY_COMPOSE_DIR" || exit 1
    run_test "grow custom compose file" "MOCK_DOCKER_COMPOSE: -f custom-stack.yml -p $(basename "$DUMMY_COMPOSE_DIR") up -d --build" grow -f custom-stack.yml || TEST_FAILED=1
)

# Test 4: harvest command with default file
( # Run in subshell to isolate cd
    cd "$DUMMY_COMPOSE_DIR" || exit 1
    run_test "harvest default compose file" "MOCK_DOCKER_COMPOSE: -f docker-compose.yml -p $(basename "$DUMMY_COMPOSE_DIR") down --volumes --remove-orphans" harvest || TEST_FAILED=1
)

# Test 5: status command with default file
( # Run in subshell to isolate cd
    cd "$DUMMY_COMPOSE_DIR" || exit 1
    run_test "status default compose file" "MOCK_DOCKER_COMPOSE: -f docker-compose.yml -p $(basename "$DUMMY_COMPOSE_DIR") ps" status || TEST_FAILED=1
)

# Test 6: weed command
run_test "weed command" "MOCK_DOCKER: System prune called." weed || TEST_FAILED=1

# Test 7: Unknown command
run_test "Unknown command" "Error: Unknown command 'foobar'" foobar || TEST_FAILED=1

# Test 8: grow with non-existent file
run_test "grow non-existent file" "Error: Compose file 'non-existent.yml' not found." grow -f non-existent.yml || TEST_FAILED=1

# Test 9: weed command with arguments (should fail)
run_test "weed with arguments" "Error: 'weed' command does not accept arguments." weed extra_arg || TEST_FAILED=1

# Cleanup mock environment
rm -rf "$MOCK_BIN_DIR" "$DUMMY_COMPOSE_DIR"

if [[ "$TEST_FAILED" -eq 0 ]]; then
    echo "All tests passed!"
    exit 0
else
    echo "Some tests failed!"
    exit 1
fi
