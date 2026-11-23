#!/usr/bin/env bash

# Nightly Radiation Report
# Generates a whimsical radiation level report for a given file.
# The radiation level is deterministic, based on the file's SHA‑256 hash.

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <file>"
  exit 1
fi

FILE="$1"

if [[ ! -f "$FILE" ]]; then
  echo "File not found: $FILE"
  exit 1
fi

# File size in bytes (portable fallback if stat -c%s is unavailable)
if command -v stat >/dev/null 2>&1; then
  SIZE=$(stat -c%s "$FILE" 2>/dev/null || wc -c <"$FILE")
else
  SIZE=$(wc -c <"$FILE")
fi

# Line count
LINES=$(wc -l <"$FILE")

# SHA‑256 hash of the file
HASH=$(sha256sum "$FILE" | awk '{print $1}')
# Use the first 8 hex characters to form a number
HEX=${HASH:0:8}
DEC=$((16#$HEX))
# Radiation level between 0 and 100 inclusive
RADIATION=$((DEC % 101))

echo "Radiation Report for $FILE"
echo "Size: $SIZE bytes"
echo "Lines: $LINES"
echo "Radiation Level: $RADIATION µSv/h"
