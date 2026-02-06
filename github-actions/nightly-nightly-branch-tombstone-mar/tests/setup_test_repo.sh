#!/bin/bash

set -euo pipefail

# Create a temporary directory for the test repository
TEST_REPO_DIR="test_repo"
mkdir -p "$TEST_REPO_DIR"
cd "$TEST_REPO_DIR"

# Initialize a git repository
git init -b main > /dev/null 2>&1
git config user.email "test@example.com"
git config user.name "Test User"

# Create initial commit on main
echo "Initial content" > file.txt
git add file.txt
git commit --date="2023-01-01T12:00:00Z" -m "Initial commit" > /dev/null 2>&1

# Create a branch 'feature-new' and make a recent commit (not stale)
git checkout -b feature-new > /dev/null 2>&1
echo "Feature content" > feature.txt
git add feature.txt
# Mock rationale: Using specific dates for commits ensures deterministic staleness calculation.
# This simulates real-world commit history for testing the date logic without external dependencies.
git commit --date="$(date -u -d '5 days ago' +%Y-%m-%dT%H:%M:%SZ)" -m "Recent feature commit" > /dev/null 2>&1

# Create a branch 'bugfix-old' and make an old commit (stale)
git checkout main > /dev/null 2>&1
git checkout -b bugfix-old > /dev/null 2>&1
echo "Bugfix content" > bugfix.txt
git add bugfix.txt
git commit --date="$(date -u -d '40 days ago' +%Y-%m-%dT%H:%M:%SZ)" -m "Old bugfix commit" > /dev/null 2>&1

# Create another stale branch 'feature-forgotten'
git checkout main > /dev/null 2>&1
git checkout -b feature-forgotten > /dev/null 2>&1
echo "Forgotten feature" > forgotten.txt
git add forgotten.txt
git commit --date="$(date -u -d '60 days ago' +%Y-%m-%dT%H:%M:%SZ)" -m "Forgotten feature commit" > /dev/null 2>&1

# Create a branch 'develop' that should be excluded by default
git checkout main > /dev/null 2>&1
git checkout -b develop > /dev/null 2>&1
echo "Develop branch" > develop.txt
git add develop.txt
git commit --date="$(date -u -d '50 days ago' +%Y-%m-%dT%H:%M:%SZ)" -m "Develop branch commit" > /dev/null 2>&1

# Create a branch 'release/v1.0' that should be excluded by pattern
git checkout main > /dev/null 2>&1
git checkout -b release/v1.0 > /dev/null 2>&1
echo "Release branch" > release.txt
git add release.txt
git commit --date="$(date -u -d '70 days ago' +%Y-%m-%dT%H:%M:%SZ)" -m "Release branch commit" > /dev/null 2>&1

# Simulate a remote origin by pushing to a bare repo
cd ..
mkdir -p "remote_origin.git"
cd "remote_origin.git"
git init --bare > /dev/null 2>&1
cd ..

cd "$TEST_REPO_DIR"
git remote add origin ../remote_origin.git > /dev/null 2>&1
git push origin --all > /dev/null 2>&1
git push origin --tags > /dev/null 2>&1

echo "Test repository setup complete in $TEST_REPO_DIR"
