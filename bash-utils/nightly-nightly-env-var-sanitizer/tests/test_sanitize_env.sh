#!/usr/bin/env bash

# test_sanitize_env.sh
# Tests for nightly‑env‑var‑sanitizer

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
SCRIPT_PATH="$SCRIPT_DIR/../src/sanitize_env.sh"

# Helper to create a temporary file and ensure cleanup
mktemp_file() {
  local tmp=$(mktemp)
  echo "$tmp"
}

# Mock rationale: we use deterministic input strings; no external dependencies.

# Test 1: Basic redaction
input_content="""
# Sample .env file
DB_HOST=localhost
DB_USER=admin
DB_PASSWORD=supersecret
API_KEY=abcd1234
NORMAL_VAR=hello
"""
expected_output="""
# Sample .env file
DB_HOST=localhost
DB_USER=admin
DB_PASSWORD=***REDACTED***
API_KEY=***REDACTED***
NORMAL_VAR=hello
"""

input_file=$(mktemp_file)
output_file=$(mktemp_file)

echo "$input_content" > "$input_file"

# Run the sanitizer, writing to a file
bash "$SCRIPT_PATH" -o "$output_file" "$input_file"

# Compare output
if diff -u <(echo "$expected_output") "$output_file"; then
  echo "Test 1 passed"
else
  echo "Test 1 failed"
  exit 1
fi

# Test 2: Stdout mode and handling of comments/blank lines
input_content2="""
# Comment line

SECRET_TOKEN=xyz
PUBLIC_VAR=public
"""
expected_output2="""
# Comment line

SECRET_TOKEN=***REDACTED***
PUBLIC_VAR=public
"""

echo "$input_content2" > "$input_file"

# Capture stdout
actual_output=$(bash "$SCRIPT_PATH" "$input_file")

if diff -u <(echo "$expected_output2") <(echo "$actual_output"); then
  echo "Test 2 passed"
else
  echo "Test 2 failed"
  exit 1
fi

# Cleanup
rm -f "$input_file" "$output_file"

echo "All tests passed"
