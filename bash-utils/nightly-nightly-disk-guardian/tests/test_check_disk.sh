#!/usr/bin/env bash

# tests for nightly-disk-guardian

set -e

# Create temporary directory for mock commands
TMPDIR=$(mktemp -d)
PATH="$TMPDIR:$PATH"

# Mock df command for high usage scenario (90%)
cat > "$TMPDIR/df" <<'EOF'
#!/usr/bin/env bash
# Mock df output for root filesystem (high usage)
cat <<EOM
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   45G   5G   90% /
EOM
EOF
chmod +x "$TMPDIR/df"

# Run script, expect non‑zero exit and warning containing 90%
if ./src/check_disk.sh >output.txt 2>&1; then
    echo "Expected non-zero exit but got zero"
    exit 1
fi
if ! grep -q "90%" output.txt; then
    echo "Warning message does not contain usage"
    exit 1
fi

# Mock df command for low usage scenario (40%)
cat > "$TMPDIR/df" <<'EOF'
#!/usr/bin/env bash
# Mock df output for root filesystem (low usage)
cat <<EOM
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   20G   30G   40% /
EOM
EOF
chmod +x "$TMPDIR/df"

# Run script, expect zero exit and safe message containing 40%
if ./src/check_disk.sh >output2.txt 2>&1; then
    echo "Low usage test passed"
else
    echo "Expected zero exit but got non-zero"
    exit 1
fi
if ! grep -q "40%" output2.txt; then
    echo "Safe message does not contain usage"
    exit 1
fi

echo "All tests passed"
