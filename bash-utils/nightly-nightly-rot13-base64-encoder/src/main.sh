#!/usr/bin/env bash
set -euo pipefail

# Function to display usage and exit with error
usage() {
  echo "Usage: $0 [string]" >&2
  exit 1
}

# Determine input source: argument or stdin
if [[ $# -gt 0 ]]; then
  input="$*"
else
  if [[ -t 0 ]]; then
    usage
  fi
  input="$(cat)"
fi

# Apply ROT13 transformation
rot13=$(echo "$input" | tr 'A-Za-z' 'N-ZA-Mn-za-m')

# Base64‑encode the ROT13 result (no trailing newline)
echo -n "$rot13" | base64
