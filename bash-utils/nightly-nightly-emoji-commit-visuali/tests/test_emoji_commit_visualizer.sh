#!/usr/bin/env bash
# test_emoji_commit_visualizer.sh
# Offline test using a mocked git command.

set -euo pipefail

# Create temporary directory for mock binaries
mock_dir=$(mktemp -d)
cleanup() {
  rm -rf "$mock_dir"
}
trap cleanup EXIT

# Mock git that outputs predetermined commit messages
cat > "$mock_dir/git" <<'EOF'
#!/usr/bin/env bash
# Simple mock of git log for testing
if [[ "$1" == "log" ]]; then
  shift
  # ignore options, just output messages
  cat <<'MOCKMSG'
Fix typo in README
Add new feature X
Remove deprecated API
Refactor module Y
Update docs for Z
Write tests for A
Miscellaneous cleanup
MOCKMSG
else
  echo "Unsupported mock git command" >&2
  exit 1
fi
EOF
chmod +x "$mock_dir/git"

# Prepend mock_dir to PATH
export PATH="$mock_dir:$PATH"

# Expected output
read -r -d '' expected <<'EOF'
🛠️ Fix typo in README
✨ Add new feature X
❌ Remove deprecated API
♻️ Refactor module Y
📚 Update docs for Z
✅ Write tests for A
🔎 Miscellaneous cleanup
EOF

# Run the utility
output=$(bash ../src/emoji_commit_visualizer.sh)

# Compare
if diff <(echo "$output") <(echo "$expected"); then
  echo "Test passed"
  exit 0
else
  echo "Test failed"
  echo "Expected:"
  echo "$expected"
  echo "Got:"
  echo "$output"
  exit 1
fi
