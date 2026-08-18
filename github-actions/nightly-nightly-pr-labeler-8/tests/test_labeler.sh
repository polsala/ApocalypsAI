#!/usr/bin/env bash
set -euo pipefail

# Mock file list (multiline string)
mock_files=$'src/main.py\ndocs/README.md\nCHANGELOG.md\nassets/logo.png'

# Run the labeler script
output=$(bash "$(dirname "$0")/../src/labeler.sh" "$mock_files")

# Expected output
expected="Labels to add: documentation,python,markdown,misc"

if [[ "$output" == "$expected" ]]; then
  echo "PASS"
  exit 0
else
  echo "FAIL"
  echo "Got: $output"
  exit 1
fi
