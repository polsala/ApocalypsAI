#!/bin/bash
set -euo pipefail

echo "Building test Docker image..."
docker build -f tests/Dockerfile.test -t apocalypse-prep-kit-tests .

echo "Running tests in container..."
docker run --rm apocalypse-prep-kit-tests

echo "Tests completed."
