#!/usr/bin/env bash
set -euo pipefail

# Create a temporary Git repository
TMPDIR=$(mktemp -d)
cd "$TMPDIR"

git init -q
git config user.email "test@example.com"
git config user.name "Test User"

# Create a file and make a commit containing a keyword
echo "hello" > file.txt
git add file.txt
git commit -q -m "fix bug in parser"

# Run the utility (relative path assumes repository root layout)
bash ../../src/commit-emoji.sh

# Capture the amended commit message
RESULT=$(git log -1 --pretty=%B)

EXPECTED="🔧 fix bug in parser"

if [[ "$RESULT" == "$EXPECTED" ]]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: expected '$EXPECTED' but got '$RESULT'"
  exit 1
fi
