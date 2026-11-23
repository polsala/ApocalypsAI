#!/usr/bin/env bash
set -euo pipefail

# ----- Mock GitHub environment -----
export GITHUB_REPOSITORY="owner/repo"
export GITHUB_TOKEN="dummy-token"
export GITHUB_EVENT_PATH="$(mktemp)"
export CURL_CMD="$(pwd)/mock_curl.sh"

# Create a mock pull request event payload (PR #7)
cat > "$GITHUB_EVENT_PATH" <<'EOF'
{
  "pull_request": {
    "number": 7
  }
}
EOF

# ----- Mock curl that records its arguments -----
cat > mock_curl.sh <<'EOF'
#!/usr/bin/env bash
# Append all arguments to a log file for inspection
printf "%s\n" "$@" >> curl_log.txt
EOF
chmod +x mock_curl.sh

# Ensure a clean log file
rm -f curl_log.txt

# ----- Run the action's entrypoint -----
bash "$(pwd)/../src/entrypoint.sh"

# ----- Verify that the expected quote was sent -----
# Quote selection: 7 % 5 = 2 -> third quote in the list
EXPECTED="Keep calm and code on."
if grep -q "$EXPECTED" curl_log.txt; then
  echo "Test passed: expected quote found in curl payload."
  exit 0
else
  echo "Test failed: expected quote not found."
  echo "--- curl_log.txt content ---"
  cat curl_log.txt
  exit 1
fi
