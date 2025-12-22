#!/bin/bash

# Test script for the ephemeral runner
set -e

echo "Running tests for nightly-docker-ephemeral-runner..."

# Test 1: Check if Dockerfile exists
if [ ! -f "Dockerfile" ]; then
    echo "❌ Dockerfile not found"
    exit 1
fi
echo "✅ Dockerfile exists"

# Test 2: Check if entrypoint script exists and is executable
if [ ! -f "scripts/entrypoint.sh" ]; then
    echo "❌ entrypoint.sh not found"
    exit 1
fi

if [ ! -x "scripts/entrypoint.sh" ]; then
    echo "❌ entrypoint.sh is not executable"
    exit 1
fi
echo "✅ entrypoint.sh exists and is executable"

# Test 3: Check if build script exists and is executable
if [ ! -f "scripts/build.sh" ]; then
    echo "❌ build.sh not found"
    exit 1
fi

if [ ! -x "scripts/build.sh" ]; then
    echo "❌ build.sh is not executable"
    exit 1
fi
echo "✅ build.sh exists and is executable"

# Test 4: Check if run script exists and is executable
if [ ! -f "scripts/run.sh" ]; then
    echo "❌ run.sh not found"
    exit 1
fi

if [ ! -x "scripts/run.sh" ]; then
    echo "❌ run.sh is not executable"
    exit 1
fi
echo "✅ run.sh exists and is executable"

# Test 5: Check Dockerfile syntax (basic check)
if ! grep -q "FROM ubuntu:22.04" Dockerfile; then
    echo "❌ Dockerfile doesn't start with expected base image"
    exit 1
fi
echo "✅ Dockerfile has correct base image"

# Test 6: Check for required scripts in Dockerfile
if ! grep -q "COPY scripts/" Dockerfile; then
    echo "❌ Dockerfile doesn't copy scripts"
    exit 1
fi
echo "✅ Dockerfile copies scripts"

# Test 7: Check for entrypoint in Dockerfile
if ! grep -q "ENTRYPOINT" Dockerfile; then
    echo "❌ Dockerfile doesn't set entrypoint"
    exit 1
fi
echo "✅ Dockerfile sets entrypoint"

# Test 8: Check README exists
if [ ! -f "README.md" ]; then
    echo "❌ README.md not found"
    exit 1
fi
echo "✅ README.md exists"

# Test 9: Check for whimsical exit messages in entrypoint
if ! grep -q "Mission accomplished" scripts/entrypoint.sh; then
    echo "❌ Whimsical exit messages not found"
    exit 1
fi
echo "✅ Whimsical exit messages found"

# Test 10: Check for cleanup function
if ! grep -q "cleanup()" scripts/entrypoint.sh; then
    echo "❌ Cleanup function not found"
    exit 1
fi
echo "✅ Cleanup function found"

echo ""
echo "🎉 All tests passed! The ephemeral runner is ready to go."
echo ""
echo "Next steps:"
echo "1. Run './scripts/build.sh' to build the Docker image"
echo "2. Run './scripts/run.sh <owner> <repo> <token>' to test the runner"
echo ""
echo "Note: For actual testing with GitHub, you'll need a real repository and token."
