#!/usr/bin/env bash
set -euo pipefail

# Create a temporary Git repository
TMP_REPO=$(mktemp -d)
cd "$TMP_REPO"

git init -q
git config user.email "test@example.com"
git config user.name "Test User"

# Create three empty commits with known messages
git commit --allow-empty -m "fix typo" -q
git commit --allow-empty -m "add new feature" -q
git commit --allow-empty -m "bug found" -q

# Write a custom mapping file
cat > map.txt <<'EOF'
fix=🔧
feature=✨
bug=🐞
EOF

# Run the utility (script located two directories up from the test file)
SCRIPT_PATH="../src/main.sh"
OUTPUT=$(bash "$SCRIPT_PATH" -n 3 -m "$PWD/map.txt" -d "$PWD")

# Expected transformed lines
expected1="🔧 typo"
expected2="add new ✨"
expected3="🐞 found"

# Verify each expected line appears in the output
if ! grep -Fq "$expected1" <<< "$OUTPUT"; then
  echo "Test failed: missing '$expected1'"
  exit 1
fi
if ! grep -Fq "$expected2" <<< "$OUTPUT"; then
  echo "Test failed: missing '$expected2'"
  exit 1
fi
if ! grep -Fq "$expected3" <<< "$OUTPUT"; then
  echo "Test failed: missing '$expected3'"
  exit 1
fi

echo "All tests passed"
