#!/usr/bin/env bash
# Test for nightly-commit-emoji-annotator

set -e

# Mock input
input=$(cat <<'EOF'
feat: add new login flow
fix: correct typo in README
docs: update API docs
chore: clean up old branches
refactor: simplify build script
style: improve formatting
EOF
)

# Expected output
expected=$(cat <<'EOF'
✨ feat: add new login flow
🐛 fix: correct typo in README
📚 docs: update API docs
🧹 chore: clean up old branches
♻️ refactor: simplify build script
🤔 style: improve formatting
EOF
)

# Run the script
output=$(printf "%s\n" "$input" | bash src/commit-emoji.sh)

if [[ "$output" == "$expected" ]]; then
  echo "PASS"
  exit 0
else
  echo "FAIL"
  echo "Expected:"
  echo "$expected"
  echo "Got:"
  echo "$output"
  exit 1
fi
