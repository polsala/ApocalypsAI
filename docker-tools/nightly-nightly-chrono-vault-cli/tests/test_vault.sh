#!/bin/bash

# Mock rationale: These tests interact with the Docker daemon, which is an external dependency.
# However, the tests are deterministic as they build a specific image and run predefined commands
# within that isolated environment, without relying on external network calls or host-specific
# filesystem state beyond the Docker daemon itself. The "mock" here is the controlled environment
# provided by Docker, ensuring consistent execution.

IMAGE_NAME="chrono-vault-cli-test"
CONTAINER_NAME="chrono-vault-test-instance"
DOCKERFILE_PATH="../src/Dockerfile"
RUN_SCRIPT_PATH="../src/run_vault.sh"

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

function assert_success() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}PASS: $1${NC}"
    else
        echo -e "${RED}FAIL: $1${NC}"
        exit 1
    fi
}

function assert_output_contains() {
    local output="$1"
    local expected_substring="$2"
    local test_name="$3"
    if echo "$output" | grep -q "$expected_substring"; then
        echo -e "${GREEN}PASS: $test_name${NC}"
    else
        echo -e "${RED}FAIL: $test_name (Expected to contain: '$expected_substring', Got: '$output')${NC}"
        exit 1
    fi
}

echo "--- Starting Chrono-Vault CLI Tests ---"

# 1. Ensure Docker is running
docker info > /dev/null 2>&1
assert_success "Docker daemon is running"

# 2. Build the Docker image
echo "Building test image..."
docker build -t "$IMAGE_NAME" -f "$DOCKERFILE_PATH" "$(dirname "$DOCKERFILE_PATH")" > /dev/null 2>&1
assert_success "Docker image '$IMAGE_NAME' built successfully"

# 3. Test if essential tools are present and executable inside the container
echo "Verifying tools inside container..."

# Test nano
OUTPUT=$(docker run --rm "$IMAGE_NAME" bash -c "which nano")
assert_success "nano is present"
assert_output_contains "$OUTPUT" "/usr/bin/nano" "nano path check"

# Test base64
OUTPUT=$(docker run --rm "$IMAGE_NAME" bash -c "echo 'test' | base64")
assert_success "base64 command runs"
assert_output_contains "$OUTPUT" "dGVzdAo=" "base64 encoding"

# Test sha256sum
OUTPUT=$(docker run --rm "$IMAGE_NAME" bash -c "echo 'data' | sha256sum")
assert_success "sha256sum command runs"
assert_output_contains "$OUTPUT" "3a6eb0790f39ac87c94f3856b2dd2c5d110e6811602261a9a9234bb457e81ce2" "sha256sum calculation"

# Test tar
OUTPUT=$(docker run --rm "$IMAGE_NAME" bash -c "which tar")
assert_success "tar is present"
assert_output_contains "$OUTPUT" "/bin/tar" "tar path check"

# Test date
OUTPUT=$(docker run --rm "$IMAGE_NAME" bash -c "date +%Y")
assert_success "date command runs"
assert_output_contains "$OUTPUT" "$(date +%Y)" "date command output (year)" # Compare with host year for determinism

# Test jq
OUTPUT=$(docker run --rm "$IMAGE_NAME" bash -c "echo '{\"key\":\"value\"}' | jq -r .key")
assert_success "jq command runs"
assert_output_contains "$OUTPUT" "value" "jq JSON parsing"

# Test curl
OUTPUT=$(docker run --rm "$IMAGE_NAME" bash -c "which curl")
assert_success "curl is present"
assert_output_contains "$OUTPUT" "/usr/bin/curl" "curl path check"

# 4. Test the run_vault.sh script's 'exec' functionality
echo "Testing run_vault.sh 'exec' command..."
OUTPUT=$("$RUN_SCRIPT_PATH" exec "echo 'Hello from Chrono-Vault!'")
assert_success "run_vault.sh exec command runs"
assert_output_contains "$OUTPUT" "Hello from Chrono-Vault!" "run_vault.sh exec output"

# 5. Clean up: Remove the test image
echo "Cleaning up Docker image..."
docker rmi "$IMAGE_NAME" > /dev/null 2>&1
assert_success "Docker image '$IMAGE_NAME' removed successfully"

echo "--- All Chrono-Vault CLI Tests Passed ---"
