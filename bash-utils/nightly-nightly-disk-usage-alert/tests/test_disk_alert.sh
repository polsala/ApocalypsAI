#!/usr/bin/env bash
set -euo pipefail

# Mock df output with two filesystems, one exceeding the default 80% threshold
export DF_OUTPUT=$'Filesystem Size Used Avail Use% Mounted on\n/dev/sda1 100G 85G 15G 85% /\n/dev/sda2 200G 50G 150G 25% /home'

# Execute the script and capture its output
output=$(bash ../src/disk_alert.sh)

# Expected warning line
expected='⚠️ /dev/sda1 mounted on / is 85% full! Consider cleaning up.'

if [[ "$output" == *"$expected"* ]]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: Unexpected output"
  echo "$output"
  exit 1
fi
