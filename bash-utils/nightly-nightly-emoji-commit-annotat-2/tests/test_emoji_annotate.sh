#!/usr/bin/env bash
set -e

# Mock input representing a handful of conventional‑commit messages
input=$(cat <<'EOF'
fix: correct typo
feat: add new feature
docs: update README
refactor: simplify logic
test: add unit tests
chore: clean up scripts
unknown change
EOF
)

expected=$(cat <<'EOF'
🔧 fix: correct typo
✨ feat: add new feature
📚 docs: update README
♻️ refactor: simplify logic
✅ test: add unit tests
🧹 chore: clean up scripts
💡 unknown change
EOF
)

# Run the utility against the mock input
output=$(echo "$input" | bash src/emoji-annotate.sh)

if [[ "$output" != "$expected" ]]; then
  echo "Test failed"
  echo "Expected:"
  echo "$expected"
  echo "Got:"
  echo "$output"
  exit 1
fi

echo "All tests passed"
