#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Inputs from GitHub Action --- 
GITHUB_TOKEN="${GITHUB_TOKEN}"
PR_NUMBER="${PR_NUMBER}"
REPO_FULL_NAME="${REPO_FULL_NAME}"
COMPLIMENT_TYPE="${COMPLIMENT_TYPE}" # Not used in V1, but kept for future expansion

# --- Compliment List ---
# Add more whimsical compliments here!
COMPLIMENTS=(
    "Your code is so clean, it could pass for a freshly polished temporal anomaly detector!"
    "This pull request is a beacon of brilliance in the digital wasteland. Well done!"
    "The elegance of this solution is truly inspiring. Keep up the magnificent work!"
    "You've refactored this like a master artisan crafting a relic from the old world. Superb!"
    "Each line of code here sings a symphony of efficiency and clarity. Bravo!"
    "This feature is so well-implemented, it feels like a gift from a benevolent AI. Thank you!"
    "Your commit history is a testament to your dedication. This PR shines!"
    "The logic here is as robust as a reinforced bunker. Impressive!"
    "This code is more delightful than finding a perfectly preserved snack cache. Excellent!"
    "You've navigated the complexities with the grace of a wasteland whisperer. Fantastic!"
)

# --- Select a random compliment ---
RANDOM_INDEX=$(( RANDOM % ${#COMPLIMENTS[@]} ))
SELECTED_COMPLIMENT="${COMPLIMENTS[$RANDOM_INDEX]}"

# --- Construct GitHub API URL and Payload ---
API_URL="https://api.github.com/repos/${REPO_FULL_NAME}/issues/${PR_NUMBER}/comments"
PAYLOAD=$(jq -n --arg body "$SELECTED_COMPLIMENT" '{body: $body}')

# --- Post the comment to GitHub ---
echo "Posting compliment to PR #${PR_NUMBER} in ${REPO_FULL_NAME}..."
echo "Compliment: \"${SELECTED_COMPLIMENT}\""

curl -s -X POST \
     -H "Authorization: token ${GITHUB_TOKEN}" \
     -H "Accept: application/vnd.github.v3+json" \
     "${API_URL}" \
     -d "${PAYLOAD}"

echo "Compliment posted successfully!"
