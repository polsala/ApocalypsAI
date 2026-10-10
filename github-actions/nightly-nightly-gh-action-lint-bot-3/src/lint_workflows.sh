#!/bin/bash

set -euo pipefail

# --- Configuration ---
WORKFLOW_PATH=${1:-.github/workflows/*.yml}
FAIL_ON_ERROR=${2:-false}

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

# Function to create GitHub Actions annotations
# Usage: create_annotation "$level" "$file" "$line" "$message"
create_annotation() {
    local level="$1"
    local file="$2"
    local line="$3"
    local message="$4"

    # GitHub Actions expects specific format for annotations
    # See: https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-annotation
    echo "::$level file=$file,line=$line::$message"
}

# --- Main Logic ---

log_info "Starting GitHub Actions workflow linting for: $WORKFLOW_PATH"

# Find all workflow files matching the pattern
workflow_files=$(find . -path "./.github/workflows" -prune -o -name "*.yml" -print | grep -E "$WORKFLOW_PATH")

if [ -z "$workflow_files" ]; then
    log_warn "No workflow files found matching '$WORKFLOW_PATH'. Skipping linting."
    exit 0
fi

error_count=0

for workflow_file in $workflow_files;
do
    log_info "Linting file: $workflow_file"

    # 1. Basic YAML Syntax Check (using yamllint if available, otherwise a simple check)
    if command -v yamllint &> /dev/null;
    then
        yamllint "$workflow_file" || {
            log_error "YAML syntax errors found in $workflow_file."
            # yamllint output is usually informative enough, but we can add a generic annotation
            create_annotation "failure" "$workflow_file" "1" "YAML syntax error detected. See yamllint output for details."
            ((error_count++))
        }
    else
        log_warn "yamllint not found. Performing basic YAML structure check."
        # Simple check for empty file or missing top-level keys
        if [ ! -s "$workflow_file" ]; then
            create_annotation "failure" "$workflow_file" "1" "Workflow file is empty."
            ((error_count++))
        elif ! grep -qE "^name:" "$workflow_file" && ! grep -qE "^on:" "$workflow_file"; then
            create_annotation "failure" "$workflow_file" "1" "Workflow file appears to be missing 'name' or 'on' key at the top level."
            ((error_count++))
        fi
    fi

    # 2. Common Workflow Pattern Checks
    # Check for missing 'jobs' section
    if ! grep -qE "^jobs:" "$workflow_file"; then
        create_annotation "failure" "$workflow_file" "1" "Workflow is missing the 'jobs:' section."
        ((error_count++))
    fi

    # Check for jobs without steps
    # This is a bit more complex, requires parsing or more advanced grep
    # For simplicity, we'll check for lines starting with '  - name:' within indented job blocks
    # This is a heuristic and might have false positives/negatives
    if grep -qE "^    [a-zA-Z0-9_-]+:$" "$workflow_file" | grep -vE "^      #" | grep -vE "^      - name:"; then
        # This is a very basic check. A more robust solution would involve a YAML parser.
        # We're looking for job definitions that don't immediately have steps.
        # This heuristic might flag comments or other indented lines.
        # A better approach would be to parse the YAML structure.
        log_warn "Potentially missing steps in a job within $workflow_file. Manual review recommended."
        # We won't fail on this heuristic warning by default.
    fi

    # Check for common insecure practices (e.g., hardcoded secrets - very basic check)
    if grep -qE "secrets\.[a-zA-Z0-9_]+" "$workflow_file" && ! grep -qE "secrets\.GITHUB_TOKEN" "$workflow_file"; then
        # This is a very naive check. It might flag legitimate uses of custom secrets.
        # A more sophisticated check would involve context or a secrets scanner.
        create_annotation "warning" "$workflow_file" "1" "Potential use of sensitive secrets detected. Ensure they are managed securely."
    fi

    # Check for deprecated 'master' branch in 'on: push:' or 'on: pull_request:'
    if grep -qE "on:" "$workflow_file"; then
        if grep -qE "branches?: \[.*master\s*(\,.*)?\]" "$workflow_file" || grep -qE "branches?: .*master" "$workflow_file"; then
            create_annotation "warning" "$workflow_file" "1" "Usage of 'master' branch detected in 'on:' triggers. Consider using 'main' or other branch protection rules."
        fi
    fi

    # Add more checks here as needed...

done

if [ "$error_count" -gt 0 ] && [ "$FAIL_ON_ERROR" = "true" ]; then
    log_error "Linting failed with $error_count errors. Failing the job."
    exit 1
elif [ "$error_count" -gt 0 ]; then
    log_warn "Linting found $error_count issues. Review annotations for details."
else
    log_info "Workflow linting completed successfully. No critical issues found."
fi

exit 0
