#!/bin/bash

set -euo pipefail

REPO_FULL_NAME="${GITHUB_REPOSITORY}"
GITHUB_TOKEN="${GITHUB_TOKEN}"
STALE_DAYS="${STALE_DAYS:-30}"
WATERING_MESSAGE="${WATERING_MESSAGE:-This little issue plant looks a bit thirsty! 💧 Any kind gardener willing to give it some attention?}"
LABELS_TO_IGNORE="${LABELS_TO_IGNORE:-}"
DRY_RUN="${DRY_RUN:-false}"
ACTION_LABEL="${ACTION_LABEL:-garden-tender-watered}"

echo "--- Nightly Issue Garden Tender ---"
echo "Repository: ${REPO_FULL_NAME}"
echo "Stale threshold: ${STALE_DAYS} days"
echo "Watering message: ${WATERING_MESSAGE}"
echo "Labels to ignore: ${LABELS_TO_IGNORE}"
echo "Action label: ${ACTION_LABEL}"
echo "Dry run: ${DRY_RUN}"

# Calculate cutoff date
CUTOFF_DATE=$(date -u -d "${STALE_DAYS} days ago" +"%Y-%m-%dT%H:%M:%SZ")
echo "Stale cutoff date (UTC): ${CUTOFF_DATE}"

# Fetch open issues
# Mock rationale: In tests, 'gh' command will be mocked to return predefined JSON.
ISSUES_JSON=$(gh api "repos/${REPO_FULL_NAME}/issues" --jq '.[] | select(.pull_request | not)' --paginate)

if [[ -z "$ISSUES_JSON" || "$ISSUES_JSON" == "[]" ]]; then
  echo "No open issues found or issues JSON is empty. Exiting."
  exit 0
fi

echo "Processing $(echo "$ISSUES_JSON" | jq -c . | wc -l) open issues..."

# Filter stale issues
STALE_ISSUES=$(echo "$ISSUES_JSON" | jq -c --arg cutoff "$CUTOFF_DATE" --arg action_label "$ACTION_LABEL" --arg labels_to_ignore "$LABELS_TO_IGNORE" '
  .[] | select(
    .state == "open" and
    (.updated_at < $cutoff) and
    (.labels | map(.name) | contains([$action_label]) | not) and
    (
      if $labels_to_ignore == "" then true
      else
        # Check if any of the issue\'s labels are in the ignore list
        (
          .labels | map(.name) |
          any(issue_label; ($labels_to_ignore | split(",")) | contains([issue_label]))
        ) | not
      end
    )
  )
')

if [[ -z "$STALE_ISSUES" || "$STALE_ISSUES" == "[]" ]]; then
  echo "No stale issues found that need watering. The garden is well-tended!"
  exit 0
fi

echo "Found $(echo "$STALE_ISSUES" | jq -c . | wc -l) issues needing watering."

# Water the stale issues
echo "$STALE_ISSUES" | jq -c . | while read -r issue; do
  ISSUE_NUMBER=$(echo "$issue" | jq -r '.number')
  ISSUE_TITLE=$(echo "$issue" | jq -r '.title')

  echo "--- Watering issue #${ISSUE_NUMBER}: ${ISSUE_TITLE} ---"

  if [[ "$DRY_RUN" == "true" ]]; then
    echo "DRY RUN: Would have posted comment and added label to issue #${ISSUE_NUMBER}."
  else
    echo "Posting comment to issue #${ISSUE_NUMBER}..."
    # Mock rationale: In tests, 'gh' command will be mocked to simulate API calls.
    gh api "repos/${REPO_FULL_NAME}/issues/${ISSUE_NUMBER}/comments" \
      -f body="${WATERING_MESSAGE}" > /dev/null

    echo "Adding label '${ACTION_LABEL}' to issue #${ISSUE_NUMBER}..."
    # Mock rationale: In tests, 'gh' command will be mocked to simulate API calls.
    gh api "repos/${REPO_FULL_NAME}/issues/${ISSUE_NUMBER}/labels" \
      -f labels[]="${ACTION_LABEL}" > /dev/null

    echo "Successfully watered issue #${ISSUE_NUMBER}."
  fi
done

echo "--- Issue Garden Tending Complete ---"
