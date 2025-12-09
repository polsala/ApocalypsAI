#!/bin/bash
# Mock test - actual Docker testing requires running container
# This is a simplified offline test

set -e

# Test 1: Basic response
response=$(curl -s http://localhost:5000/playlist?genre=post-apocalyptic)
if ! echo "$response" | grep -q "tracks"; then
  echo "Test failed: No tracks found in response"
  exit 1
fi

# Test 2: Survival tip validation
if ! echo "$response" | grep -q "water"; then
  echo "Test failed: No water tip found"
  exit 1
fi

# Test 3: Status code
code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/playlist)
if [ "$code" != "200" ]; then
  echo "Test failed: Expected 200, got $code"
  exit 1
fi

echo "All tests passed!"
