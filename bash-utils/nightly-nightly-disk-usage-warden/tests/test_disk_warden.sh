#!/usr/bin/env bash
set -euo pipefail

SCRIPT="../src/disk_warden.sh"

run_test() {
  local name="$1"
  local mock_file="$2"
  local expected="$3"
  output=$($SCRIPT "$mock_file")
  if [[ "$output" == "$expected" ]]; then
    echo "PASS $name"
  else
    echo "FAIL $name"
    echo "Expected: $expected"
    echo "Got: $output"
    exit 1
  fi
}

# Create temporary directory for mock files
TMPDIR=$(mktemp -d)

cat >"$TMPDIR/low.txt" <<'EOF'
Filesystem Size Used Avail Use% Mounted on
/dev/sda1 100G 30G 70G 30% /
EOF

cat >"$TMPDIR/warn.txt" <<'EOF'
Filesystem Size Used Avail Use% Mounted on
/dev/sda1 100G 85G 15G 85% /
EOF

cat >"$TMPDIR/crit.txt" <<'EOF'
Filesystem Size Used Avail Use% Mounted on
/dev/sda1 100G 95G 5G 95% /
EOF

run_test "low usage" "$TMPDIR/low.txt" "✅ All clear: Disk usage at 30%."
run_test "warning usage" "$TMPDIR/warn.txt" "⚠️ Warning: Disk usage at 85%. Consider cleaning up."
run_test "critical usage" "$TMPDIR/crit.txt" "🚨 Critical: Disk usage at 95%! Time to evacuate the data vault!"

rm -rf "$TMPDIR"

exit 0
