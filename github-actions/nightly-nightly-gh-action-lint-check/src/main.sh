#!/bin/bash

set -euo pipefail

# Default path to check if not provided
WORKFLOW_PATH=${INPUT_WORKFLOW_PATH:-'.github/workflows/*.yml'}

echo "Checking GitHub Actions workflows at: $WORKFLOW_PATH"

# Install actionlint if not already present (for local testing/execution)
if ! command -v actionlint &> /dev/null
then
    echo "actionlint not found. Installing..."
    # This is a simplified installation for demonstration. In a real action, you'd likely use a pre-built image or a more robust installation method.
    # For this example, we'll assume it's available or can be installed via a package manager.
    # A more robust solution would involve downloading a binary or using a Docker image.
    # For now, we'll just echo a message and proceed, assuming it might be available in the runner environment.
    echo "Please ensure 'actionlint' is available in the environment. For local testing, you might need to install it (e.g., 'brew install actionlint' or 'go install github.com/rhysd/actionlint/cmd/actionlint@latest')."
    # Exit if actionlint is truly not found and we can't proceed.
    if ! command -v actionlint &> /dev/null
then
    echo "Error: actionlint is required but not found. Exiting."
    exit 1
fi
fi

# Find all workflow files matching the pattern
WORKFLOW_FILES=$(find . -path './.github/workflows' -prune -o -name '*.yml' -print | grep -E "$WORKFLOW_PATH")

if [ -z "$WORKFLOW_FILES" ]; then
    echo "No workflow files found matching '$WORKFLOW_PATH'. Skipping linting."
    exit 0
fi

LINT_ERRORS=0

for file in $WORKFLOW_FILES;
do
    echo "Linting: $file"
    if ! actionlint -color=always "$file"; then
        echo "::error file=$file::GitHub Actions workflow linting failed for $file."
        LINT_ERRORS=$((LINT_ERRORS + 1))
    fi
done

if [ "$LINT_ERRORS" -gt 0 ]; then
    echo "::error::Found $LINT_ERRORS linting errors in GitHub Actions workflows. Please fix them."
    exit 1
else
    echo "All GitHub Actions workflows passed linting."
fi
