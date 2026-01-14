#!/bin/sh -l

set -euo pipefail

# Parse inputs
PATHS="$1"
EXCLUDE_PATHS="$2"
FAIL_ON_ERROR="$3"

# Set default for fail_on_error if not provided or empty
if [ -z "$FAIL_ON_ERROR" ] || [ "$FAIL_ON_ERROR" = "" ]; then
  FAIL_ON_ERROR="true"
fi

# Construct yamllint command
YAMLLINT_CMD="yamllint"

if [ -n "$PATHS" ] && [ "$PATHS" != "." ]; then
  YAMLLINT_CMD="$YAMLLINT_CMD $PATHS"
fi

if [ -n "$EXCLUDE_PATHS" ]; then
  # yamllint uses --ignore for exclusion
  YAMLLINT_CMD="$YAMLLINT_CMD --ignore $EXCLUDE_PATHS"
fi

# Construct action-validator command
ACTION_VALIDATOR_CMD="action-validator"

if [ -n "$PATHS" ] && [ "$PATHS" != "." ]; then
  ACTION_VALIDATOR_CMD="$ACTION_VALIDATOR_CMD $PATHS"
fi

# Variable to track if any errors occurred
ANY_ERRORS=0

echo "Starting YAML linting..."

# Execute yamllint
if yamllint $PATHS --ignore $EXCLUDE_PATHS; then
  echo "YAML linting passed."
else
  echo "YAML linting failed."
  ANY_ERRORS=1
fi

echo "Starting GitHub Actions workflow validation..."

# Execute action-validator
# action-validator expects paths as arguments, not a single string
# We need to split the PATHS variable if it's not empty and not just '.'
VALIDATOR_PATHS_ARG=""
if [ -n "$PATHS" ] && [ "$PATHS" != "." ]; then
  # Split by space and add each as a separate argument
  for path in $PATHS; do
    VALIDATOR_PATHS_ARG="$VALIDATOR_PATHS_ARG $path"
  done
fi

# action-validator doesn't have a direct exclude option like yamllint, so we'll rely on the paths argument.
# If EXCLUDE_PATHS is critical, a more complex file globbing or filtering would be needed.

# Check if there are any files to validate
if [ -n "$VALIDATOR_PATHS_ARG" ]; then
  if action-validator $VALIDATOR_PATHS_ARG; then
    echo "GitHub Actions workflow validation passed."
  else
    echo "GitHub Actions workflow validation failed."
    ANY_ERRORS=1
  fi
else
  echo "No paths specified for action-validator, skipping."
fi

# Set output status
if [ "$ANY_ERRORS" -eq 0 ]; then
  echo "::set-output name=lint_status::success"
else
  echo "::set-output name=lint_status::failure"
  if [ "$FAIL_ON_ERROR" = "true" ]; then
    echo "Failing workflow due to linting errors."
    exit 1
  fi
fi

exit 0
