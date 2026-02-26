#!/bin/bash

set -euo pipefail

STALE_DAYS="${INPUT_STALE_DAYS:-90}"
REPO_TOKEN="${INPUT_REPO_TOKEN}"
EXCLUDE_BRANCHES_RAW="${INPUT_EXCLUDE_BRANCHES:-main,master,develop,dev}"
MOCK_CURRENT_TIMESTAMP="${MOCK_CURRENT_TIMESTAMP:-}" # For testing

IFS=',' read -r -a EXCLUDE_BRANCHES_ARRAY <<< "$EXCLUDE_BRANCHES_RAW"

# Get current timestamp in seconds since epoch
CURRENT_TIMESTAMP=$(date +%s)
if [[ -n "$MOCK_CURRENT_TIMESTAMP" ]]; then
    CURRENT_TIMESTAMP="$MOCK_CURRENT_TIMESTAMP" # Mock rationale: Allows deterministic testing of staleness calculation.
fi

STALE_THRESHOLD_SECONDS=$(( STALE_DAYS * 24 * 60 * 60 ))

echo "🔍 Whispering to the branches for staleness beyond $STALE_DAYS days..."

# Fetch all remote branches and their last commit dates
# This requires actions/checkout to have fetched the remote with fetch-depth: 0
# Mock rationale: The `git for-each-ref` command is mocked by providing a file with the expected output format in tests.
BRANCH_DATA=$(git for-each-ref --sort=-committerdate refs/remotes/origin/ --format='%(refname:short)|%(committerdate:raw)')

STALE_BRANCHES_COUNT=0
STALE_BRANCHES_REPORT="### 👻 Whispers from the Branch Graveyard 👻\n\n"
STALE_BRANCHES_REPORT+="The following branches have been slumbering for over $STALE_DAYS days:\n\n"
STALE_BRANCHES_REPORT+="| Branch Name | Last Commit | Whimsical Suggestion |\n"
STALE_BRANCHES_REPORT+="|-------------|-------------|----------------------|\n"

while IFS='|' read -r refname committerdate; do
    # Strip "origin/" prefix
    BRANCH_NAME="${refname#origin/}"

    # Skip if it's an excluded branch
    EXCLUDE=false
    for excluded in "${EXCLUDE_BRANCHES_ARRAY[@]}"; do
        if [[ "$BRANCH_NAME" == "$excluded" ]]; then
            EXCLUDE=true
            break
        fi
    done
    if $EXCLUDE; then
        continue
    fi

    LAST_COMMIT_TIMESTAMP=$(echo "$committerdate" | awk '{print $1}') # committerdate:raw gives "timestamp timezone"
    LAST_COMMIT_DATE=$(date -d "@$LAST_COMMIT_TIMESTAMP" "+%Y-%m-%d")

    TIME_DIFFERENCE=$(( CURRENT_TIMESTAMP - LAST_COMMIT_TIMESTAMP ))

    if (( TIME_DIFFERENCE > STALE_THRESHOLD_SECONDS )); then
        STALE_BRANCHES_COUNT=$(( STALE_BRANCHES_COUNT + 1 ))
        
        SUGGESTION=""
        case $(( STALE_BRANCHES_COUNT % 4 )) in
            0) SUGGESTION="Consider re-animating this branch with fresh commits!";;
            1) SUGGESTION="Perhaps it's time to offer this branch to the great code archive.";;
            2) SUGGESTION="The temporal currents suggest this branch is ready for a peaceful merge into the void.";;
            3) SUGGESTION="A forgotten relic! Does it hold ancient wisdom, or merely dust?";;
        esac
        
        STALE_BRANCHES_REPORT+="| \`$BRANCH_NAME\` | $LAST_COMMIT_DATE | $SUGGESTION |\n"
    fi
done <<< "$BRANCH_DATA"

if (( STALE_BRANCHES_COUNT == 0 )); then
    STALE_BRANCHES_REPORT+="No stale branches found. All branches are vibrant and active! ✨\n"
fi

echo "::set-output name=stale-branches-count::$STALE_BRANCHES_COUNT"
echo "::set-output name=stale-branches-report::$STALE_BRANCHES_REPORT"

echo "Report generated."
