#!/bin/bash

# Mock rationale: Create a temporary Git repo, simulate commits by multiple authors,
# and verify that the gremlin tracker detects authors exceeding the threshold.

set -e

TEMP_REPO=$(mktemp -d)
SCRIPT_PATH="../src/git_gremlin_tracker.sh"

# Setup mock repo
pushd "$TEMP_REPO" > /dev/null

git init

git config user.name "Alice"
git config user.email "alice@example.com"

# Simulate 12 commits by Alice
for i in {1..12}; do
  echo "Commit $i" > file.txt
  git add file.txt
  git commit -m "Commit $i by Alice"
done

# Switch to Bob
git config user.name "Bob"
git config user.email "bob@example.com"

# Simulate 3 commits by Bob
for i in {1..3}; do
  echo "Bob Commit $i" > bob_file.txt
  git add bob_file.txt
  git commit -m "Commit $i by Bob"
done

popd > /dev/null

# Run tracker with threshold 10
OUTPUT=$("$SCRIPT_PATH" "$TEMP_REPO" 10)

# Assertions
if echo "$OUTPUT" | grep -q "Alice has 12 commits"; then
  echo "PASS: Detected Alice as gremlin."
else
  echo "FAIL: Did not detect Alice as gremlin."
  exit 1
fi

if echo "$OUTPUT" | grep -q "Bob has 3 commits"; then
  echo "FAIL: Incorrectly flagged Bob as gremlin."
  exit 1
else
  echo "PASS: Correctly ignored Bob."
fi

# Cleanup
rm -rf "$TEMP_REPO"

echo "All tests passed."
