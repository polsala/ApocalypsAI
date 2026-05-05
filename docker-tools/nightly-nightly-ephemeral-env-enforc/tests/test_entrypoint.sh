#!/bin/bash
set -euo pipefail

# Mock rationale: We need to simulate docker commands without actually running them
# to ensure deterministic and offline testing. This mock creates a temporary 'docker'
# executable that logs its calls and simulates success for expected commands.

MOCK_DOCKER_DIR=$(mktemp -d)
export PATH="$MOCK_DOCKER_DIR:$PATH"
MOCK_LOG="/tmp/mock_docker_log_$$_$(date +%s%N).txt"

# Create a mock docker command
cat << 'EOF' > "$MOCK_DOCKER_DIR/docker"
#!/bin/bash
echo "MOCK DOCKER: $@" >> "$MOCK_LOG"
if [[ "$1" == "run" ]]; then
    echo "MOCK DOCKER RUN: Container started"
    # Simulate a successful run
    exit 0
elif [[ "$1" == "ps" ]]; then
    # Simulate container is running for the first check after sleep
    if grep -q "MOCK DOCKER: ps -q -f name=ephemeral-env-" "$MOCK_LOG"; then
        echo "mock_container_id" # Simulate a running container
    fi
    exit 0
elif [[ "$1" == "stop" ]]; then
    echo "MOCK DOCKER STOP: Container stopped"
    exit 0
elif [[ "$1" == "rm" ]]; then
    echo "MOCK DOCKER RM: Container removed"
    exit 0
else
    echo "MOCK DOCKER: Unknown command $1"
    exit 1
fi
EOF
chmod +x "$MOCK_DOCKER_DIR/docker"

echo "Running test: Valid arguments"
# The entrypoint script expects to be run as /app/entrypoint.sh
# We'll simulate this by calling it directly. The sleep duration is 1 second.
/app/entrypoint.sh "ubuntu:latest" "1" "sleep 0.1 && echo Hello" > /dev/null

# Verify mock docker calls
if ! grep -q "MOCK DOCKER: run -d --name ephemeral-env-" "$MOCK_LOG"; then
    echo "Test failed: 'docker run' not called."
    cat "$MOCK_LOG"
    exit 1
fi
if ! grep -q "MOCK DOCKER: ps -q -f name=ephemeral-env-" "$MOCK_LOG"; then
    echo "Test failed: 'docker ps' not called."
    cat "$MOCK_LOG"
    exit 1
fi
if ! grep -q "MOCK DOCKER: stop ephemeral-env-" "$MOCK_LOG"; then
    echo "Test failed: 'docker stop' not called."
    cat "$MOCK_LOG"
    exit 1
fi
if ! grep -q "MOCK DOCKER: rm ephemeral-env-" "$MOCK_LOG"; then
    echo "Test failed: 'docker rm' not called."
    cat "$MOCK_LOG"
    exit 1
fi
echo "Test passed: Valid arguments"

# Test case: Missing arguments
echo "Running test: Missing arguments"
if /app/entrypoint.sh "ubuntu:latest" "1" > /dev/null 2>&1; then
    echo "Test failed: Missing arguments should fail."
    exit 1
fi
echo "Test passed: Missing arguments"

# Clean up mock docker and log file
rm -rf "$MOCK_DOCKER_DIR"
rm "$MOCK_LOG"

echo "All tests passed!"
