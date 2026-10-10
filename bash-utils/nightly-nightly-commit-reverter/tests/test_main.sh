#!/usr/bin/env bash
set -euo pipefail

# Create temporary directory for repo
TMPDIR=$(mktemp -d)
cd "$TMPDIR"

git init -q

# Configure user
git config user.name "Test User"
git config user.email "test@example.com"

# Initial commit
echo "line1" > file.txt
git add file.txt
git commit -qm "Initial commit"

# Commit with WIP
echo "line2" >> file.txt
git add file.txt
git commit -qm "Add feature WIP"

# Commit without pattern
echo "line3" >> file.txt
git add file.txt
git commit -qm "Add feature stable"

# Another WIP commit
echo "line4" >> file.txt
git add file.txt
git commit -qm "Fix bug WIP"

# Run the utility (script is located one directory up from tests)
../src/main.sh "WIP"

# Verify that two revert commits were added
REVERT_COUNT=$(git log --grep="Revert" --oneline | wc -l | tr -d ' ')
if [[ "$REVERT_COUNT" -ne 2 ]]; then
  echo "Expected 2 revert commits, found $REVERT_COUNT"
  exit 1
fi

# Verify that the latest commit message starts with "Revert"
LATEST_MSG=$(git log -1 --pretty=%B)
if [[ "$LATEST_MSG" != Revert* ]]; then
  echo "Latest commit is not a revert"
  exit 1
fi

echo "All tests passed."
