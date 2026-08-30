#!/usr/bin/env bash
set -euo pipefail

# Directory of this script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$DIR")"

# Helper to run ghostbuster with a mock ps output
run_with_mock() {
  local mock_output="$1"
  shift
  local args=("$@")
  local tmpdir
  tmpdir=$(mktemp -d)
  # Create mock ps executable
  cat > "$tmpdir/ps" <<'EOF'
#!/usr/bin/env bash
# Mock ps output
cat <<'MOCK'
EOF
  echo "$mock_output" >> "$tmpdir/ps"
  cat >> "$tmpdir/ps" <<'EOF'
MOCK
EOF
  chmod +x "$tmpdir/ps"
  # Prepend mock directory to PATH and invoke the script
  PATH="$tmpdir:$PATH" "${ROOT}/src/ghostbuster.sh" "${args[@]}"
  rm -rf "$tmpdir"
}

# Test 1: Detect a zombie process (dry run)
output=$(run_with_mock "  PID  PPID S CMD\n 1234  5678 Z sleep 100\n 2345  1    S bash" --dry-run)
if ! echo "$output" | grep -q "1234 5678 sleep"; then
  echo "Test 1 failed: zombie not detected"
  exit 1
fi

# Test 2: No zombie processes (dry run)
output=$(run_with_mock "  PID  PPID S CMD\n 2345  1    S bash" --dry-run)
if ! echo "$output" | grep -q "No zombie processes found."; then
  echo "Test 2 failed: expected no zombies"
  exit 1
fi

echo "All tests passed."
