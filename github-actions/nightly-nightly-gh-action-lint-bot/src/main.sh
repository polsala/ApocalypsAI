#!/bin/bash

set -euo pipefail

# --- Configuration ---
# Path to the directory containing GitHub Actions workflows
WORKFLOWS_DIR=".github/workflows"

# --- Helper Functions ---
log_info() {
  echo "\033[0;32m[INFO]\033[0m $1"
}

log_warn() {
  echo "\033[0;33m[WARN]\033[0m $1"
}

log_error() {
  echo "\033[0;31m[ERROR]\033[0m $1"
}

# --- Main Logic ---

log_info "Starting GitHub Actions workflow linting..."

# Check if workflows directory exists
if [ ! -d "$WORKFLOWS_DIR" ]; then
  log_warn "No workflows directory found at '$WORKFLOWS_DIR'. Skipping linting."
  exit 0
fi

# Find all YAML files in the workflows directory
WORKFLOW_FILES=$(find "$WORKFLOWS_DIR" -name "*.yml" -o -name "*.yaml")

if [ -z "$WORKFLOW_FILES" ]; then
  log_warn "No YAML workflow files found in '$WORKFLOWS_DIR'. Skipping linting."
  exit 0
fi

TOTAL_ERRORS=0

for workflow_file in $WORKFLOW_FILES;
do
  log_info "Linting: $workflow_file"
  FILE_ERRORS=0

  # 1. YAML Syntax Check (using yq for robustness)
  if ! yq eval '.' "$workflow_file" > /dev/null 2>&1;
  then
    log_error "  - Invalid YAML syntax."
    ((FILE_ERRORS++))
    ((TOTAL_ERRORS++))
    continue # Skip further checks if syntax is invalid
  fi

  # 2. Basic Structure and Keyword Checks
  if ! grep -q "^name:" "$workflow_file"; then
    log_error "  - Missing 'name:' at the top level."
    ((FILE_ERRORS++))
    ((TOTAL_ERRORS++))
  fi

  # Check for common event triggers (add more as needed)
  if ! grep -qE "^on:" "$workflow_file"; then
    log_warn "  - Missing 'on:' trigger. Workflows should have a trigger."
    # Not a hard error, but a warning
  fi

  # 3. Action Versioning Check
  # Find lines that look like 'uses: actions/checkout@v3' or 'uses: docker/build-push-action@v2'
  # Exclude comments and lines that are not actual 'uses' statements
  if grep -vE '^#.*' "$workflow_file" | grep -qE "uses: actions/[^@]+@"; then
    # This is a basic check. More sophisticated checks might be needed for specific actions.
    # For now, we'll just warn if any action is found without an explicit version.
    # A more robust check would parse the YAML and check each 'uses' entry.
    # For simplicity, we'll assume if 'uses:' is present, it *should* have a version.
    # This is a heuristic and might have false positives/negatives.
    if ! grep -vE '^#.*' "$workflow_file" | grep -qE "uses: actions/[^@]+@[0-9.]+"; then
      log_warn "  - Potential missing version tag for an 'actions/*' step. Consider pinning to a specific version (e.g., @v3).
      This is a heuristic and might not catch all cases. Review manually."
      # Not a hard error, but a strong warning.
    fi
  fi

  # 4. Avoidance of Hardcoded Secrets (basic check)
  # This is a very basic check and can be easily bypassed. A more robust solution would involve secrets scanning tools.
  if grep -q "secrets\." "$workflow_file"; then
    log_warn "  - Found 'secrets.' usage. Ensure these are properly scoped and not hardcoded sensitive values."
    # This is a warning, as using secrets is often necessary, but needs careful handling.
  fi

  # 5. Check for empty jobs or steps
  if grep -qE '^jobs:' "$workflow_file"; then
    if ! grep -qE '^jobs:.*$' "$workflow_file"; then
      log_warn "  - 'jobs:' section appears to be empty or malformed."
    fi
    # Check for empty steps within jobs
    grep -E '^\s+steps:' "$workflow_file" | while read -r line; do
      job_name=$(echo "$line" | sed -E 's/^\s+steps:.*//' | sed -E 's/.*jobs: \*?([^:]+):.*/\1/')
