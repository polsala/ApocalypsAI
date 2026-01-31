#!/usr/bin/env bash
# Tests for nightly-emoji-traffic-light

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/src/traffic_light.sh"

# Helper to run the script with environment overrides
run() {
  env "$@" "$SCRIPT_PATH"
}

# Mock loadavg files (Mock rationale: provide deterministic inputs for low, moderate, high load)
mkdir -p "$SCRIPT_DIR/tests/tmp"
cat > "$SCRIPT_DIR/tests/tmp/low" <<'EOF'
0.20 0.15 0.10 1/200 12345
EOF

cat > "$SCRIPT_DIR/tests/tmp/moderate" <<'EOF'
2.00 1.80 1.70 2/200 12345
EOF

cat > "$SCRIPT_DIR/tests/tmp/high" <<'EOF'
5.00 4.80 4.70 3/200 12345
EOF

# Test low load (Mock rationale: CPU_COUNT=4 makes per‑CPU load 0.05 < 0.5)
output=$(run LOADAVG_FILE="$SCRIPT_DIR/tests/tmp/low" CPU_COUNT=4)
expected="Load: 0.20 (per CPU: 0.05) - Status: 🟢 (low)"
[[ "$output" == "$expected" ]]

# Test moderate load (Mock rationale: per‑CPU load 0.50 → yellow)
output=$(run LOADAVG_FILE="$SCRIPT_DIR/tests/tmp/moderate" CPU_COUNT=4)
expected="Load: 2.00 (per CPU: 0.50) - Status: 🟡 (moderate)"
[[ "$output" == "$expected" ]]

# Test high load (Mock rationale: per‑CPU load 1.25 > 1.0 → red)
output=$(run LOADAVG_FILE="$SCRIPT_DIR/tests/tmp/high" CPU_COUNT=4)
expected="Load: 5.00 (per CPU: 1.25) - Status: 🔴 (high)"
[[ "$output" == "$expected" ]]

echo "All tests passed."
