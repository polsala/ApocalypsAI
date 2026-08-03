#!/usr/bin/env bash
set -euo pipefail

# Determine target commit (default HEAD)
TARGET="${1:-HEAD}"

# Get raw commit message
MSG=$(git log -1 --pretty=%B "$TARGET") || {
  echo "Error: not a git repository or invalid commit" >&2
  exit 1
}

# If message already starts with an emoji (basic Unicode range), skip
if [[ "$MSG" =~ ^[[:space:]]*[\x{1F300}-\x{1FAFF}] ]]; then
  echo "Commit already has an emoji. No changes made."
  exit 0
fi

# Lowercase for keyword matching
LOWER=$(echo "$MSG" | tr '[:upper:]' '[:lower:]')

# Choose emoji based on keywords
if grep -qE 'fix|bug|patch' <<<"$LOWER"; then
  EMOJI="🔧"
elif grep -qE 'add|feature|implement' <<<"$LOWER"; then
  EMOJI="✨"
elif grep -qE 'remove|delete|drop' <<<"$LOWER"; then
  EMOJI="❌"
elif grep -qE 'docs?|readme' <<<"$LOWER"; then
  EMOJI="📚"
else
  EMOJI="🛠️"
fi

# New commit message with emoji prefix
NEW_MSG="${EMOJI} ${MSG}"

# Amend the commit preserving author/date
git commit --amend -m "$NEW_MSG" --no-edit --allow-empty

echo "Emoji added: $EMOJI"
