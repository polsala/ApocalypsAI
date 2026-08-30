#!/usr/bin/env bash

# Tests for nightly-emoji-commit-annotator
# These tests are deterministic and run offline.

set -euo pipefail

# Helper: create a temporary Git repo
setup_repo() {
  REPO_DIR=$(mktemp -d)
  pushd "$REPO_DIR" > /dev/null
  git init -q
  git config user.email "test@example.com"
  git config user.name "Test User"
  echo "Hello" > file.txt
  git add file.txt
  git commit -qm "Initial commit"
}

# Helper: clean up after test
teardown_repo() {
  popd > /dev/null
  rm -rf "$REPO_DIR"
}

# Test 1: Append a specific emoji using -e flag
run_test_specific_emoji() {
  setup_repo
  # Path to the script relative to repository root (adjust if needed)
  SCRIPT_PATH="$(git rev-parse --show-toplevel)/src/annotate.sh"
  bash "$SCRIPT_PATH" -e "🚀"
  NEW_MSG=$(git log -1 --pretty=%B)
  if [[ "$NEW_MSG" != "Initial commit 🚀" ]]; then
    echo "FAIL: Expected 'Initial commit 🚀' but got '$NEW_MSG'"
    exit 1
  fi
  echo "PASS: Specific emoji appended correctly"
  teardown_repo
}

# Test 2: Random emoji is from the allowed list
run_test_random_emoji() {
  setup_repo
  SCRIPT_PATH="$(git rev-parse --show-toplevel)/src/annotate.sh"
  # Force a known RANDOM seed for reproducibility
  RANDOM=42 bash "$SCRIPT_PATH"
  NEW_MSG=$(git log -1 --pretty=%B)
  # Extract the last token (the emoji)
  EMOJI=$(echo "$NEW_MSG" | awk '{print $NF}')
  # List of allowed emojis (must match script's EMOJIS array)
  ALLOWED=("😀" "🚀" "🌟" "🔥" "💡" "🧩" "🎉" "🛠️" "📦" "🧪" "⚡" "🪐" "🤖" "🦄" "🌈")
  FOUND=false
  for e in "${ALLOWED[@]}"; do
    if [[ "$e" == "$EMOJI" ]]; then
      FOUND=true
      break
    fi
  done
  if ! $FOUND; then
    echo "FAIL: Random emoji '$EMOJI' not in allowed list"
    exit 1
  fi
  echo "PASS: Random emoji '$EMOJI' is valid"
  teardown_repo
}

# Execute tests
run_test_specific_emoji
run_test_random_emoji
