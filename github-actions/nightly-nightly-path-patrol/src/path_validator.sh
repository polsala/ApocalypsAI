#!/bin/bash

PR_NUMBER=$1
GITHUB_TOKEN=$2

if [ -z "$PR_NUMBER" ] || [ -z "$GITHUB_TOKEN" ]; then
  echo "::error::Usage: $0 <PR_NUMBER> <GITHUB_TOKEN>"
  exit 1
fi

export GITHUB_TOKEN # Make token available for 'gh' CLI

echo "Fetching changed files for PR #$PR_NUMBER..."
# Use gh CLI to get added files. Filter for 'added' status.
# Mock rationale: In tests, 'gh' command will be replaced by a mock function/script
# that outputs predefined JSON simulating different PR file changes.
CHANGED_FILES_JSON=$(gh pr view "$PR_NUMBER" --json files --jq '.files[] | select(.status == "added") | .path')

if [ -z "$CHANGED_FILES_JSON" ]; then
  echo "No new files added in PR #$PR_NUMBER. Skipping utility path validation."
  exit 0
fi

echo "Detected added files:"
echo "$CHANGED_FILES_JSON"

# Extract unique potential utility root directories
# A utility root directory is something like 'python-utils/my-util/'
# It must be at least two levels deep (classifier/util_name)
# And contain a '/' after the classifier
UTILITY_ROOTS=""
VALID_CLASSIFIERS="python-utils|rust-utils|bash-utils|react-webpage|github-actions|devops-tools|docker-tools|cli-apps|web-apis|js-utils|node-utils|typescript-utils|data-scripts|test-suite-tools|monitoring-scripts|infra-automation|go-utils|java-utils|cpp-utils|ansible-playbooks|terraform-modules|k8s-resources|ci-cd-pipelines|database-scripts|ml-notebooks|api-clients"

# Read files line by line
while IFS= read -r file; do
  # Check for V2 classifier paths
  if [[ "$file" =~ ^($VALID_CLASSIFIERS)/([^/]+)/.* ]]; then
    CLASSIFIER_PATH="${BASH_REMATCH[1]}"
    UTIL_NAME="${BASH_REMATCH[2]}"
    ROOT_DIR="$CLASSIFIER_PATH/$UTIL_NAME"
    if [[ ! " $UTILITY_ROOTS " =~ " $ROOT_DIR " ]]; then
      UTILITY_ROOTS="$UTILITY_ROOTS $ROOT_DIR"
    fi
  # Also check for legacy 'utils/' path
  elif [[ "$file" =~ ^utils/([^/]+)/.* ]]; then
    UTIL_NAME="${BASH_REMATCH[1]}"
    ROOT_DIR="utils/$UTIL_NAME"
    if [[ ! " $UTILITY_ROOTS " =~ " $ROOT_DIR " ]]; then
      UTILITY_ROOTS="$UTILITY_ROOTS $ROOT_DIR"
    fi
  fi
done <<< "$CHANGED_FILES_JSON"

if [ -z "$UTILITY_ROOTS" ]; then
  echo "No new utility directories detected in added files. Skipping validation."
  exit 0
fi

echo "Detected new utility roots for validation: $UTILITY_ROOTS"

VALIDATION_FAILED=0
for util_root in $UTILITY_ROOTS; do
  echo "--- Validating utility: $util_root ---"
  
  # 1. Check for 'nightly-' prefix
  UTIL_DIR_NAME=$(basename "$util_root")
  if [[ ! "$UTIL_DIR_NAME" =~ ^nightly- ]]; then
    echo "::error file=$util_root::Utility directory '$UTIL_DIR_NAME' must start with 'nightly-'"
    VALIDATION_FAILED=1
  fi

  # 2. Check for README.md
  if [ ! -f "$util_root/README.md" ]; then
    echo "::error file=$util_root::Missing $util_root/README.md"
    VALIDATION_FAILED=1
  fi

  # 3. Check for src/ directory with at least one file
  if [ ! -d "$util_root/src" ] || [ -z "$(find "$util_root/src" -maxdepth 1 -type f -print -quit)" ]; then
    echo "::error file=$util_root::Missing $util_root/src/ directory or it's empty."
    VALIDATION_FAILED=1
  fi

  # 4. Check for tests/ directory with at least one file
  if [ ! -d "$util_root/tests" ] || [ -z "$(find "$util_root/tests" -maxdepth 1 -type f -print -quit)" ]; then
    echo "::error file=$util_root::Missing $util_root/tests/ directory or it's empty."
    VALIDATION_FAILED=1
  fi
  echo "--- Finished validation for $util_root ---"
done

if [ $VALIDATION_FAILED -ne 0 ]; then
  echo "::error::One or more utility validations failed. Please check the logs above."
  exit 1
else
  echo "All new utilities passed path validation!"
fi
