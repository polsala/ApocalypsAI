#!/bin/bash

# Mock rationale: We need to test the script's logic for parsing arguments and
# deciding which docker commands to run, as well as its output formatting.
# Directly interacting with a live Docker daemon would make tests non-deterministic
# and require a running Docker environment. By mocking the 'docker' command,
# we can control its output and verify the script's behavior in isolation.

# --- Test Setup ---

# Create a temporary directory for test outputs and mock executables
TEST_DIR=$(mktemp -d)
export PATH="$TEST_DIR:$PATH" # Add test dir to PATH to intercept 'docker'

# Create a mock docker executable
cat << 'EOF' > "$TEST_DIR/docker"
#!/bin/bash
# This is a mock docker command for testing purposes.
# It simulates various docker command outputs based on predefined scenarios.

MOCK_SCENARIO=${MOCK_SCENARIO:-"empty"} # Default scenario

case "$1" in
    "images")
        if [[ "$2" == "-f" && "$3" == "dangling=true" ]]; then
            if [[ "$MOCK_SCENARIO" == "dangling_images" || "$MOCK_SCENARIO" == "all_dust" ]]; then
                if [[ "$4" == "-q" ]]; then
                    echo "dangling_image_id_1\ndangling_image_id_2"
                else
                    echo "REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE"
                    echo "<none>              <none>              dangling_image_id_1 2 hours ago         10MB"
                    echo "<none>              <none>              dangling_image_id_2 5 hours ago         20MB"
                fi
            fi
        fi
        ;;
    "ps")
        if [[ "$2" == "-a" && "$3" == "-f" && "$4" == "status=exited" ]]; then
            if [[ "$MOCK_SCENARIO" == "exited_containers" || "$MOCK_SCENARIO" == "all_dust" ]]; then
                if [[ "$5" == "-q" ]]; then
                    echo "exited_container_id_1\nexited_container_id_2"
                else
                    echo "CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                      PORTS               NAMES"
                    echo "exited_container_id_1 myimage:latest      \"/bin/sh\"           3 hours ago         Exited (0) 2 hours ago                          exited_app_1"
                    echo "exited_container_id_2 another:v1          \"/bin/bash\"         6 hours ago         Exited (137) 5 hours ago                        old_service_2"
                fi
            fi
        fi
        ;;
    "volume")
        if [[ "$2" == "ls" && "$3" == "-f" && "$4" == "dangling=true" ]]; then
            if [[ "$MOCK_SCENARIO" == "unused_volumes" || "$MOCK_SCENARIO" == "all_dust" ]]; then
                if [[ "$5" == "-q" ]]; then
                    echo "unused_volume_1\nunused_volume_2"
                else
                    echo "DRIVER              VOLUME NAME"
                    echo "local               unused_volume_1"
                    echo "local               unused_volume_2"
                fi
            fi
        fi
        ;;
    "rmi")
        shift # remove "rmi"
        for id in "$@"; do
            echo "Mock: Removed image $id"
        done
        ;;
    "rm")
        shift # remove "rm"
        for id in "$@"; do
            echo "Mock: Removed container $id"
        done
        ;;
    "volume")
        if [[ "$2" == "rm" ]]; then
            shift 2 # remove "volume" and "rm"
            for id in "$@"; do
                echo "Mock: Removed volume $id"
            done
        fi
        ;;
    *)
        echo "Mock: Unknown docker command: $@" >&2
        exit 1
        ;;
esac
EOF
chmod +x "$TEST_DIR/docker"

# --- Helper function for assertions ---
assert_contains() {
    local expected="$1"
    local actual="$2"
    if ! echo "$actual" | grep -qF "$expected"; then
        echo "FAIL: Expected '$actual' to contain '$expected'"
        exit 1
    fi
}

assert_not_contains() {
    local unexpected="$1"
    local actual="$2"
    if echo "$actual" | grep -qF "$unexpected"; then
        echo "FAIL: Expected '$actual' NOT to contain '$unexpected'"
        exit 1
    fi
}

# --- Test Cases ---

echo "Running tests for sweep.sh..."
SCRIPT_PATH="./src/sweep.sh" # Assuming script is in src/

# Test 1: No dust bunnies (report only)
echo "Test 1: Report only, no dust bunnies"
export MOCK_SCENARIO="empty"
OUTPUT=$(bash "$SCRIPT_PATH" 2>&1)
assert_contains "No dangling images found." "$OUTPUT"
assert_contains "No exited containers found." "$OUTPUT"
assert_contains "No unused volumes found." "$OUTPUT"
assert_contains "Report complete. Run with '--prune' to remove identified resources." "$OUTPUT"
assert_not_contains "Pruning dangling images..." "$OUTPUT"
assert_not_contains "Removing exited containers..." "$OUTPUT"
assert_not_contains "Pruning unused volumes..." "$OUTPUT"
echo "Test 1 Passed."

