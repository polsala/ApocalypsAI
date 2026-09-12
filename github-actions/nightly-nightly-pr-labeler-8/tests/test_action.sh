#!/usr/bin/env bash
set -euo pipefail

# Mock gh command to avoid real network calls
gh() {
  if [[ "$1" == "api" ]]; then
    shift
    case "$1" in
      "repos/owner/repo/pulls/42/files")
        cat <<'EOF'
[
  {"filename":"docs/README.md"},
  {"filename":"src/main.go"},
  {"filename":"tests/test_main.go"}
]
EOF
        ;;
      "repos/owner/repo/issues/42/labels")
        # Simulate successful label addition
        echo "Labels added"
        ;;
      *)
        echo "Unexpected gh api call: $*" >&2
        exit 1
        ;;
    esac
  else
    echo "Unexpected gh command: $*" >&2
    exit 1
  fi
}

# Export required environment variables for the script
export GITHUB_REPOSITORY="owner/repo"
export GITHUB_REF="refs/pull/42/merge"
export GITHUB_EVENT_PATH="/dev/null"
export GITHUB_TOKEN="dummy-token"
export LABEL_MAPPING='{"docs/**":"documentation","src/**":"code","tests/**":"tests"}'

# Run the labeler script (relative path from test directory)
bash "$(dirname "$0")/../src/labeler.sh" > output.txt

# Verify that the expected labels were reported
if grep -q "Added labels: documentation code tests" output.txt; then
  echo "Test passed"
  exit 0
else
  echo "Test failed"
  cat output.txt
  exit 1
fi
