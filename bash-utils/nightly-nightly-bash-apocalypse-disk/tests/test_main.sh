#!/usr/bin/env bash
set -euo pipefail

# -------------------------------------------------------------------
# Test for nightly-bash-apocalypse-disk-alert
# -------------------------------------------------------------------
# This test replaces the real `df` with a mock that reports one
# partition at 90% usage. It also forces RANDOM=2 so the selected
# phrase is predictable (index 2 -> "The seas rise!").
# -------------------------------------------------------------------

# Create a temporary directory for mock binaries
MOCK_BIN=$(mktemp -d)

# Mock df script
cat > "$MOCK_BIN/df" <<'EOF'
#!/usr/bin/env bash
cat <<'MOCK'
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   45G   5G  90% /
/dev/sda2        20G   10G  10G  50% /home
MOCK
EOF
chmod +x "$MOCK_BIN/df"

# Prepend mock directory to PATH so our script picks it up
export PATH="$MOCK_BIN:$PATH"

# Force a deterministic RANDOM value (index = 2 % 10 = 2)
RANDOM=2

# Execute the utility (relative path from the test directory)
output=$(bash ../src/main.sh)

expected="The seas rise!"

if [[ "$output" != "$expected" ]]; then
  echo "Test failed: expected '$expected', got '$output'"
  exit 1
fi

echo "Test passed."
