#!/bin/bash

# Define V2 classifier paths
V2_CLASSIFIERS=(
  "python-utils" "rust-utils" "bash-utils" "react-webpage" "github-actions"
  "devops-tools" "docker-tools" "cli-apps" "web-apis" "js-utils" "node-utils"
  "typescript-utils" "data-scripts" "test-suite-tools" "monitoring-scripts"
  "infra-automation" "go-utils" "java-utils" "cpp-utils" "ansible-playbooks"
  "terraform-modules" "k8s-resources" "ci-cd-pipelines" "database-scripts"
  "ml-notebooks" "api-clients"
)

# Read file paths from stdin
readarray -t NEW_FILES

# Keep track of new utility directories found to avoid duplicate errors
declare -A NEW_UTILITY_DIRS

# Function to check if a path is a V2 classifier path
is_v2_classifier_path() {
  local path="$1"
  for classifier in "${V2_CLASSIFIERS[@]}"; do
    if [[ "$path" == "$classifier" ]]; then
      return 0 # True
    fi
  done
  return 1 # False
}

# Function to validate utility name format
validate_util_name() {
  local util_name="$1"
  if [[ ! "$util_name" =~ ^nightly-[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
    echo "::error file=$util_name::Utility name '$util_name' does not follow 'nightly-<kebab-case>' convention." >&2
    return 1
  fi
  return 0
}

EXIT_CODE=0

# Process each new file
for file_path in "${NEW_FILES[@]}"; do
  # Extract the top-level directory (e.g., 'python-utils', 'utils')
  # and the utility name directory (e.g., 'nightly-my-tool')
  
  if [[ "$file_path" =~ ^([^/]+)/([^/]+)/.* ]]; then
    TOP_DIR="${BASH_REMATCH[1]}"
    UTIL_NAME_DIR="${BASH_REMATCH[2]}"

    # If it's a new utility, add it to our tracking and perform checks
    if [[ ! -v NEW_UTILITY_DIRS["$TOP_DIR/$UTIL_NAME_DIR"] ]]; then
      NEW_UTILITY_DIRS["$TOP_DIR/$UTIL_NAME_DIR"]=1 # Mark as seen
      
      # Check for legacy 'utils/' path
      if [[ "$TOP_DIR" == "utils" ]]; then
        echo "::error file=$file_path::New utility '$TOP_DIR/$UTIL_NAME_DIR' found in legacy 'utils/' path. Please move it to a V2 classifier path (e.g., 'python-utils/', 'rust-utils/')." >&2
        EXIT_CODE=1
      elif ! is_v2_classifier_path "$TOP_DIR"; then
        echo "::error file=$file_path::New utility '$TOP_DIR/$UTIL_NAME_DIR' found in an unrecognized top-level directory '$TOP_DIR'. Please use a valid V2 classifier path." >&2
        EXIT_CODE=1
      fi

      # Validate utility name format
      if ! validate_util_name "$UTIL_NAME_DIR"; then
        EXIT_CODE=1
      fi
    fi
  fi
done

if [[ "$EXIT_CODE" == "1" ]]; then
  echo "::error::Path Pioneer Patrol detected violations. Please review the errors above." >&2
  exit 1
else
  echo "::notice::Path Pioneer Patrol: All new utility paths and names adhere to V2 standards. Good job, pioneer!"
fi
