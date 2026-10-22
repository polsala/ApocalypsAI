#!/bin/bash

# Configuration
STALE_DAYS=${STALE_DAYS:-60} # Default to 60 days
PROTECTED_BRANCHES=${PROTECTED_BRANCHES:-"main master develop"} # Space-separated list of branches/patterns to ignore
CURRENT_DATE_EPOCH=${CURRENT_DATE_EPOCH:-$(date +%s)} # For testing, can be overridden

# GitHub context
GITHUB_TOKEN=${GITHUB_TOKEN:?GITHUB_TOKEN is required}
REPO_FULL_NAME=${GITHUB_REPOSITORY:?GITHUB_REPOSITORY is required}
REPO_OWNER=$(echo "$REPO_FULL_NAME" | cut -d'/' -f1)
REPO_NAME=$(echo "$REPO_FULL_NAME" | cut -d'/' -f2)

echo "--- Branch Barnacle Banishment Initiated ---"
echo "Repository: $REPO_FULL_NAME"
echo "Stale threshold: $STALE_DAYS days"
echo "Protected branches: $PROTECTED_BRANCHES"
echo "Current epoch: $CURRENT_DATE_EPOCH"

# Set up gh CLI authentication
export GH_TOKEN="$GITHUB_TOKEN"

# Get all branches
# Mock rationale: Simulating git commands to avoid actual repository operations and ensure deterministic tests.
# In a real GitHub Action, this would fetch from the actual repo.
ALL_BRANCHES=$(git ls-remote --heads origin | awk '{print $2}' | sed 's/refs\/heads\///')

for branch in $ALL_BRANCHES; do
    # Skip main/master and protected branches
    IS_PROTECTED=false
    for protected_pattern in $PROTECTED_BRANCHES; do
        if [[ "$branch" == "$protected_pattern" || "$branch" =~ $protected_pattern ]]; then
            IS_PROTECTED=true
            break
        fi
    done
    if $IS_PROTECTED; then
        echo "Skipping protected branch: $branch"
        continue
    fi

    # Get last commit date in epoch seconds
    # Mock rationale: Simulating git commands to avoid actual repository operations and ensure deterministic tests.
    LAST_COMMIT_EPOCH=$(git log -1 --format=%ct "origin/$branch")
    if [ -z "$LAST_COMMIT_EPOCH" ]; then
        echo "Warning: Could not get last commit for branch $branch. Skipping." >&2
        continue
    fi

    # Calculate age in days
    AGE_SECONDS=$((CURRENT_DATE_EPOCH - LAST_COMMIT_EPOCH))
    AGE_DAYS=$((AGE_SECONDS / 86400)) # 60*60*24

    echo "Branch: $branch, Last commit: $(date -d "@$LAST_COMMIT_EPOCH" +%Y-%m-%d), Age: $AGE_DAYS days"

    if (( AGE_DAYS > STALE_DAYS )); then
        echo "  -> Branch '$branch' is stale ($AGE_DAYS days old)."

        # Get last committer
        # Mock rationale: Simulating git commands to avoid actual repository operations and ensure deterministic tests.
        LAST_COMMITTER=$(git log -1 --format=%an "origin/$branch")

        # Check for open PRs
        # Mock rationale: Simulating GitHub CLI interactions to avoid actual API calls and ensure deterministic tests.
        PR_INFO=$(gh pr list --head "$branch" --state open --json number,url 2>/dev/null)

        if [ "$(echo "$PR_INFO" | jq 'length')" -gt 0 ]; then
            PR_NUMBER=$(echo "$PR_INFO" | jq '.[0].number')
            PR_URL=$(echo "$PR_INFO" | jq -r '.[0].url')
            echo "  -> Found open PR #$PR_NUMBER for '$branch'. Adding a whimsical comment."
            COMMENT_BODY="Psst! This branch, \`$branch\`, seems to be gathering a bit of digital dust. Perhaps it's time to give it some love, merge it, or send it off to the great byte-bin in the sky? Just a friendly whisper from the ApocalypsAI Branch Barnacle Banishment squad! $PR_URL"
            # Mock rationale: Simulating GitHub CLI interactions to avoid actual API calls and ensure deterministic tests.
            gh pr comment "$PR_NUMBER" --body "$COMMENT_BODY"
        else
            echo "  -> No open PR for '$branch'. Creating a whimsical issue."
            ISSUE_TITLE="Branch Barnacle Alert! \`$branch\` is feeling neglected."
            ISSUE_BODY="Greetings, @$LAST_COMMITTER! The ApocalypsAI Integrator has noticed that the branch \`$branch\` hasn't seen any activity in over $STALE_DAYS days. It's looking a bit like a forgotten relic in our digital archives. Could you please take a moment to review its purpose? Perhaps it's ready to be merged, rebased, or gracefully retired? Let's keep our repository sparkling!"
            # Mock rationale: Simulating GitHub CLI interactions to avoid actual API calls and ensure deterministic tests.
            gh issue create --title "$ISSUE_TITLE" --body "$ISSUE_BODY"
        fi
    fi
done

echo "--- Branch Barnacle Banishment Complete ---"
