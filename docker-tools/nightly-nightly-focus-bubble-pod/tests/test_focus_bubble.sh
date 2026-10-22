#!/bin/bash

# Mock rationale: We need to test the shell script's logic and its interaction
# with the 'docker' command without actually running Docker containers, which
# would make the tests non-deterministic, slow, and require a Docker daemon.
# Mocking 'docker' allows us to verify command arguments and outputs.

# --- Mocks ---
MOCKED_DOCKER_CALLS=() # Stores full command strings as they would be executed
MOCKED_DOCKER_EXIT_CODE=0
MOCKED_DOCKER_PS_OUTPUT=""
MOCKED_DOCKER_IMAGES_OUTPUT=""

docker() {
    MOCKED_DOCKER_CALLS+=("docker $@") # Capture the full command
    case "$1" in
        "build")
            if [[ "$MOCKED_DOCKER_EXIT_CODE" -ne 0 ]]; then
                return "$MOCKED_DOCKER_EXIT_CODE"
            fi
            echo "Mock: Building image $3 from $4"
            ;;
        "run")
            if [[ "$MOCKED_DOCKER_EXIT_CODE" -ne 0 ]]; then
                return "$MOCKED_DOCKER_EXIT_CODE"
            fi
            # Simulate interactive session by not exiting immediately
            # For testing, we just need to know it was called.
            echo "Mock: Running container $10 with volume $6"
            ;;
        "ps")
            echo "$MOCKED_DOCKER_PS_OUTPUT"
            ;;
        "images")
            echo "$MOCKED_DOCKER_IMAGES_OUTPUT"
            ;;
        "stop")
            echo "Mock: Stopping container $2"
            ;;
        "rm")
            echo "Mock: Removing container $3"
            ;;
        "rmi")
            echo "Mock: Removing image $2"
            ;;
        *)
            echo "Mock: Unknown docker command: $@"
            ;;
    esac
    return "$MOCKED_DOCKER_EXIT_CODE"
}

# --- Test Helpers ---
assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "$expected" != "$actual" ]]; then
        echo "FAIL: $message"
        echo "  Expected: '$expected'"
        echo "  Actual:   '$actual'"
        exit 1
    else
        echo "PASS: $message"
    fi
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if [[ "$haystack" != *"$needle"* ]]; then
        echo "FAIL: $message"
        echo "  Haystack: '$haystack'"
        echo "  Needle:   '$needle'"
        exit 1
    else
        echo "PASS: $message"
    fi
}

reset_mocks() {
    MOCKED_DOCKER_CALLS=()
    MOCKED_DOCKER_EXIT_CODE=0
    MOCKED_DOCKER_PS_OUTPUT=""
    MOCKED_DOCKER_IMAGES_OUTPUT=""
}

# --- Tests ---

SCRIPT_PATH="./src/focus-bubble.sh"
IMAGE_NAME="focus-bubble-pod"
CONTAINER_NAME="focus-bubble-instance"
DATA_DIR="focus_data"

echo "--- Running Tests for Focus Bubble Pod ---"

# Test 1: build command success
reset_mocks
output=$(bash "$SCRIPT_PATH" build 2>&1)
assert_equals "docker build -t $IMAGE_NAME src/" "${MOCKED_DOCKER_CALLS[0]}" "Test 1.1: build calls docker build"
assert_contains "$output" "Focus Bubble Pod image built successfully!" "Test 1.2: build success message"

# Test 2: build command failure
reset_mocks
MOCKED_DOCKER_EXIT_CODE=1
output=$(bash "$SCRIPT_PATH" build 2>&1)
assert_equals "docker build -t $IMAGE_NAME src/" "${MOCKED_DOCKER_CALLS[0]}" "Test 2.1: build calls docker build on failure"
assert_contains "$output" "Failed to build Focus Bubble Pod image." "Test 2.2: build failure message"

# Test 3: start command - image not found, builds then runs
reset_mocks
MOCKED_DOCKER_IMAGES_OUTPUT="" # Simulate no image
output=$(bash "$SCRIPT_PATH" start 2>&1)
assert_equals "docker build -t $IMAGE_NAME src/" "${MOCKED_DOCKER_CALLS[0]}" "Test 3.1: start builds image if not found"
assert_contains "${MOCKED_DOCKER_CALLS[1]}" "docker run -it --rm -v $(pwd)/$DATA_DIR:/app/data --name $CONTAINER_NAME $IMAGE_NAME bash -c cowsay 'Welcome to your Focus Bubble! Your thoughts are safe here. Your data is in /app/data.'; bash" "Test 3.2: start runs container with correct args"
assert_contains "$output" "Starting your ephemeral Focus Bubble Pod." "Test 3.3: start success message"
rmdir "$DATA_DIR" > /dev/null 2>&1 # Clean up created directory

