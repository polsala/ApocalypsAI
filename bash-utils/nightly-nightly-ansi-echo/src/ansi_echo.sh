#!/usr/bin/env bash
set -euo pipefail

# Determine message
if [ $# -gt 0 ]; then
  MSG="$*"
else
  read -r MSG
fi

# Compute hash
HASH=$(printf "%s" "$MSG" | md5sum | awk '{print $1}')
# Take first hex digit
FIRST_DIGIT=${HASH:0:1}
# Convert hex to decimal
DEC=$((16#$FIRST_DIGIT))
# Map to color index 0-5
COLOR_INDEX=$((DEC % 6))
# Define colors
COLORS=(31 32 33 34 35 36)
COLOR=${COLORS[$COLOR_INDEX]}

# Print colored message
printf "\\x1b[%sm%s\\x1b[0m\\n" "$COLOR" "$MSG"

# Log with timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "$TIMESTAMP - $MSG" >> ansi_echo.log

exit 0
