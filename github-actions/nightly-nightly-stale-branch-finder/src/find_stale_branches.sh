#!/bin/bash

set -euo pipefail

GITHUB_TOKEN=$1
DAYS_STALE=$2
IGNORE_BRANCHES_RAW=$3

# Mock rationale: In a real GitHub Actions workflow, these would be provided by environment variables.
# For local testing, we provide sensible defaults.
GITHUB_REPOSITORY=${GITHUB_REPOSITORY:-"octocat/Hello-World"} # Simulates GITHUB_REPOSITORY env var
GITHUB_API_URL=${GITHUB_API_URL:-"https://api.github.com"} # Simulates GitHub API base URL

OWNER=$(echo "$GITHUB_REPOSITORY" | cut -d'/' -f1)
REPO=$(echo "$GITHUB_REPOSITORY" | cut -d'/' -f2)

# Convert comma-separated ignore patterns to a regex pattern
IGNORE_REGEX=""
if [[ -n "$IGNORE_BRANCHES_RAW" ]]; then
    IFS=',' read -ra ADDR <<< "$IGNORE_BRANCHES_RAW"
    for i in "${ADDR[@]}"; do
        # Trim whitespace from pattern
        PATTERN=$(echo "$i" | xargs)
        if [[ -n "$PATTERN" ]]; then
            # If the pattern contains any regex metacharacters, assume it's a full regex.
            # Otherwise, treat it as an exact match by adding anchors.
            if [[ "$PATTERN" =~ [.^$*+?|(){}\[\]\\] ]]; then
                IGNORE_REGEX+="|$PATTERN"
            else
                IGNORE_REGEX+="|^$PATTERN$"
            fi
        fi
    done
    IGNORE_REGEX="${IGNORE_REGEX:1}" # Remove leading '|'
fi

# Function to make API calls (mocked in tests)
github_api_call() {
    local endpoint="$1"
    curl -s -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        "$GITHUB_API_URL/repos/$OWNER/$REPO/$endpoint"
}

# Get all branches
BRANCHES_JSON=$(github_api_call "branches?per_page=100") # Max 100 branches for simplicity

# Check if branches JSON is valid and not empty
if [[ -z "$BRANCHES_JSON" || "$BRANCHES_JSON" == "[]" ]]; then
    echo "[]"
    exit 0
fi

# Parse branch names
# Mock rationale: Use 'jq' for JSON parsing. Assumed to be available in GitHub Actions runners.
BRANCH_NAMES=$(echo "$BRANCHES_JSON" | jq -r '.[].name')

STALE_BRANCHES=()
CURRENT_TIMESTAMP=$(date +%s)
SECONDS_IN_DAY=86400
STALE_THRESHOLD_SECONDS=$((DAYS_STALE * SECONDS_IN_DAY))

for BRANCH_NAME in $BRANCH_NAMES; do
    # Check if branch should be ignored
    if [[ -n "$IGNORE_REGEX" && "$BRANCH_NAME" =~ $IGNORE_REGEX ]]; then
        continue
    }

    # Get the latest commit for the branch
    BRANCH_DETAILS_JSON=$(github_api_call "branches/$BRANCH_NAME")
    
    # Mock rationale: Handle cases where branch details might not be found or API returns error
    if [[ -z "$BRANCH_DETAILS_JSON" || "$(echo "$BRANCH_DETAILS_JSON" | jq -r '.message // empty')" == "Not Found" ]]; then
        echo "::warning::Could not retrieve details for branch '$BRANCH_NAME'. Skipping." >&2
        continue
    fi

    COMMIT_SHA=$(echo "$BRANCH_DETAILS_JSON" | jq -r '.commit.sha')

    # Get commit details to find the commit date
    COMMIT_DETAILS_JSON=$(github_api_call "commits/$COMMIT_SHA")

    # Mock rationale: Handle cases where commit details might not be found or API returns error
    if [[ -z "$COMMIT_DETAILS_JSON" || "$(echo "$COMMIT_DETAILS_JSON" | jq -r '.message // empty')" == "Not Found" ]]; then
        echo "::warning::Could not retrieve commit details for SHA '$COMMIT_SHA' of branch '$BRANCH_NAME'. Skipping." >&2
        continue
    fi

    COMMIT_DATE_ISO=$(echo "$COMMIT_DETAILS_JSON" | jq -r '.commit.committer.date')
    COMMIT_TIMESTAMP=$(date -d "$COMMIT_DATE_ISO" +%s)

    AGE_SECONDS=$((CURRENT_TIMESTAMP - COMMIT_TIMESTAMP))

    if (( AGE_SECONDS > STALE_THRESHOLD_SECONDS )); then
        STALE_BRANCHES+=("\"$BRANCH_NAME\"")
    fi
done

# Output as JSON array
echo "[$(IFS=,; echo "${STALE_BRANCHES[*]}") ]"
