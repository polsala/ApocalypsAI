#!/usr/bin/env bash
set -euo pipefail

# Create temporary directory for mock binaries
TMPDIR=$(mktemp -d)
cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

# Mock df script that outputs a fixed table
cat > "$TMPDIR/df" <<'EOF'
#!/usr/bin/env bash
cat <<EOD
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   25G   25G  50% /
/dev/sdb2       100G   80G   20G  80% /data
EOD
EOF
chmod +x "$TMPDIR/df"

# Prepend mock directory to PATH so our script picks it up
export PATH="$TMPDIR:$PATH"

# Run the utility (relative path from tests to src)
output=$(bash ../src/main.sh)

# Expected output
read -r -d '' expected <<'EOM'
/ 50% 🟥🟥🟥🟥🟥⬜⬜⬜⬜⬜
/data 80% 🟥🟥🟥🟥🟥🟥🟥🟥⬜⬜
EOM

# Compare actual vs expected
if [[ "$output" == "$expected" ]]; then
  echo "PASS"
  exit 0
else
  echo "FAIL"
  echo "Got:"
  echo "$output"
  echo "Expected:"
  echo "$expected"
  exit 1
fi