# Test 2: Dangling images present (report only)
echo "Test 2: Report only, dangling images present"
export MOCK_SCENARIO="dangling_images"
OUTPUT=$(bash "$SCRIPT_PATH" 2>&1)
assert_contains "dangling_image_id_1" "$OUTPUT"
assert_contains "No exited containers found." "$OUTPUT"
assert_contains "No unused volumes found." "$OUTPUT"
assert_contains "Report complete. Run with '--prune' to remove identified resources." "$OUTPUT"
assert_not_contains "Pruning dangling images..." "$OUTPUT"
echo "Test 2 Passed."

# Test 3: Exited containers present (report only)
echo "Test 3: Report only, exited containers present"
export MOCK_SCENARIO="exited_containers"
OUTPUT=$(bash "$SCRIPT_PATH" 2>&1)
assert_contains "exited_container_id_1" "$OUTPUT"
assert_contains "No dangling images found." "$OUTPUT"
assert_contains "No unused volumes found." "$OUTPUT"
assert_contains "Report complete. Run with '--prune' to remove identified resources." "$OUTPUT"
assert_not_contains "Removing exited containers..." "$OUTPUT"
echo "Test 3 Passed."

# Test 4: Unused volumes present (report only)
echo "Test 4: Report only, unused volumes present"
export MOCK_SCENARIO="unused_volumes"
OUTPUT=$(bash "$SCRIPT_PATH" 2>&1)
assert_contains "unused_volume_1" "$OUTPUT"
assert_contains "No dangling images found." "$OUTPUT"
assert_contains "No exited containers found." "$OUTPUT"
assert_contains "Report complete. Run with '--prune' to remove identified resources." "$OUTPUT"
assert_not_contains "Pruning unused volumes..." "$OUTPUT"
echo "Test 4 Passed."

# Test 5: All dust bunnies present (report only)
echo "Test 5: Report only, all dust bunnies present"
export MOCK_SCENARIO="all_dust"
OUTPUT=$(bash "$SCRIPT_PATH" 2>&1)
assert_contains "dangling_image_id_1" "$OUTPUT"
assert_contains "exited_container_id_1" "$OUTPUT"
assert_contains "unused_volume_1" "$OUTPUT"
assert_contains "Report complete. Run with '--prune' to remove identified resources." "$OUTPUT"
assert_not_contains "Pruning dangling images..." "$OUTPUT"
assert_not_contains "Removing exited containers..." "$OUTPUT"
assert_not_contains "Pruning unused volumes..." "$OUTPUT"
echo "Test 5 Passed."

# Test 6: All dust bunnies present (prune mode)
echo "Test 6: Prune mode, all dust bunnies present"
export MOCK_SCENARIO="all_dust"
OUTPUT=$(bash "$SCRIPT_PATH" --prune 2>&1)
assert_contains "dangling_image_id_1" "$OUTPUT"
assert_contains "exited_container_id_1" "$OUTPUT"
assert_contains "unused_volume_1" "$OUTPUT"
assert_contains "Pruning dangling images..." "$OUTPUT"
assert_contains "Mock: Removed image dangling_image_id_1" "$OUTPUT"
assert_contains "Mock: Removed image dangling_image_id_2" "$OUTPUT"
assert_contains "Dangling images pruned." "$OUTPUT"
assert_contains "Removing exited containers..." "$OUTPUT"
assert_contains "Mock: Removed container exited_container_id_1" "$OUTPUT"
assert_contains "Mock: Removed container exited_container_id_2" "$OUTPUT"
assert_contains "Exited containers removed." "$OUTPUT"
assert_contains "Pruning unused volumes..." "$OUTPUT"
assert_contains "Mock: Removed volume unused_volume_1" "$OUTPUT"
assert_contains "Mock: Removed volume unused_volume_2" "$OUTPUT"
assert_contains "Unused volumes pruned." "$OUTPUT"
assert_contains "Cleanup complete." "$OUTPUT"
assert_not_contains "Report complete. Run with '--prune' to remove identified resources." "$OUTPUT"
echo "Test 6 Passed."

# Test 7: Help message
echo "Test 7: Help message"
OUTPUT=$(bash "$SCRIPT_PATH" --help 2>&1)
assert_contains "Usage: sweep.sh [--prune]" "$OUTPUT"
assert_contains "Display this help message." "$OUTPUT"
echo "Test 7 Passed."

# Test 8: Unknown option
echo "Test 8: Unknown option"
OUTPUT=$(bash "$SCRIPT_PATH" --unknown-arg 2>&1)
assert_contains "Unknown option: --unknown-arg" "$OUTPUT"
assert_contains "Usage: sweep.sh [--prune]" "$OUTPUT"
echo "Test 8 Passed."

echo "All tests passed!"

# --- Teardown ---
rm -rf "$TEST_DIR"
