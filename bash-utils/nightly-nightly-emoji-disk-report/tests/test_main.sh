#!/usr/bin/env bash

# Test for nightly-emoji-disk-report

# Load the script
source "$(dirname "$0")/../src/main.sh"

# Mock get_df_output to return fixed data
mock_df() {
    cat <<EOF
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   10G   38G  21% /
/dev/sda2       100G   70G   25G  75% /home
/dev/sda3       200G  180G   15G  92% /var
/dev/sda4       500G  495G   5G  99% /data
EOF
}

# Override the function
get_df_output() {
    mock_df
}

# Capture output
output=$(main)

# Expected emojis:
# 21% -> 🌱
# 75% -> 🌿
# 92% -> 🌳
# 99% -> 🔥

# Check each line contains correct emoji
if [[ "$output" == *"🌱"*"/dev/sda1"* ]]; then
    echo "PASS: low usage emoji"
else
    echo "FAIL: low usage emoji"
    exit 1
fi

if [[ "$output" == *"🌿"*"/dev/sda2"* ]]; then
    echo "PASS: medium usage emoji"
else
    echo "FAIL: medium usage emoji"
    exit 1
fi

if [[ "$output" == *"🌳"*"/dev/sda3"* ]]; then
    echo "PASS: high usage emoji"
else
    echo "FAIL: high usage emoji"
    exit 1
fi

if [[ "$output" == *"🔥"*"/dev/sda4"* ]]; then
    echo "PASS: critical usage emoji"
else
    echo "FAIL: critical usage emoji"
    exit 1
fi

echo "All tests passed."
