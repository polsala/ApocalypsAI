#!/usr/bin/env bash
set -euo pipefail

# Mock gh CLI to avoid network calls
# Mock rationale: gh CLI is mocked to capture calls without contacting GitHub.
MOCK_GH=$(mktemp)
cat <<'EOF' > "$MOCK_GH"
#!/usr/bin/env bash
# Echo the arguments for verification
printf "gh called with: %s\n" "$@"
EOF
chmod +x "$MOCK_GH"

# Prepend mock to PATH so that the script uses it
export PATH="$(dirname "$MOCK_GH"):$PATH"

# Required environment variables for the action
export GITHUB_REPOSITORY="owner/repo"
export GITHUB_PR_NUMBER="42"
export GITHUB_TOKEN="dummy-token"
# Force a deterministic emoji for the test
export FIXED_EMOJI="🚀"

# Run the labeler script
bash "$(dirname "$0")/../src/labeler.sh" > output.txt

# Verify that the script reported the expected label
if grep -q "Added label 🚀 and comment." output.txt; then
  echo "Test passed"
  exit 0
else
  echo "Test failed"
  cat output.txt
  exit 1
fi
