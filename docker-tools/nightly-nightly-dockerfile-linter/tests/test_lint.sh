#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: we run lint.sh directly to avoid needing Docker in CI.

# Helper function to assert that output contains a given substring
assert_contains() {
  local output="$1"
  local needle="$2"
  if [[ "$output" != *"$needle"* ]]; then
    echo "FAIL: Expected output to contain '$needle'"
    exit 1
  fi
}

# Test 1: Dockerfile with all issues
cat > Dockerfile.test1 <<'EOF'
FROM ubuntu:latest
RUN echo "hello"
EOF

output=$(bash src/lint.sh Dockerfile.test1 || true)
assert_contains "$output" "Avoid using the 'latest' tag"
assert_contains "$output" "No maintainer label"
assert_contains "$output" "No USER instruction"

# Test 2: Good Dockerfile
cat > Dockerfile.test2 <<'EOF'
FROM alpine:3.18
LABEL maintainer="dev@example.com"
USER nonroot
RUN echo "hi"
EOF

output=$(bash src/lint.sh DockerFile.test2 || true) || true
if [[ "$output" != *"No issues found"* ]]; then
  echo "FAIL: Expected no issues"
  exit 1
fi

echo "All tests passed."
