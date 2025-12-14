#!/bin/bash

set -euo pipefail

# Inputs
FORBIDDEN_PATTERNS=$(echo "${{ inputs.forbidden_patterns }}" | tr -d '\r')
FAIL_ON_DETECTION=${{ inputs.fail_on_detection }}

echo "Starting Workflow Guard Dog..."

# Function to check for forbidden patterns
check_patterns() {
  local line
  local found_violation=0

  if [ -z "$FORBIDDEN_PATTERNS" ]; then
    echo "No forbidden patterns configured. Skipping check."
    return 0
  fi

  echo "Checking for forbidden patterns..."
  echo "--- Forbidden Patterns ---"
  echo "$FORBIDDEN_PATTERNS"
  echo "--------------------------"

  while IFS= read -r line; do
    if [[ "$line" =~ ^# ]]; then
      continue # Skip comments
    fi
    if grep -qE "$line" <<< "$FORBIDDEN_PATTERNS"; then
      echo "🚨 VIOLATION DETECTED: Pattern '$line' found in forbidden list!"
      found_violation=1
    fi
  done <<< "$FORBIDDEN_PATTERNS"

  return $found_violation
}

# Get the current workflow run's job steps (this is a simplification, real analysis would be more complex)
# In a real-world scenario, you'd likely parse the GitHub API for job logs or use a more sophisticated method.
# For this example, we'll simulate checking the script itself or a hypothetical log file.

# Simulate checking the current script for forbidden patterns
if check_patterns; then
  echo "No forbidden patterns found in the current script. Woof woof! 🐶"
else
  echo "🚨 Forbidden patterns detected in the workflow script!"
  if [ "$FAIL_ON_DETECTION" = "true" ]; then
    echo "Failing workflow as per configuration."
    exit 1
  else
    echo "Workflow will continue, but a warning has been logged."
    # In a real action, you might add a comment to the PR/run here.
  fi
fi

exit 0
