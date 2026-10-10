#!/bin/bash
set -euo pipefail

WORKFLOW_PATH=${INPUT_WORKFLOW_PATH}

echo "Starting GitHub Actions workflow linting in directory: ${WORKFLOW_PATH}"

# Install yamllint if not already present
if ! command -v yamllint &> /dev/null
then
    echo "yamllint not found. Installing..."
    apt-get update && apt-get install -y yamllint
fi

# Find all .yml files in the specified path and lint them
# Using find with -print0 and xargs -0 for robust handling of filenames with spaces or special characters
find "${WORKFLOW_PATH}" -name '*.yml' -print0 | xargs -0 yamllint --strict

if [ $? -eq 0 ]; then
  echo "All GitHub Actions workflows linted successfully!"
else
  echo "Linting errors found in GitHub Actions workflows. Please fix them."
  exit 1
fi
