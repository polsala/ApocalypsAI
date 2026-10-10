#!/usr/bin/env bash
# nightly-terminal-qr: generate QR code in terminal

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 \"text to encode\""
  exit 1
fi

TEXT="$1"

if ! command -v qrencode >/dev/null 2>&1; then
  echo "Error: 'qrencode' is not installed. Install it via your package manager."
  exit 1
fi

# Generate QR code in ANSI UTF-8 mode
qrencode -t ANSIUTF8 "$TEXT"
