#!/bin/bash

# This script checks GitHub Actions workflow files for best practices.
# Arguments: <workflow_file_glob> <output_report_path>

WORKFLOW_GLOB="$1"
REPORT_PATH="$2"

# Initialize report file
> "$REPORT_PATH"

echo "Scanning workflows matching: $WORKFLOW_GLOB"
echo "Scanning workflows matching: $WORKFLOW_GLOB" >> "$REPORT_PATH"

# Collect files into an array to avoid subshell issues with ISSUES_FOUND
# Using 'readarray' (bash 4+) or a loop for older bash. GitHub Actions runners have modern bash.
# 'ls -d' handles glob expansion; '2>/dev/null' suppresses errors if no files match.
readarray -t WORKFLOW_FILES < <(ls -d $WORKFLOW_GLOB 2>/dev/null)

if [ ${#WORKFLOW_FILES[@]} -eq 0 ]; then
  echo "::notice::No workflow files found matching '$WORKFLOW_GLOB'."
  echo "No workflow files found matching '$WORKFLOW_GLOB'." >> "$REPORT_PATH"
  exit 0
fi

ISSUES_FOUND=0

for WF_FILE in "${WORKFLOW_FILES[@]}";
do
  echo "Checking workflow: $WF_FILE"
  echo "Checking workflow: $WF_FILE" >> "$REPORT_PATH"

  # Check 1: Missing 'permissions' block
  if ! grep -q '^permissions:' "$WF_FILE"; then
    echo "::warning file=$WF_FILE::Workflow is missing an explicit 'permissions' block. Consider adding one for security best practices."
    echo "::warning file=$WF_FILE::Workflow is missing an explicit 'permissions' block. Consider adding one for security best practices." >> "$REPORT_PATH"
    ISSUES_FOUND=1
  fi

  # Check 2: Outdated actions/checkout version (v1 or v2)
  if grep -q 'uses: actions/checkout@v[1-2]' "$WF_FILE"; then
    echo "::warning file=$WF_FILE::Found 'actions/checkout@v1' or 'v2'. Consider upgrading to 'actions/checkout@v3' or 'v4' for improved security and features."
    echo "::warning file=$WF_FILE::Found 'actions/checkout@v1' or 'v2'. Consider upgrading to 'actions/checkout@v3' or 'v4' for improved security and features." >> "$REPORT_PATH"
    ISSUES_FOUND=1
  fi

  # Check 3: Missing 'concurrency' for push/pull_request triggers
  # Check if 'on:' block exists and contains 'push' or 'pull_request'
  # AND if 'concurrency:' block does NOT exist at the top level
  if (grep -q 'on:' "$WF_FILE" && (grep -q '  push:' "$WF_FILE" || grep -q '  pull_request:' "$WF_FILE")) && ! grep -q '^concurrency:' "$WF_FILE"; then
    echo "::warning file=$WF_FILE::Workflow triggered by 'push' or 'pull_request' is missing a 'concurrency' group. Consider adding one to prevent redundant runs."
    echo "::warning file=$WF_FILE::Workflow triggered by 'push' or 'pull_request' is missing a 'concurrency' group. Consider adding one to prevent redundant runs." >> "$REPORT_PATH"
    ISSUES_FOUND=1
  fi

done

if [ "$ISSUES_FOUND" -eq 0 ]; then
  echo "::notice::All checked workflows are in harmony!"
  echo "::notice::All checked workflows are in harmony!" >> "$REPORT_PATH"
fi

# The script should always exit 0, as it's a linter/checker, not a build failure.
# The calling workflow can decide to fail based on the report.
exit 0
