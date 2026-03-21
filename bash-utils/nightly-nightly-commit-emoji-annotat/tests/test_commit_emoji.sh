#!/usr/bin/env bash
set -euo pipefail

# Create a temporary directory to hold a mock 'git' executable
MOCK_GIT_DIR=$(mktemp -d)
cat > "$MOCK_GIT_DIR/git" <<'EOF'
#!/usr/bin/env bash
# Minimal mock for 'git' used by commit-emoji.sh
if [[ "$1" == "-C" ]]; then
  shift 2  # discard -C and repo argument
fi
if [[ "$1" == "log" ]]; then
  # ignore all other options; output a fixed log
  cat <<EOL
a1b2c3d feat: add new rocket engine
d4e5f6g fix: correct typo in docs
h7i8j9k docs: update README
l0m1n2o chore: clean up temp files
EOL
else
  echo "Unsupported git command" >&2
  exit 1
fi
EOF
chmod +x "$MOCK_GIT_DIR/git"

# Prepend the mock directory to PATH so our script picks it up
export PATH="$MOCK_GIT_DIR:$PATH"

# Execute the utility (the script is located relative to the test file)
output=$(bash src/commit-emoji.sh -n 4 .)

# Expected deterministic output
read -r -d '' expected <<'EOL'
🚀 a1b2c3d feat: add new rocket engine
🐛 d4e5f6g fix: correct typo in docs
📚 h7i8j9k docs: update README
🧹 l0m1n2o chore: clean up temp files
EOL

if [[ "$output" == "$expected" ]]; then
  echo "PASS"
  exit 0
else
  echo "FAIL"
  echo "Got:"
  echo "$output"
  echo "Expected:"
  echo "$expected"
  exit 1
fi
