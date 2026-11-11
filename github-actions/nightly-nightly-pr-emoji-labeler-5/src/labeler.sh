#!/usr/bin/env bash
set -euo pipefail

# List of whimsical emojis
EMOJIS=("🚀" "✨" "🐛" "🎉" "🤖" "🧪" "⚡️" "🌟" "🔥" "💡")

# Choose emoji – deterministic if FIXED_EMOJI is set (used in tests)
if [[ -n "${{FIXED_EMOJI:-}}" ]]; then
  CHOSEN="${{FIXED_EMOJI}}"
else
  INDEX=$((RANDOM % ${#EMOJIS[@]}))
  CHOSEN="${{EMOJIS[$INDEX]}}"
fi

# Add label to the PR
gh api -X POST "/repos/${{GITHUB_REPOSITORY}}/issues/${{GITHUB_PR_NUMBER}}/labels" -f labels="${{CHOSEN}}" -H "Authorization: token ${{GITHUB_TOKEN}}" > /dev/null

# Post a friendly comment
MESSAGE="${{CHOSEN}} PR labeled with ${{CHOSEN}}! Happy coding!"
gh api -X POST "/repos/${{GITHUB_REPOSITORY}}/issues/${{GITHUB_PR_NUMBER}}/comments" -f body="${{MESSAGE}}" -H "Authorization: token ${{GITHUB_TOKEN}}" > /dev/null

echo "Added label ${{CHOSEN}} and comment."
