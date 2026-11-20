#!/bin/sh -l

# Get inputs from environment variables set by GitHub Actions
WORKFLOWS_PATH="${INPUT_WORKFLOWS_PATH}"
FAIL_ON_WARNINGS="${INPUT_FAIL_ON_WARNINGS}"

# Construct the actionlint command
ACTIONLINT_CMD="actionlint"

# Add the workflows path to the command
ACTIONLINT_CMD="${ACTIONLINT_CMD} -f utf-8 ${WORKFLOWS_PATH}"

# Add the fail-on-warnings flag if set
if [ "${FAIL_ON_WARNINGS}" = "true" ]; then
  ACTIONLINT_CMD="${ACTIONLINT_CMD} --fail-on-warnings"
fi

echo "Running command: ${ACTIONLINT_CMD}"

# Execute the command
# The output of actionlint will be printed to the console, and the exit code will determine job success/failure.
${ACTIONLINT_CMD}
