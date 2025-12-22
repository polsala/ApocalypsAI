#!/bin/bash

# Build the Docker image
echo "Building nightly-docker-ephemeral-runner..."
docker build -t nightly-docker-ephemeral-runner:latest .

if [ $? -eq 0 ]; then
    echo "Build successful!"
    echo "Run './run.sh <owner> <repo> <token>' to start the runner."
else
    echo "Build failed!"
    exit 1
fi
