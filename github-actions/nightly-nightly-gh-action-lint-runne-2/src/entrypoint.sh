#!/bin/bash
set -euo pipefail

# Mock rationale: This script is designed to be run within a Docker container provided by GitHub Actions.
# The 'actionlint' binary is expected to be pre-installed in the container image.
# For local testing, we'll use docker-compose to build and run the container with actionlint.

WORKFLOW_PATH=${1:-'**/.github/workflows/*.yml'}

echo "Linting GitHub Actions workflows matching: ${WORKFLOW_PATH}"

# Execute actionlint with the specified path
actionlint "${WORKFLOW_PATH}"

if [ $? -eq 0 ]; then
  echo "All GitHub Actions workflows linted successfully!"
else
  echo "::error::GitHub Actions workflows failed linting. Please check the output above." >&2
  exit 1
fi
