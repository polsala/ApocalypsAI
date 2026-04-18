#!/usr/bin/env bash
set -euo pipefail

# Helper to create a temporary event JSON file
create_event() {
  local title="$1"
  cat > "$2" <<'EOF'
{
  "pull_request": {
    "title": "PLACEHOLDER"
  }
}
EOF
  # Replace placeholder with the actual title, properly escaped
  sed -i "s/PLACEHOLDER/$(printf '%s' "$title" | sed 's/"/\\"/g')/" "$2"
}

# Test case: title matches the pattern
EVENT_MATCH=$(mktemp)
create_event "feat: add new feature" "$EVENT_MATCH"
export GITHUB_EVENT_PATH="$EVENT_MATCH"
export INPUT_PATTERN="^feat: .+"
if ! bash "${PWD}/src/lint.sh"; then
  echo "Test failed: expected success for matching title"
  exit 1
fi

# Test case: title does NOT match the pattern
EVENT_FAIL=$(mktemp)
create_event "fix bug" "$EVENT_FAIL"
export GITHUB_EVENT_PATH="$EVENT_FAIL"
export INPUT_PATTERN="^feat: .+"
if bash "${PWD}/src/lint.sh"; then
  echo "Test failed: expected failure for non‑matching title"
  exit 1
fi

# Clean up temporary files
rm -f "$EVENT_MATCH" "$EVENT_FAIL"

echo "All tests passed."
