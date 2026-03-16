#!/bin/bash

DOC_PATHS_INPUT="${{ inputs.doc-paths }}"
CODE_PATHS_INPUT="${{ inputs.code-paths }}"
THRESHOLD_LINES="${{ inputs.threshold-lines }}"
GITHUB_TOKEN="${{ inputs.github-token }}" # Not directly used in this script for API calls, but passed through.

# Mock rationale: In a real PR, GITHUB_BASE_REF and GITHUB_SHA are provided by the GitHub context.
# For testing, the test workflow explicitly sets these environment variables.
BASE_SHA="${GITHUB_BASE_REF}"
HEAD_SHA="${GITHUB_SHA}"

echo "--- Inputs ---"
echo "DOC_PATHS_INPUT: $DOC_PATHS_INPUT"
echo "CODE_PATHS_INPUT: $CODE_PATHS_INPUT"
echo "THRESHOLD_LINES: $THRESHOLD_LINES"
echo "BASE_SHA: $BASE_SHA"
echo "HEAD_SHA: $HEAD_SHA"
echo "----------------"

DOC_CHANGED=false
# Iterate through each documentation pattern
IFS=',' read -ra DOC_PATTERNS_ARRAY <<< "$DOC_PATHS_INPUT"
for doc_pattern in "${DOC_PATTERNS_ARRAY[@]}"; do
  # Check if any file matching the pattern was changed
  # Mock rationale: `git diff` is a real command. For offline testing, the test workflow creates a dummy git repo.
  if git diff --name-only "$BASE_SHA" "$HEAD_SHA" -- "$doc_pattern" | grep -q .; then
    DOC_CHANGED=true
    echo "Documentation file matching '$doc_pattern' was changed."
    break
  fi
done

TOTAL_CODE_LINES_CHANGED=0
# Iterate through each code pattern
IFS=',' read -ra CODE_PATTERNS_ARRAY <<< "$CODE_PATHS_INPUT"
for code_pattern in "${CODE_PATTERNS_ARRAY[@]}"; do
  # Get lines added/deleted for files matching the code pattern
  # Mock rationale: `git diff --numstat` is a real command. For offline testing, the test workflow creates a dummy git repo.
  CODE_CHANGES=$(git diff --numstat "$BASE_SHA" "$HEAD_SHA" -- "$code_pattern" | awk '{ print $1 + $2 }')
  for lines in $CODE_CHANGES; do
    TOTAL_CODE_LINES_CHANGED=$((TOTAL_CODE_LINES_CHANGED + lines))
  done
done

echo "Total code lines changed: $TOTAL_CODE_LINES_CHANGED"
echo "Documentation changed: $DOC_CHANGED"

DRIFT_DETECTED=false
SUGGESTION_COMMENT=""

if [ "$DOC_CHANGED" = false ] && [ "$TOTAL_CODE_LINES_CHANGED" -ge "$THRESHOLD_LINES" ]; then
  DRIFT_DETECTED=true
  SUGGESTION_COMMENT="### ⏱️ Temporal Drift Detected! ⏱️\n\nIt looks like there have been significant code changes (approximately ${TOTAL_CODE_LINES_CHANGED} lines) in this Pull Request, but no corresponding updates to the monitored documentation files (e.g., \`${DOC_PATHS_INPUT}\`).\n\nTo prevent 'temporal drift' and keep our knowledge base fresh, please consider reviewing and updating the relevant documentation. A well-maintained \`README.md\` is a beacon in the wasteland!\n\n_This message is brought to you by the ApocalypsAI Nightly Integrator agent._"
  echo "Potential documentation temporal drift detected!"
else
  echo "No significant documentation temporal drift detected."
fi

echo "drift-detected=$DRIFT_DETECTED" >> "$GITHUB_OUTPUT"
echo "suggestion-comment=$SUGGESTION_COMMENT" >> "$GITHUB_OUTPUT"
