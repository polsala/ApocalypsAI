#!/usr/bin/env bash

# Test suite for disk-guardian.sh
# Uses a mock df command to simulate different usage scenarios.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
SCRIPT="${SCRIPT_DIR}/disk-guardian.sh"

# Helper to run script with mock df
run_with_mock() {
  local mock_output="$1"
  local threshold="${2:-80}"
  # Create temporary directory for mock
  local tmpdir
  tmpdir=$(mktemp -d)
  # Mock df script
  cat > "${tmpdir}/df" <<'EOF'
#!/usr/bin/env bash
# Mock df: prints provided output
cat "$0.mock"
EOF
  chmod +x "${tmpdir}/df"
  echo "${mock_output}" > "${tmpdir}/df.mock"
  # Prepend mock dir to PATH and run the script
  PATH="${tmpdir}:$PATH" "${SCRIPT}" -t "${threshold}"
  rm -rf "${tmpdir}"
}

# Test case: usage below threshold
output=$(run_with_mock "Filesystem Size Used Avail Use% Mounted on\n/dev/root 100G 50G 50G 50% /")
if [[ "$output" != *"✅ Disk usage at 50% – All is calm."* ]]; then
  echo "Test failed: expected calm message for 50% usage"
  exit 1
fi

# Test case: usage above threshold
output=$(run_with_mock "Filesystem Size Used Avail Use% Mounted on\n/dev/root 100G 90G 10G 90% /")
if [[ "$output" != *"⚠️  Disk usage at 90% –"* ]]; then
  echo "Test failed: expected warning for 90% usage"
  exit 1
fi

echo "All tests passed."
