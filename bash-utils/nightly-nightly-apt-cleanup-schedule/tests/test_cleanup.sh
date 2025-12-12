#!/usr/bin/env bash
set -euo pipefail

# Directory of this test script
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load the utility functions
source "${TEST_DIR}/../src/cleanup.sh"

# Create mock `find` that pretends to locate two old .deb files
cat > "${TEST_DIR}/mock_find.sh" <<'EOF'
#!/usr/bin/env bash
# Ignore all arguments; just output two fake .deb paths
printf "%s\n" "/var/cache/apt/archives/old1.deb" "/var/cache/apt/archives/old2.deb"
EOF
chmod +x "${TEST_DIR}/mock_find.sh"

# Create mock `sudo` that records its arguments
cat > "${TEST_DIR}/mock_sudo.sh" <<'EOF'
#!/usr/bin/env bash
# Echo the arguments for verification
printf "sudo called with: %s\n" "$@"
EOF
chmod +x "${TEST_DIR}/mock_sudo.sh"

# Prepend the mock directory to PATH so our script uses the mocks
export PATH="${TEST_DIR}:$PATH"

# ---- Test list_old_debs ----
EXPECTED_DEBS="/var/cache/apt/archives/old1.deb\n/var/cache/apt/archives/old2.deb"
OUTPUT_DEBS=$(list_old_debs 10)
if [[ "$OUTPUT_DEBS" != "$EXPECTED_DEBS" ]]; then
  echo "list_old_debs test FAILED"
  echo "Expected:"
  echo "$EXPECTED_DEBS"
  echo "Got:"
  echo "$OUTPUT_DEBS"
  exit 1
fi

# ---- Test remove_files ----
REMOVE_OUTPUT=$(remove_files "/var/cache/apt/archives/old1.deb" "/var/cache/apt/archives/old2.deb")
if [[ "$REMOVE_OUTPUT" != *"sudo called with: rm -f /var/cache/apt/archives/old1.deb /var/cache/apt/archives/old2.deb"* ]]; then
  echo "remove_files test FAILED"
  echo "Output was: $REMOVE_OUTPUT"
  exit 1
fi

echo "All tests passed"
