#!/bin/bash

# Check if we have the right number of arguments
if [ $# -ne 3 ]; then
    echo "Usage: $0 <github-owner> <github-repo> <github-token>"
    echo "Example: $0 myorg myrepo abc123def456"
    exit 1
fi

GITHUB_OWNER=$1
GITHUB_REPO=$2
GITHUB_TOKEN=$3

# Run the Docker container
echo "Starting ephemeral runner for $GITHUB_OWNER/$GITHUB_REPO..."
docker run --rm \
    -e GITHUB_OWNER="$GITHUB_OWNER" \
    -e GITHUB_REPO="$GITHUB_REPO" \
    -e GITHUB_TOKEN="$GITHUB_TOKEN" \
    -e RUNNER_NAME="ephemeral-$(date +%s)" \
    nightly-docker-ephemeral-runner:latest
