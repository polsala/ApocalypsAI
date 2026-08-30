#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <regex>"
  exit 1
fi

PATTERN=$1

# Get list of commit hashes whose messages match the pattern, oldest first
mapfile -t commits < <(git log --reverse --pretty=format:%H --grep="$PATTERN")

if [[ ${#commits[@]} -eq 0 ]]; then
  echo "No commits matching pattern '$PATTERN' found."
  exit 0
fi

for commit in "${commits[@]}"; do
  # Revert without editing commit message
  git revert --no-edit "$commit"
done

echo "Reverted ${#commits[@]} commit(s)."
