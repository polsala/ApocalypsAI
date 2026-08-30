#!/usr/bin/env sh
set -e

# ---- Mock environment ----
export GITHUB_TOKEN="mock-token"
export LABEL_NAME="post-apocalypse"

# Create a fake event payload for an issue opened on Friday
cat > event.json <<'EOF'
{
  "action": "opened",
  "issue": {
    "number": 42,
    "created_at": "2023-09-01T12:34:56Z"
  },
  "repository": {
    "full_name": "example/repo"
  },
  "number": 42,
  "created_at": "2023-09-01T12:34:56Z",
  "full_name": "example/repo"
}
EOF
export GITHUB_EVENT_PATH="$(pwd)/event.json"

# Mock curl to capture its arguments instead of performing a network request
mock_curl_output=""
mock_curl() {
  # Capture all arguments into a variable for later inspection
  mock_curl_output="$*"
  # Simulate a successful HTTP 201 response
  echo "201"
}
export -f mock_curl

# Replace the real curl with our mock using a wrapper script
# We'll create a temporary directory and prepend it to PATH
TMPDIR=$(mktemp -d)
cat > "$TMPDIR/curl" <<'EOS'
#!/usr/bin/env sh
exec mock_curl "$@"
EOS
chmod +x "$TMPDIR/curl"
export PATH="$TMPDIR:$PATH"

# Run the entrypoint script
sh ./src/entrypoint.sh

# Verify that curl was called with the expected API endpoint and payload
expected_url="https://api.github.com/repos/example/repo/issues/42/labels"
if echo "$mock_curl_output" | grep -q "$expected_url" && echo "$mock_curl_output" | grep -q "\[\"post-apocalypse\"\]"; then
  echo "Test passed: curl invoked with correct URL and payload."
  exit 0
else
  echo "Test failed: curl invocation did not match expectations."
  echo "Captured curl args: $mock_curl_output"
  exit 1
fi
