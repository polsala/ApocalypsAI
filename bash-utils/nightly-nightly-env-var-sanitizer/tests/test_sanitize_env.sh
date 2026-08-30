#!/usr/bin/env bash

# Mock rationale: set known environment variables, run the sanitizer, and verify redaction.

set -e

# Preserve original environment (not strictly needed for this test)
orig_env=$(env)

# Define test variables
export API_TOKEN="supersecret"
export DB_PASSWORD="hunter2"
export USERNAME="alice"
export PATH="/usr/bin"

# Run the sanitizer and capture output
output=$(bash ../../src/sanitize_env.sh)

# Expected lines
expected_token="API_TOKEN=[REDACTED]"
expected_pass="DB_PASSWORD=[REDACTED]"
expected_user="USERNAME=alice"
expected_path="PATH=/usr/bin"

# Verify each expected line appears exactly once
echo "$output" | grep -Fx "$expected_token"
echo "$output" | grep -Fx "$expected_pass"
echo "$output" | grep -Fx "$expected_user"
echo "$output" | grep -Fx "$expected_path"

# Clean up test variables
unset API_TOKEN DB_PASSWORD USERNAME PATH

# Optionally restore original environment (not required for isolated test)
# export $(printf "%s\0" "$orig_env" | xargs -0 -n1)

echo "All tests passed."
