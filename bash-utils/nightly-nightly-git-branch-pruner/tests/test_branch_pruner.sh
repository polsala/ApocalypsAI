#!/usr/bin/env bash

# test_branch_pruner.sh
# Automated tests for nightly-git-branch-pruner.
# These tests run entirely offline and use a temporary Git repository.

set -euo pipefail

# Helper: create a temporary directory and clean up on exit
TMPDIR=$(mktemp -d)
cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

cd "$TMPDIR"

git init -q

git config user.email "tester@example.com"

git config user.name "Test User"

# Create an initial commit on main
echo "initial" > README.md
git add README.md
git commit -q -m "initial commit"

# Helper to create a commit with a specific date (epoch seconds)
make_commit() {
  local branch=$1
  local file=$2
  local content=$3
  local epoch=$4
  git checkout -q "$branch"
  echo "$content" > "$file"
  GIT_AUTHOR_DATE="@$epoch" GIT_COMMITTER_DATE="@$epoch" git add "$file"
  GIT_AUTHOR_DATE="@$epoch" GIT_COMMITTER_DATE="@$epoch" git commit -q -m "commit on $branch"
}

# Create an old branch that will be merged
git checkout -q -b old-branch
# Epoch for 40 days ago (40*86400 seconds)
OLD_EPOCH=$(( $(date +%s) - 40 * 86400 ))
make_commit old-branch old.txt "old content" "$OLD_EPOCH"

# Merge old-branch into main
git checkout -q main
git merge -q --no-ff old-branch -m "Merge old-branch"

# Create a recent branch that will NOT be merged
git checkout -q -b recent-branch
RECENT_EPOCH=$(( $(date +%s) - 5 * 86400 ))
make_commit recent-branch recent.txt "recent content" "$RECENT_EPOCH"
# Stay on recent-branch (unmerged)

# ---------- Test 1: Detection only ----------
# Run the script with --days 30 (should list old-branch only)
OUTPUT=$(bash ../../src/branch_pruner.sh --days 30)
# Mock rationale: we expect the output to contain "old-branch" and not "recent-branch"
if [[ "$OUTPUT" != *"old-branch"* ]] || [[ "$OUTPUT" == *"recent-branch"* ]]; then
  echo "Test 1 FAILED: Expected old-branch to be listed and recent-branch to be absent"
  echo "Output was:"
  echo "$OUTPUT"
  exit 1
fi

echo "Test 1 passed: stale branch correctly identified."

# ---------- Test 2: Deletion ----------
# Run the script with --days 30 -d to delete the stale branch
bash ../../src/branch_pruner.sh --days 30 -d > /dev/null
# Verify that old-branch no longer exists
if git branch --list | grep -q "old-branch"; then
  echo "Test 2 FAILED: old-branch was not deleted"
  exit 1
fi
# Ensure recent-branch is still present
if ! git branch --list | grep -q "recent-branch"; then
  echo "Test 2 FAILED: recent-branch disappeared unexpectedly"
  exit 1
fi

echo "Test 2 passed: stale branch successfully deleted."

# ---------- Test 3: No stale branches ----------
# Run with a very small threshold (1 day) – should report none
OUTPUT2=$(bash ../../src/branch_pruner.sh --days 1)
if [[ "$OUTPUT2" != *"No stale merged branches"* ]]; then
  echo "Test 3 FAILED: Expected a message about no stale branches"
  echo "Output was: $OUTPUT2"
  exit 1
fi

echo "Test 3 passed: correctly reports no stale branches when none qualify."

# All tests passed
exit 0
