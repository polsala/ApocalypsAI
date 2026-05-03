#!/usr/bin/env bash

# nightly-branch-pruner
# Lists (and optionally deletes) local git branches that have been merged into a base branch.
#
# Options:
#   -b <base>   Base branch to compare against (default: main)
#   -d          Delete the merged branches (dry‑run by default)
#   -r <remote> Remote name to delete remote branches as well (optional)

set -euo pipefail

BASE_BRANCH="main"
DELETE=false
REMOTE=""

while getopts ":b:dr:" opt; do
  case $opt in
    b) BASE_BRANCH="$OPTARG" ;;
    d) DELETE=true ;;
    r) REMOTE="$OPTARG" ;;
    \?) echo "Invalid option: -$OPTARG" >&2; exit 1 ;;
    :)  echo "Option -$OPTARG requires an argument." >&2; exit 1 ;;
  esac
done

# Ensure we are inside a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
  echo "Error: Not a git repository." >&2
  exit 1
fi

# Fetch latest refs for remote branches if a remote is specified
if [[ -n "$REMOTE" ]]; then
  git fetch "$REMOTE" > /dev/null 2>&1 || true
fi

# Get list of merged branches, exclude base, main, master, and the current branch
MERGED_BRANCHES=$(git branch --merged "$BASE_BRANCH" | \
  grep -vE "^\*| $BASE_BRANCH$| master$| main$" | \
  sed 's/^ *//')

if [[ -z "$MERGED_BRANCHES" ]]; then
  echo "No merged branches found (excluding $BASE_BRANCH, main, master)."
  exit 0
fi

if $DELETE; then
  echo "Deleting merged branches:"
  while IFS= read -r branch; do
    echo "  $branch"
    git branch -d "$branch"
    if [[ -n "$REMOTE" ]]; then
      git push "$REMOTE" --delete "$branch" || true
    fi
  done <<< "$MERGED_BRANCHES"
else
  echo "Merged branches (dry‑run):"
  while IFS= read -r branch; do
    echo "  $branch"
  done <<< "$MERGED_BRANCHES"
fi
