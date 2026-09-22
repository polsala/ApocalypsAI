#!/bin/bash

# Mock rationale: This test script mocks the file system operations by creating
# temporary directories and files, and then uses standard shell commands
# (grep, cat, test) to verify the content and existence of the generated files.
# It does not interact with Docker daemon or any external services.

set -euo pipefail

# Define the generator script path
GENERATOR_SCRIPT="../src/generate_bag.sh"

# Setup a temporary directory for tests
TEST_DIR=$(mktemp -d -t bugout-bag-test-XXXXXXXX)
echo "Using temporary test directory: $TEST_DIR"

cleanup() {
    echo "Cleaning up temporary test directory: $TEST_DIR"
    rm -rf "$TEST_DIR"
}

trap cleanup EXIT

# Test Case 1: Default generation
echo "--- Running Test Case 1: Default generation ---"
OUTPUT_BAG_DIR="$TEST_DIR/default-bag"
"$GENERATOR_SCRIPT" -o "$OUTPUT_BAG_DIR"

# Verify directory and files exist
test -d "$OUTPUT_BAG_DIR" || { echo "FAIL: Output directory not created."; exit 1; }
test -f "$OUTPUT_BAG_DIR/Dockerfile" || { echo "FAIL: Dockerfile not created."; exit 1; }
test -f "$OUTPUT_BAG_DIR/docker-compose.yml" || { echo "FAIL: docker-compose.yml not created."; exit 1; }
test -f "$OUTPUT_BAG_DIR/run_bag.sh" || { echo "FAIL: run_bag.sh not created."; exit 1; }
test -f "$OUTPUT_BAG_DIR/README.md" || { echo "FAIL: README.md not created."; exit 1; }
test -d "$OUTPUT_BAG_DIR/data" || { echo "FAIL: data directory not created."; exit 1; }

# Verify Dockerfile content (default tools)
grep -q "RUN apk update && apk add --no-cache \\
    git jq curl vim python3" "$OUTPUT_BAG_DIR/Dockerfile" || { echo "FAIL: Dockerfile missing default tools."; exit 1; }
grep -q "FROM alpine/git:latest" "$OUTPUT_BAG_DIR/Dockerfile" || { echo "FAIL: Dockerfile missing base image."; exit 1; }
grep -q "Welcome to your Digital Bugout Bag: my-digital-bag!" "$OUTPUT_BAG_DIR/Dockerfile" || { echo "FAIL: Dockerfile missing welcome message."; exit 1; }

# Verify docker-compose.yml content (default name)
grep -q "services:" "$OUTPUT_BAG_DIR/docker-compose.yml" || { echo "FAIL: docker-compose.yml missing services section."; exit 1; }
grep -q "my-digital-bag:" "$OUTPUT_BAG_DIR/docker-compose.yml" || { echo "FAIL: docker-compose.yml missing default service name."; exit 1; }
grep -q "container_name: my-digital-bag-container" "$OUTPUT_BAG_DIR/docker-compose.yml" || { echo "FAIL: docker-compose.yml missing default container name."; exit 1; }
grep -q "- ./data:/app/data" "$OUTPUT_BAG_DIR/docker-compose.yml" || { echo "FAIL: docker-compose.yml missing volume mount."; exit 1; }

# Verify run_bag.sh content
grep -q "docker-compose build" "$OUTPUT_BAG_DIR/run_bag.sh" || { echo "FAIL: run_bag.sh missing build command."; exit 1; }
grep -q "docker-compose run --rm my-digital-bag /bin/bash" "$OUTPUT_BAG_DIR/run_bag.sh" || { echo "FAIL: run_bag.sh missing run command."; exit 1; }
test -x "$OUTPUT_BAG_DIR/run_bag.sh" || { echo "FAIL: run_bag.sh not executable."; exit 1; }

# Verify README.md content
grep -q "# My Digital Bugout Bag: my-digital-bag" "$OUTPUT_BAG_DIR/README.md" || { echo "FAIL: README.md missing correct title."; exit 1; }
grep -q "git" "$OUTPUT_BAG_DIR/README.md" || { echo "FAIL: README.md missing git tool."; exit 1; }
grep -q "python3" "$OUTPUT_BAG_DIR/README.md" || { echo "FAIL: README.md missing python3 tool."; exit 1; }
echo "Test Case 1 PASSED."

# Test Case 2: Custom tools and name
echo "--- Running Test Case 2: Custom tools and name ---"
CUSTOM_TOOLS="node,npm,yarn"
CUSTOM_NAME="web-dev-bag"
OUTPUT_BAG_DIR_CUSTOM="$TEST_DIR/custom-web-dev-bag"
"$GENERATOR_SCRIPT" -t "$CUSTOM_TOOLS" -n "$CUSTOM_NAME" -o "$OUTPUT_BAG_DIR_CUSTOM"

# Verify Dockerfile content (custom tools)
grep -q "RUN apk update && apk add --no-cache \\
    node npm yarn" "$OUTPUT_BAG_DIR_CUSTOM/Dockerfile" || { echo "FAIL: Dockerfile missing custom tools."; exit 1; }
grep -q "Welcome to your Digital Bugout Bag: web-dev-bag!" "$OUTPUT_BAG_DIR_CUSTOM/Dockerfile" || { echo "FAIL: Dockerfile missing custom welcome message."; exit 1; }

# Verify docker-compose.yml content (custom name)
grep -q "$CUSTOM_NAME:" "$OUTPUT_BAG_DIR_CUSTOM/docker-compose.yml" || { echo "FAIL: docker-compose.yml missing custom service name."; exit 1; }
grep -q "container_name: $CUSTOM_NAME-container" "$OUTPUT_BAG_DIR_CUSTOM/docker-compose.yml" || { echo "FAIL: docker-compose.yml missing custom container name."; exit 1; }

# Verify run_bag.sh content (custom name)
grep -q "docker-compose run --rm $CUSTOM_NAME /bin/bash" "$OUTPUT_BAG_DIR_CUSTOM/run_bag.sh" || { echo "FAIL: run_bag.sh missing custom run command."; exit 1; }

# Verify README.md content (custom name and tools)
grep -q "# My Digital Bugout Bag: $CUSTOM_NAME" "$OUTPUT_BAG_DIR_CUSTOM/README.md" || { echo "FAIL: README.md missing correct custom title."; exit 1; }
grep -q "node" "$OUTPUT_BAG_DIR_CUSTOM/README.md" || { echo "FAIL: README.md missing node tool."; exit 1; }
grep -q "yarn" "$OUTPUT_BAG_DIR_CUSTOM/README.md" || { echo "FAIL: README.md missing yarn tool."; exit 1; }
echo "Test Case 2 PASSED."

echo "All tests PASSED."