# Test 4: start command - image found, runs
reset_mocks
MOCKED_DOCKER_IMAGES_OUTPUT="<some_image_id> $IMAGE_NAME latest <size>" # Simulate image exists
output=$(bash "$SCRIPT_PATH" start 2>&1)
assert_contains "${MOCKED_DOCKER_CALLS[0]}" "docker run -it --rm -v $(pwd)/$DATA_DIR:/app/data --name $CONTAINER_NAME $IMAGE_NAME" "Test 4.1: start runs container directly if image found"
assert_contains "$output" "Starting your ephemeral Focus Bubble Pod." "Test 4.2: start success message"
rmdir "$DATA_DIR" > /dev/null 2>&1 # Clean up created directory

# Test 5: start command - container already running
reset_mocks
MOCKED_DOCKER_PS_OUTPUT="<container_id> $CONTAINER_NAME <image> <command> <created> <status> <ports>" # Simulate container running
MOCKED_DOCKER_IMAGES_OUTPUT="<some_image_id> $IMAGE_NAME latest <size>" # Simulate image exists
output=$(bash "$SCRIPT_PATH" start 2>&1)
assert_equals 0 "${#MOCKED_DOCKER_CALLS[@]}" "Test 5.1: start does not call docker if container running"
assert_contains "$output" "Focus Bubble Pod is already running or stopped." "Test 5.2: start error message if running"

# Test 6: stop command - container running
reset_mocks
MOCKED_DOCKER_PS_OUTPUT="<container_id> $CONTAINER_NAME <image> <command> <created> <status> <ports>" # Simulate container running
output=$(bash "$SCRIPT_PATH" stop 2>&1)
assert_equals "docker stop $CONTAINER_NAME" "${MOCKED_DOCKER_CALLS[0]}" "Test 6.1: stop calls docker stop"
assert_contains "$output" "Focus Bubble Pod stopped." "Test 6.2: stop success message"

# Test 7: stop command - container not running
reset_mocks
MOCKED_DOCKER_PS_OUTPUT="" # Simulate no container running
output=$(bash "$SCRIPT_PATH" stop 2>&1)
assert_equals 0 "${#MOCKED_DOCKER_CALLS[@]}" "Test 7.1: stop does not call docker if container not running"
assert_contains "$output" "Focus Bubble Pod is not running." "Test 7.2: stop message if not running"

# Test 8: clean command - container and image exist
reset_mocks
MOCKED_DOCKER_PS_OUTPUT="<container_id> $CONTAINER_NAME <image> <command> <created> <status> <ports>"
MOCKED_DOCKER_IMAGES_OUTPUT="<some_image_id> $IMAGE_NAME latest <size>"
output=$(bash "$SCRIPT_PATH" clean 2>&1)
assert_equals "docker rm -f $CONTAINER_NAME" "${MOCKED_DOCKER_CALLS[0]}" "Test 8.1: clean removes container"
assert_equals "docker rmi $IMAGE_NAME" "${MOCKED_DOCKER_CALLS[1]}" "Test 8.2: clean removes image"
assert_contains "$output" "Cleanup complete." "Test 8.3: clean success message"

# Test 9: clean command - only image exists
reset_mocks
MOCKED_DOCKER_PS_OUTPUT=""
MOCKED_DOCKER_IMAGES_OUTPUT="<some_image_id> $IMAGE_NAME latest <size>"
output=$(bash "$SCRIPT_PATH" clean 2>&1)
assert_equals "docker rmi $IMAGE_NAME" "${MOCKED_DOCKER_CALLS[0]}" "Test 9.1: clean removes image if no container"
assert_contains "$output" "Cleanup complete." "Test 9.2: clean success message"

# Test 10: clean command - nothing exists
reset_mocks
MOCKED_DOCKER_PS_OUTPUT=""
MOCKED_DOCKER_IMAGES_OUTPUT=""
output=$(bash "$SCRIPT_PATH" clean 2>&1)
assert_equals 0 "${#MOCKED_DOCKER_CALLS[@]}" "Test 10.1: clean calls no docker commands if nothing exists"
assert_contains "$output" "Cleanup complete." "Test 10.2: clean success message"

# Test 11: invalid command
reset_mocks
output=$(bash "$SCRIPT_PATH" invalid_command 2>&1)
assert_contains "$output" "Usage: ./src/focus-bubble.sh {build|start|stop|clean}" "Test 11.1: invalid command usage message"

echo "--- All tests passed! ---"
