#!/bin/sh -l

# Get inputs
WORKFLOW_PATH="$1"

# Default to .github/workflows/ if no path is provided
if [ -z "$WORKFLOW_PATH" ]; then
  WORKFLOW_PATH=".github/workflows/"
fi

echo "Linting GitHub Actions workflows in: $WORKFLOW_PATH"

# Run yamllint on all YAML files in the specified directory
# --strict: fail on warnings and errors
# --config-file: use a default config if none is found
yamllint --strict --config-file /etc/yamllint/config.yaml "$WORKFLOW_PATH"*.yml

# Check the exit code of yamllint
if [ $? -ne 0 ]; then
  echo "::error::GitHub Actions workflow linting failed. Please check the output above for details."
  exit 1
else
  echo "GitHub Actions workflow linting passed."
fi
