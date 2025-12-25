#!/usr/bin/env bash
set -euo pipefail

# Mock get_df_output to return predetermined usage
get_df_output() {
    case "$1" in
        /var) echo -e "Filesystem 1024-blocks Used Available Capacity Mounted on\n/dev/sda1 1000000 780000 220000 78% /var";;
        /home) echo -e "Filesystem 1024-blocks Used Available Capacity Mounted on\n/dev/sda2 2000000 1800000 200000 90% /home";;
        *) echo -e "Filesystem 1024-blocks Used Available Capacity Mounted on\n/dev/sda3 500000 250000 250000 50% $1";;
    esac
}

# Create temporary config file
config=$(mktemp)
cat > "$config" <<EOF
/var 75
/home 85
/tmp 60
EOF

# Capture output
output=$(bash "$(dirname "$0")/../src/main.sh" "$config")

# Expected lines
expected1="⚠️  /var is at 78% – beware the wasteland!"
expected2="💀  /home is at 90% – the void beckons!"

# Test assertions
if [[ "$output" != *"$expected1"* ]]; then
    echo "FAIL: missing warning for /var"
    exit 1
fi

if [[ "$output" != *"$expected2"* ]]; then
    echo "FAIL: missing skull warning for /home"
    exit 1
fi

echo "PASS"
rm -f "$config"
