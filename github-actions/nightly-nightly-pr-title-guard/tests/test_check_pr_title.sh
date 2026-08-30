#!/usr/bin/env bash
set -e

# Mock rationale: create a temporary event JSON file for the action to read.
TMP_EVENT=$(mktemp)

# Helper to run the validator
run_validator() {
  python3 ../src/check_pr_title.py --prefix "$1"
}

# Test case 1: title with correct prefix (should succeed)
cat > "$TMP_EVENT" <<'EOF'
{
  "pull_request": {
    "title": "feat: add new feature"
  }
}
EOF
export GITHUB_EVENT_PATH="$TMP_EVENT"
if run_validator "feat:"; then
  echo "PASS: title with correct prefix succeeded"
else
  echo "FAIL: title with correct prefix unexpectedly failed"
  exit 1
fi

# Test case 2: title without required prefix (should fail)
cat > "$TMP_EVENT" <<'EOF'
{
  "pull_request": {
    "title": "fix bug in module"
  }
}
EOF
export GITHUB_EVENT_PATH="$TMP_EVENT"
if run_validator "feat:"; then
  echo "FAIL: title without prefix unexpectedly succeeded"
  exit 1
else
  echo "PASS: title without required prefix correctly failed"
fi

# Clean up
rm "$TMP_EVENT"
