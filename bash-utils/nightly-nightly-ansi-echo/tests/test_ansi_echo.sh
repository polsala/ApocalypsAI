#!/usr/bin/env bash
set -euo pipefail

# Ensure script is executable
chmod +x src/ansi_echo.sh

# Test with known input
INPUT="Hello World"
OUTPUT=$(./src/ansi_echo.sh "$INPUT")
# Check that output contains ANSI escape code
if [[ ! "$OUTPUT" =~ $'\\x1b\\[' ]]; then
  echo "FAIL: Output does not contain ANSI escape code"
  exit 1
fi

# Extract color code
COLOR_CODE=$(echo "$OUTPUT" | grep -oP '\\x1b\\[\\K[0-9]+(?=m)')
# Ensure color code is one of 31-36
case "$COLOR_CODE" in
  31|32|33|34|35|36) ;;
  *) echo "FAIL: Invalid color code $COLOR_CODE"; exit 1 ;;
esac

# Check that log file contains the message
LOG_CONTENT=$(tail -n 1 ansi_echo.log)
if [[ "$LOG_CONTENT" != *"$INPUT"* ]]; then
  echo "FAIL: Log file does not contain message"
  exit 1
fi

echo "PASS"
