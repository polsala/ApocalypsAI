#!/bin/bash

set -euo pipefail

# --- Inputs ---
WORKFLOW_PATH=${INPUT_WORKFLOW_PATH:-.github/workflows/}
FAIL_IF_NO_WORKFLOWS=${INPUT_FAIL_IF_NO_WORKFLOWS:-false}
VERBOSE=${INPUT_VERBOSE:-false}

# --- Helper Functions ---
log() {
  if [ "$VERBOSE" = "true" ]; then
    echo "[INFO] $1"
  fi
}

error() {
  echo "[ERROR] $1" >&2
  exit 1
}

# --- Main Logic ---

log "Starting GitHub Actions workflow lint check in path: $WORKFLOW_PATH"

# Find all .yml files in the specified path that look like workflow files
# We're looking for files that are likely GitHub Actions workflows, typically in .github/workflows/
WORKFLOW_FILES=$(find "$WORKFLOW_PATH" -type f -name "*.yml" -print)

if [ -z "$WORKFLOW_FILES" ]; then
  log "No YAML files found in $WORKFLOW_PATH."
  if [ "$FAIL_IF_NO_WORKFLOWS" = "true" ]; then
    error "No workflow files found and FAIL_IF_NO_WORKFLOWS is set to true."
  else
    log "Skipping linting as no workflow files were found."
    exit 0
  fi
fi

HAS_ERRORS=false

for workflow_file in $WORKFLOW_FILES;
 do
  log "Linting: $workflow_file"

  # Basic YAML syntax check using 'yamllint' (if available, otherwise skip)
  if command -v yamllint &> /dev/null; then
    log "  Running yamllint..."
    if ! yamllint "$workflow_file"; then
      error "YAML syntax error found in $workflow_file. Please fix."
      HAS_ERRORS=true
    fi
  else
    log "  yamllint not found. Skipping YAML syntax check."
  fi

  # Add more specific GitHub Actions linting rules here
  # Example: Check for missing 'runs-on' in jobs
  if ! grep -q "runs-on:" "$workflow_file"; then
    log "  Potential issue: '$workflow_file' might be missing a 'runs-on' key in its jobs."
    # This is a warning, not a hard error, as some workflows might not have jobs directly
  fi

  # Example: Check for common typos in keywords (e.g., 'on' instead of 'on:')
  if grep -q "^on \(\\|[^:]\)" "$workflow_file"; then
    error "Possible typo detected in '$workflow_file'. Ensure 'on:' is correctly formatted."
    HAS_ERRORS=true
  fi

  # Add more checks as needed. For instance, checking for deprecated features or security best practices.
  # For a comprehensive check, consider integrating with a dedicated GitHub Actions linter if one exists.

done

if [ "$HAS_ERRORS" = "true" ]; then
  error "Linting failed for one or more workflow files."
else
  log "All checked workflow files passed linting."
fi

exit 0
