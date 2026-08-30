#!/usr/bin/env bash

# Test suite for nightly-branch-pruner
# This script creates a temporary git repository, sets up merged and unmerged branches,
# runs the pruner in dry‑run and delete modes, and checks the expected output.

set -euo pipefail

# Helper to run the script and capture stdout
run_pruner() {
  local args="$1"
  ./src/branch_pruner.sh $args
}

# Create a temporary directory for the repo
TMPDIR=$(mktemp -d)
cd "$TMPDIR"

git init -q

git config user.email "tester@example.com"
git config user.name "Test User"

# Create initial commit on main
echo "initial" > README.md
git add README.md
git commit -q -m "initial commit"

git checkout -b feature-merged -q
echo "feature" > feature.txt
git add feature.txt
git commit -q -m "add feature"

git checkout main -q
git merge --no-ff feature-merged -q -m "merge feature-merged"

# Create a branch that stays unmerged
git checkout -b feature-unmerged -q
echo "unmerged" > unmerged.txt
git add unmerged.txt
git commit -q -m "add unmerged"

git checkout main -q

# ---- Dry‑run test ----
OUTPUT=$(run_pruner "")
# Expect feature-merged to appear, feature-unmerged not to appear
if ! echo "$OUTPUT" | grep -q "feature-merged"; then
  echo "[FAIL] Dry‑run did not list merged branch 'feature-merged'" >&2
  exit 1
fi
if echo "$OUTPUT" | grep -q "feature-unmerged"; then
  echo "[FAIL] Dry‑run incorrectly listed unmerged branch 'feature-unmerged'" >&2
  exit 1
fi

echo "[PASS] Dry‑run lists only merged branches"

# ---- Delete mode test ----
run_pruner "-d"
# After deletion, the merged branch should no longer exist
if git branch --list | grep -q "feature-merged"; then
  echo "[FAIL] Branch 'feature-merged' was not deleted" >&2
  exit 1
fi
# Unmerged branch should still exist
if ! git branch --list | grep -q "feature-unmerged"; then
  echo "[FAIL] Unmerged branch 'feature-unmerged' disappeared unexpectedly" >&2
  exit 1
fi

echo "[PASS] Delete mode removes only merged branches"

# Cleanup
cd /
rm -rf "$TMPDIR"
