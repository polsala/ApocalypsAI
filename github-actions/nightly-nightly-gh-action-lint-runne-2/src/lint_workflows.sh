#!/bin/bash

set -euo pipefail

# Default path for workflows
WORKFLOW_PATH=${1:-.github/workflows/}

echo "Linting GitHub Actions workflows in: $WORKFLOW_PATH"

# Check if yamllint is installed
if ! command -v yamllint &> /dev/null
then
    echo "Error: yamllint is not installed. Please install it using 'pip install yamllint'." >&2
    exit 1
fi

# Find all .yml files in the specified directory and its subdirectories
WORKFLOW_FILES=$(find "$WORKFLOW_PATH" -type f -name '*.yml')

if [ -z "$WORKFLOW_FILES" ]; then
    echo "No workflow files found in $WORKFLOW_PATH. Exiting."
    exit 0
fi

# Run yamllint on all found workflow files
# The --strict flag ensures that even minor warnings cause a non-zero exit code.
# The --config-file option can be used to specify a custom .yamllint config.
if yamllint --strict $WORKFLOW_FILES; then
    echo "All GitHub Actions workflows passed linting!"
else
    echo "Error: One or more GitHub Actions workflows failed linting. Please check the output above." >&2
    exit 1
fi
