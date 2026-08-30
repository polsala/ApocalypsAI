#!/bin/bash
set -euo pipefail

# Create a temporary directory for mock binaries
MOCK_BIN_DIR=$(mktemp -d)
export PATH="$MOCK_BIN_DIR:$PATH"

# Mock rationale: We don't want to actually run Docker commands during tests.
# We want to verify that the entrypoint script calls 'docker compose' with the correct arguments.
# This mock replaces the actual 'docker compose' binary.
cat <<EOF > "$MOCK_BIN_DIR/docker-compose"
#!/bin/bash
echo "MOCK: docker compose called with: \$@" >> /tmp/docker_compose_calls.log
case "\$1" in
    up)
        echo "MOCK: docker compose up called"
        ;;
    down)
        echo "MOCK: docker compose down called"
        ;;
    ps)
        echo "MOCK: docker compose ps called"
        echo "web running"
        echo "db running"
        echo "cache running"
        ;;
    *)
        echo "MOCK: Unknown docker compose command: \$1"
        exit 1
        ;;
esac
EOF
chmod +x "$MOCK_BIN_DIR/docker-compose"

# Ensure the log file is clean before tests
> /tmp/docker_compose_calls.log

# Set the compose file path for the entrypoint script during testing
export OASIS_COMPOSE_FILE="src/docker-compose.yml"

echo "Running tests for Nightly Ephemeral Dev Oasis..."

# Test 1: 'up' command
echo "Test 1: 'up' command"
if ! src/entrypoint.sh up; then
    echo "FAIL: 'up' command failed"
    exit 1
fi
grep -q "MOCK: docker compose called with: -f src/docker-compose.yml up -d" /tmp/docker_compose_calls.log || { echo "FAIL: 'up' command did not call 'docker compose up -d'"; exit 1; }
echo "PASS: 'up' command called 'docker compose up -d'"

# Test 2: 'down' command
echo "Test 2: 'down' command"
if ! src/entrypoint.sh down; then
    echo "FAIL: 'down' command failed"
    exit 1
fi
grep -q "MOCK: docker compose called with: -f src/docker-compose.yml down" /tmp/docker_compose_calls.log || { echo "FAIL: 'down' command did not call 'docker compose down'"; exit 1; }
echo "PASS: 'down' command called 'docker compose down'"

# Test 3: 'status' command
echo "Test 3: 'status' command"
output=$(src/entrypoint.sh status)
echo "$output" | grep -q "MOCK: docker compose called with: -f src/docker-compose.yml ps" || { echo "FAIL: 'status' command did not call 'docker compose ps'"; exit 1; }
echo "$output" | grep -q "web running" || { echo "FAIL: 'status' command did not show web status"; exit 1; }
echo "PASS: 'status' command called 'docker compose ps' and showed status"

# Clean up
rm -rf "$MOCK_BIN_DIR"
rm /tmp/docker_compose_calls.log

echo "All tests passed!"
