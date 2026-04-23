#!/usr/bin/env bash
set -euo pipefail

# Create a temporary directory for an isolated Git repo
TMPDIR=$(mktemp -d)
cd "$TMPDIR"

git init -q

# Helper function to create a commit with a given message
commit_msg() {
  echo "temp" > file.txt
  git add file.txt
  git commit -q -m "$1"
}

# Create a series of commits containing various emojis
commit_msg "Initial commit 🚀"
commit_msg "Fix bug 🐛"
commit_msg "Add feature ✨"
commit_msg "Refactor code 🛠️"
commit_msg "Update docs 📚"
commit_msg "Improve performance 🚀"
commit_msg "Release version 🎉"

# Run the utility against the last 10 commits
output=$(bash ../../src/git-emoji-summary.sh 10)

# Expected lines (emoji, count, bar of '#')
expected=(
  "🚀 2 ##"
  "🐛 1 #"
  "✨ 1 #"
  "🛠️ 1 #"
  "📚 1 #"
  "🎉 1 #"
)

# Verify each expected line appears in the output
for line in "${expected[@]}"; do
  if ! grep -Fq "$line" <<< "$output"; then
    echo "Missing expected line: $line"
    exit 1
  fi
done

echo "All tests passed."
