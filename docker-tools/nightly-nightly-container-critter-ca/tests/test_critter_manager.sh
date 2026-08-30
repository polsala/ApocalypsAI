#!/bin/bash

set -euo pipefail

# Mock rationale: We need to test the shell script's logic without actually running Docker commands,
# which would require a Docker daemon, introduce network dependencies, and lead to non-deterministic and slow tests.
# These mocks simulate the expected behavior and output of `docker-compose` and `docker` commands.

# Variables to track mock calls (for debugging if needed)
MOCK_DOCKER_COMPOSE_CALLS=""
MOCK_DOCKER_CALLS=""

# --- Mock `docker-compose` command ---
docker-compose() {
    local cmd="$1"
    shift
    MOCK_DOCKER_COMPOSE_CALLS+="docker-compose $cmd $@\n"

    case "$cmd" in
        "up")
            # Simulate `docker-compose up -d` output
            echo "Mock: docker-compose up -d called"
            ;;
        "down")
            # Simulate `docker-compose down` output
            echo "Mock: docker-compose down called"
            ;;
        "ps")
            # Simulate `docker-compose ps` output for a running container
            echo "Name                     Command               State    Ports"
            echo "-------------------------------------------------------------------"
            echo "testcritter-critter-container   python /app/critter.py   Up      "
            ;;
        "exec")
            # Simulate `docker-compose exec` to run `critter.py`
            local critter_container_name=""
            local python_script_path=""
            local critter_command=""

            # Parse arguments for exec
            while [[ $# -gt 0 ]]; do
                case "$1" in
                    "-f") shift ;; # Skip -f <file>
                    "testcritter-critter") critter_container_name="$1" ;;
                    "python") python_script_path="$1" ;;
                    "/app/critter.py") python_script_path="$1" ;;
                    *) critter_command="$1" ;;
                esac
                shift
            done

            # Simulate critter.py output based on command
            case "$critter_command" in
                "feed")
                    echo "Critter fed! It's feeling Happy."
                    ;;
                "play")
                    echo "Critter played with! It's feeling Excited."
                    ;;
                *) # Default or unknown command, simulate reading mood
                    echo "Critter is feeling Content."
                    ;;
            esac
            ;;
        *)
            echo "Mock: Unknown docker-compose command: $cmd" >&2
            exit 1
            ;;
    esac
}

# --- Mock `docker` command ---
docker() {
    MOCK_DOCKER_CALLS+="docker $@\n"
    local cmd="$1"
    shift

    case "$cmd" in
        "ps")
            # Simulate `docker ps` to check if container is running
            if [[ "$@" == *"--format '{{.Names}}'"* && "$@" == *"testcritter-critter-container"* ]]; then
                echo "testcritter-critter-container"
            else
                echo ""
            fi
            ;;
        *)
            echo "Mock: Unknown docker command: $cmd" >&2
            exit 1
            ;;
    esac
}

# --- Test Setup ---
# Create a temporary directory for tests to avoid polluting the actual filesystem
TEST_ROOT_DIR=$(mktemp -d)

# Copy the script and its templates to the test directory
cp ../src/critter_manager.sh "$TEST_ROOT_DIR/critter_manager.sh"
mkdir -p "$TEST_ROOT_DIR/src/critter_template"
cp ../src/critter_template/Dockerfile "$TEST_ROOT_DIR/src/critter_template/Dockerfile"
cp ../src/critter_template/critter.py "$TEST_ROOT_DIR/src/critter_template/critter.py"

# Adjust the script's internal paths to point to the test directories
# This ensures the script operates within the isolated test environment
sed -i "s|CRITTER_DIR=\"critters\"|CRITTER_DIR=\"$TEST_ROOT_DIR/critters\"|" "$TEST_ROOT_DIR/critter_manager.sh"
sed -i "s|CRITTER_TEMPLATE_DIR=\"src/critter_template\"|CRITTER_TEMPLATE_DIR=\"$TEST_ROOT_DIR/src/critter_template\"|" "$TEST_ROOT_DIR/critter_manager.sh"

CRITTER_MANAGER_SCRIPT="$TEST_ROOT_DIR/critter_manager.sh"
CRITTERS_TEST_DIR="$TEST_ROOT_DIR/critters"

# Helper function to run a test case
run_test() {
    local test_name="$1"
    local expected_output_regex="$2"
    local command_args="${@:3}"
    local actual_output

    echo "--- Running Test: $test_name ---"
    actual_output=$("$CRITTER_MANAGER_SCRIPT" $command_args 2>&1)

    if [[ "$actual_output" =~ $expected_output_regex ]]; then
        echo "PASS: $test_name"
    else
        echo "FAIL: $test_name"
        echo "  Expected regex: '$expected_output_regex'"
        echo "  Actual output:  '$actual_output'"
        exit 1
    fi
    echo ""
}

# --- Test Cases ---

# Test 1: init command - successful initialization
run_test "init command - success" "Critter 'testcritter' initialized." init testcritter

# Verify files and directories created by init
if [[ ! -d "$CRITTERS_TEST_DIR/testcritter" ]]; then echo "FAIL: testcritter directory not created"; exit 1; fi
if [[ ! -f "$CRITTERS_TEST_DIR/testcritter/docker-compose.yml" ]]; then echo "FAIL: docker-compose.yml not created"; exit 1; fi
if ! grep -q "testcritter-critter:" "$CRITTERS_TEST_DIR/testcritter/docker-compose.yml"; then echo "FAIL: docker-compose.yml content incorrect"; exit 1; fi
if ! grep -q "container_name: testcritter-critter-container" "$CRITTERS_TEST_DIR/testcritter/docker-compose.yml"; then echo "FAIL: docker-compose.yml container_name incorrect"; exit 1; fi
echo "PASS: init command - file verification"
echo ""

# Test 2: init command - critter already exists
run_test "init command - already exists" "Error: Critter 'testcritter' already exists." init testcritter

# Test 3: start command
run_test "start command" "Mock: docker-compose up -d called" start testcritter

# Test 4: status command
run_test "status command" "testcritter-critter-container   python /app/critter.py   Up" status testcritter

# Test 5: interact command - default mood
run_test "interact command - default mood" "Critter is feeling Content." interact testcritter

# Test 6: interact command - feed
run_test "interact command - feed" "Critter fed! It's feeling Happy." interact testcritter feed

# Test 7: interact command - play
run_test "interact command - play" "Critter played with! It's feeling Excited." interact testcritter play

# Test 8: stop command
run_test "stop command" "Mock: docker-compose down called" stop testcritter

# Test 9: interact command - critter not running (after stop)
# Temporarily disable docker ps mock to simulate container not running
# Mock rationale: Simulating a container not running requires temporarily altering the mock behavior.
# This ensures the error handling for non-running containers is tested deterministically.

# Save original docker function
ORIG_DOCKER=$(declare -f docker)

# Override docker ps to return empty, simulating no running container
docker() {
    local cmd="$1"
    shift
    if [[ "$cmd" == "ps" ]]; then
        echo "" # Simulate no running containers
    else
        eval "$ORIG_DOCKER"
    fi
}

run_test "interact command - critter not running" "Error: Critter 'testcritter' container is not running. Please start it first." interact testcritter

# Restore original docker function
eval "$ORIG_DOCKER"

# --- Cleanup ---
rm -rf "$TEST_ROOT_DIR"

echo "All tests passed!"
