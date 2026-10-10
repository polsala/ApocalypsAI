#!/usr/bin/env bash
# Tests for nightly-mem-guardian

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT_PATH="${SCRIPT_DIR}/src/mem_guardian.sh"

# Helper to run script with a given meminfo file and capture output
run_script() {
  local meminfo_file="$1"
  "$SCRIPT_PATH" "$meminfo_file"
}

# Test case 1: plenty of free memory (≈40% free)
meminfo_high_free=$(mktemp)
cat > "$meminfo_high_free" <<'EOF'
MemTotal:       8000000 kB
MemAvailable:   3500000 kB
EOF

output=$(run_script "$meminfo_high_free")
# Expect happy message
echo "$output" | grep -q "fresh as a morning breeze"
rm -f "$meminfo_high_free"

# Test case 2: low free memory (≈10% free)
meminfo_low_free=$(mktemp)
cat > "$meminfo_low_free" <<'EOF'
MemTotal:       8000000 kB
MemAvailable:    800000 kB
EOF

output=$(run_script "$meminfo_low_free")
# Expect warning message
echo "$output" | grep -q "memory is feeling cramped"
rm -f "$meminfo_low_free"

echo "All tests passed."
