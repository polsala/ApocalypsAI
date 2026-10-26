#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: This script is deliberately simple and uses only bash built‑ins.
# In production the `gh` CLI would be used, but for offline testing we just echo the API call.

# Required environment variables (provided by the composite action)
: "${PR_NUMBER:?Missing PR_NUMBER}"   # Pull request number
: "${PR_TITLE:?Missing PR_TITLE}"     # Pull request title
: "${REPO:?Missing REPO}"             # owner/repo
: "${GITHUB_TOKEN:?Missing GITHUB_TOKEN}" # token (unused in mock)

# Determine label based on title keywords (case‑insensitive)
lower_title=$(echo "$PR_TITLE" | tr '[:upper:]' '[:lower:]')
if [[ "$lower_title" == *"bug"* ]]; then
  label="bug"
elif [[ "$lower_title" == *"feature"* ]]; then
  label="enhancement"
elif [[ "$lower_title" == *"doc"* ]] || [[ "$lower_title" == *"docs"* ]]; then
  label="documentation"
else
  label="needs-triage"
fi

# In a real action we would call the GitHub API, e.g.:
# gh api -X POST "/repos/${REPO}/issues/${PR_NUMBER}/labels" -f labels='["${label}"]'
# For offline deterministic testing we simply echo the intended API request.

echo "Would add label '${label}' to PR #${PR_NUMBER} in repository ${REPO}"
