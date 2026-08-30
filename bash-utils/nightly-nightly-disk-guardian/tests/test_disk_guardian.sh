#!/usr/bin/env bash
set -euo pipefail

# Directory of this test script
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create a temporary directory for mock binaries
MOCK_BIN="${TEST_DIR}/mock_bin"
mkdir -p "${MOCK_BIN}"

# Mock df that reads the desired usage from the MOCK_USAGE env var
cat > "${MOCK_BIN}/df" <<'EOF'
#!/usr/bin/env bash
# Mock df: prints a single line with the usage percentage supplied via MOCK_USAGE
# Expected env var MOCK_USAGE like "50%" or "90%"

echo "Filesystem      Size  Used Avail Use% Mounted on"
echo "/dev/root        20G   10G   10G  ${MOCK_USAGE} /"
EOF
chmod +x "${MOCK_BIN}/df"

# Helper to invoke the guardian with a mocked df
run_guardian() {
    local usage=$1   # e.g. "50%"
    local threshold=$2
    MOCK_USAGE="${usage}" PATH="${MOCK_BIN}:$PATH" bash "${TEST_DIR}/../src/disk_guardian.sh" "${threshold}"
}

# ---------- Test 1: usage below threshold ----------
output=$(run_guardian "50%" 80)
expected="✅  Disk usage at 50% – All is calm."
if [[ "$output" != "$expected" ]]; then
    echo "Test 1 failed: expected '$expected', got '$output'"
    exit 1
fi

# ---------- Test 2: usage above threshold ----------
output=$(run_guardian "90%" 80)
# Should start with the warning emoji
if [[ "$output" != ⚠️* ]]; then
    echo "Test 2 failed: expected a warning line, got '$output'"
    exit 1
fi
# Verify that the warning contains one of the known phrases
found=0
for phrase in "The sky darkens as your storage swells!" "Ravens gather over the overflowing bytes." "The digital tide rises, beware the flood." "Your disks whisper of impending doom." "Apocalypse imminent: space runs out!"; do
    if [[ "$output" == *"$phrase"* ]]; then
        found=1
        break
    fi
done
if (( found == 0 )); then
    echo "Test 2 failed: warning phrase not recognized in output '$output'"
    exit 1
fi

echo "All tests passed."
