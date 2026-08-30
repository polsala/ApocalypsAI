#!/bin/bash
set -euo pipefail

# Mock rationale: We don't want to actually run Docker commands during tests,
# as this would make tests non-deterministic, slow, and require a Docker daemon.
# We mock 'docker' to capture its arguments and simulate its output.

MOCKED_DOCKER_CALLS=""
MOCKED_DOCKER_BUILD_SUCCESS=true
MOCKED_DOCKER_RUN_SUCCESS=true
MOCKED_DOCKER_RMI_SUCCESS=true

# Mock the docker command
docker() {
    MOCKED_DOCKER_CALLS+="docker $@\n"
    case "$1" in
        "build")
            if [ "$MOCKED_DOCKER_BUILD_SUCCESS" = true ]; then
                echo "Mocked docker build success"
            else
                echo "Mocked docker build failure" >&2
                return 1
            fi
            ;;
        "run")
            if [ "$MOCKED_DOCKER_RUN_SUCCESS" = true ]; then
                # Capture the command passed to bash -c (it's the 8th argument)
                local run_command_arg="${@:8}"
                echo "Mocked docker run success for command: $run_command_arg"
            else
                echo "Mocked docker run failure" >&2
                return 1
            fi
            ;;
        "rmi")
            if [ "$MOCKED_DOCKER_RMI_SUCCESS" = true ]; then
                echo "Mocked docker rmi success"
            else
                echo "Mocked docker rmi failure" >&2
                return 1
            fi
            ;;
        *)
            echo "Unknown docker command: $@" >&2
            return 1
            ;;
    esac
}

# Save original PATH and add current directory to PATH for mocking
ORIGINAL_PATH="$PATH"
export PATH="$(pwd):$PATH"

# Create a dummy Dockerfile for the test in the src directory
mkdir -p src
echo "FROM alpine:latest" > src/Dockerfile

# Test 1: No command provided
echo "--- Test 1: No command provided ---"
MOCKED_DOCKER_CALLS=""
output=$( (cd src && bash run.sh) 2>&1 || true )
if [[ "$output" == *"Usage: ./run.sh <command_to_run_in_container>"* ]]; then
    echo "PASS: Correctly handled no command."
else
    echo "FAIL: Did not handle no command. Output: $output"
    exit 1
fi
if [[ "$MOCKED_DOCKER_CALLS" != "" ]]; then
    echo "FAIL: Docker commands were called when they shouldn't have been. Calls: $MOCKED_DOCKER_CALLS"
    exit 1
fi

# Test 2: Successful execution
echo "--- Test 2: Successful execution ---"
MOCKED_DOCKER_CALLS=""
output=$( (cd src && bash run.sh "echo Hello Forager") 2>&1 )
if [[ "$output" == *"Building Foraging Pod image..."* && \
          "$output" == *"Launching Foraging Pod container"* && \
          "$output" == *"Foraging Pod mission complete. Cleaning up..."* && \
          "$output" == *"Foraging Pod is gone. Stay safe out there!"* ]]; then
    echo "PASS: Script output looks correct."
else
    echo "FAIL: Script output incorrect. Output: $output"
    exit 1
fi

# Verify correct Docker commands were called
if [[ "$MOCKED_DOCKER_CALLS" == *"docker build -t foraging-pod-image ."* && \
          "$MOCKED_DOCKER_CALLS" == *"docker run --rm --name foraging-pod-container-"*" foraging-pod-image bash -c echo Hello Forager"* && \
          "$MOCKED_DOCKER_CALLS" == *"docker rmi foraging-pod-image"* ]]; then
    echo "PASS: Correct Docker commands were called."
else
    echo "FAIL: Incorrect Docker commands called. Calls: $MOCKED_DOCKER_CALLS"
    exit 1
fi

# Test 3: Docker build fails
echo "--- Test 3: Docker build fails ---"
MOCKED_DOCKER_CALLS=""
MOCKED_DOCKER_BUILD_SUCCESS=false
output=$( (cd src && bash run.sh "echo Test") 2>&1 || true )
if [[ "$output" == *"Mocked docker build failure"* ]]; then
    echo "PASS: Handled docker build failure."
else
    echo "FAIL: Did not handle docker build failure. Output: $output"
    exit 1
fi
if [[ "$MOCKED_DOCKER_CALLS" == *"docker run"* || "$MOCKED_DOCKER_CALLS" == *"docker rmi"* ]]; then
    echo "FAIL: Docker run or rmi called after build failure. Calls: $MOCKED_DOCKER_CALLS"
    exit 1
fi
MOCKED_DOCKER_BUILD_SUCCESS=true # Reset for next tests

# Test 4: Docker run fails
echo "--- Test 4: Docker run fails ---"
MOCKED_DOCKER_CALLS=""
MOCKED_DOCKER_RUN_SUCCESS=false
output=$( (cd src && bash run.sh "echo Test") 2>&1 || true )
if [[ "$output" == *"Mocked docker run failure"* ]]; then
    echo "PASS: Handled docker run failure."
else
    echo "FAIL: Did not handle docker run failure. Output: $output"
    exit 1
fi
# Ensure build was called, but rmi was not
if [[ ! "$MOCKED_DOCKER_CALLS" == *"docker build"* || "$MOCKED_DOCKER_CALLS" == *"docker rmi"* ]]; then
    echo "FAIL: Docker build not called or rmi called after run failure. Calls: $MOCKED_DOCKER_CALLS"
    exit 1
fi
MOCKED_DOCKER_RUN_SUCCESS=true # Reset for next tests

# Test 5: Docker rmi fails (should still complete the script, but log error)
echo "--- Test 5: Docker rmi fails ---"
MOCKED_DOCKER_CALLS=""
MOCKED_DOCKER_RMI_SUCCESS=false
output=$( (cd src && bash run.sh "echo Test") 2>&1 )
if [[ "$output" == *"Mocked docker rmi failure"* ]]; then
    echo "PASS: Handled docker rmi failure."
else
    echo "FAIL: Did not handle docker rmi failure. Output: $output"
    exit 1
fi
# Ensure build, run, and rmi were all attempted
if [[ ! "$MOCKED_DOCKER_CALLS" == *"docker build"* || ! "$MOCKED_DOCKER_CALLS" == *"docker run"* || ! "$MOCKED_DOCKER_CALLS" == *"docker rmi"* ]]; then
    echo "FAIL: Docker build, run, or rmi not called correctly. Calls: $MOCKED_DOCKER_CALLS"
    exit 1
fi
MOCKED_DOCKER_RMI_SUCCESS=true # Reset for next tests

# Cleanup dummy Dockerfile and src directory
rm src/Dockerfile
rmdir src

# Restore original PATH
export PATH="$ORIGINAL_PATH"

echo "All tests passed!"
