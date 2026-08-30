#!/usr/bin/env bash
set -e

# Build the Docker image (quietly)
docker build -t nightly-radio-signal-decoder-test . > /dev/null

# Test 1: valid base64 signal
output=$(docker run --rm -e SIGNAL=SGVsbG8gd29ybGQ= nightly-radio-signal-decoder-test)
expected="🔊 Decoded signal: Hello world"
if [ "$output" != "$expected" ]; then
  echo "Test failed: expected '$expected', got '$output'"
  exit 1
fi

# Test 2: missing SIGNAL env var should exit with error
if docker run --rm nightly-radio-signal-decoder-test 2>/dev/null; then
  echo "Test failed: expected error when SIGNAL is missing"
  exit 1
fi

# Test 3: invalid base64 should exit with error
if docker run --rm -e SIGNAL=@@@invalid@@@ nightly-radio-signal-decoder-test 2>/dev/null; then
  echo "Test failed: expected error on invalid base64"
  exit 1
fi

echo "All tests passed"
