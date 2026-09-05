#!/bin/bash

# Mock rationale: These tests mock the behavior of Docker commands and package managers
# by using dummy files and environment variables. They are deterministic and offline.

set -euo pipefail

# --- Mocking Functions ---

# Mock for yq to simulate parsing YAML
mock_yq() {
  local yaml_content="$1"
  local query="$2"
  echo "$yaml_content" | yq "$query" - 
}

# Mock for apt-get install
mock_apt_get_install() {
  echo "Mock apt-get install: $@"
}

# Mock for curl
mock_curl() {
  local url="$1"
  echo "Mock curl: $url"
  if [[ "$url" == "https://api.github.com/repos/docker/compose/releases/latest" ]]; then
    echo '{"tag_name": "v2.10.0"}'
  elif [[ "$url" == "https://github.com/docker/compose/releases/download/v2.10.0/docker-compose-Linux-x86_64" ]]; then
    echo "Mock docker-compose binary content"
  elif [[ "$url" == "https://deb.nodesource.com/setup_18.x" ]]; then
    echo "Mock nodejs setup script"
  fi
}

# Mock for chmod
mock_chmod() {
  echo "Mock chmod: $@"
}

# Mock for tail -f
mock_tail() {
  echo "Mock tail -f: $@"
}

# --- Test Cases ---

run_test() {
  local test_name="$1"
  local script_content="$2"
  local config_content="$3"
  local expected_output="$4"
  local expected_error="$5"

  echo "Running test: $test_name"

  # Create dummy config file
  echo "$config_content" > env.yaml

  # Mock dependencies
  local original_yq=$(command -v yq)
  local original_apt_get=$(command -v apt-get)
  local original_curl=$(command -v curl)
  local original_chmod=$(command -v chmod)
  local original_tail=$(command -v tail)

  # Replace actual commands with mocks
  alias yq='mock_yq "$config_content"'
  alias apt-get='mock_apt_get_install'
  alias curl='mock_curl'
  alias chmod='mock_chmod'
  alias tail='mock_tail'

  # Execute the script and capture output/error
  local actual_output=$(bash -c "$script_content" 2>&1)
  local exit_code=$?

  # Restore original commands
  unalias yq
  unalias apt-get
  unalias curl
  unalias chmod
  unalias tail
  if [ -n "$original_yq" ]; then alias yq="$original_yq"; fi
  if [ -n "$original_apt_get" ]; then alias apt-get="$original_apt_get"; fi
  if [ -n "$original_curl" ]; then alias curl="$original_curl"; fi
  if [ -n "$original_chmod" ]; then alias chmod="$original_chmod"; fi
  if [ -n "$original_tail" ]; then alias tail="$original_tail"; fi

  # Clean up dummy config file
  rm -f env.yaml

  # Assertions
  if [ "$exit_code" -ne 0 ]; then
    if [ -n "$expected_error" ]; then
      if [[ "$actual_output" == *"$expected_error"* ]]; then
        echo "  PASS: Expected error found."
      else
        echo "  FAIL: Expected error '$expected_error' but got '$actual_output'"
        return 1
      fi
    else
      echo "  FAIL: Script exited with error code $exit_code. Output: $actual_output"
      return 1
    fi
  elif [ -n "$expected_error" ]; then
    echo "  FAIL: Script succeeded but expected error '$expected_error'. Output: $actual_output"
    return 1
  fi

  if [ -n "$expected_output" ]; then
    if [[ "$actual_output" == *"$expected_output"* ]]; then
      echo "  PASS: Expected output found."
    else
      echo "  FAIL: Expected output '$expected_output' not found in '$actual_output'"
      return 1
    fi
  fi

  echo "  PASS: Test '$test_name' completed successfully."
  return 0
}

# --- Script Content ---
SCRIPT_CONTENT=$(cat entrypoint.sh)

# --- Test Case 1: Basic Python Environment ---
CONFIG_PYTHON="
name: python-dev
image: ubuntu:latest
packages:
  - python3
  - python3-pip
  - git
ports:
  - 8000:8000
volumes:
  - .:/app
"

run_test "Basic Python Environment"
  "$SCRIPT_CONTENT"
  "$CONFIG_PYTHON"
  "Installing packages..."
  "Port mappings configured: 8000:8000"
  ""

# --- Test Case 2: Node.js and Docker Compose ---
CONFIG_NODE_COMPOSE="
name: node-web-dev
image: ubuntu:latest
packages:
  - curl
tools:
  - name: nodejs
    version: "18"
  - name: docker-compose
    version: "latest"
"

run_test "Node.js and Docker Compose"
  "$SCRIPT_CONTENT"
  "$CONFIG_NODE_COMPOSE"
  "Installing packages..."
  "Installing nodejs (version: 18)..."
  "Installing docker-compose (version: latest)..."
  ""

# --- Test Case 3: Missing Config File ---
run_test "Missing Config File"
  "$SCRIPT_CONTENT"
  ""
  "Error: Configuration file 'env.yaml' not found or not readable."
  ""

# --- Test Case 4: Empty Config ---
CONFIG_EMPTY="
name: empty-env
"

run_test "Empty Config"
  "$SCRIPT_CONTENT"
  "$CONFIG_EMPTY"
  "Installing packages..."
  "Installing tools..."
  "Setting up port mappings..."
  "Setting up volume mounts..."
  "Environment setup complete!"
  ""

echo "All tests passed!"
exit 0
