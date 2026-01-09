#!/usr/bin/env bash
set -euo pipefail

# Function to rotate an alphabet string by SHIFT positions
rotate_alphabet() {
  local alphabet="$1"
  local shift=$2
  local len=${#alphabet}
  local rotated=""
  for ((i=0; i<len; i++)); do
    # Compute new index with wrap‑around
    local new_index=$(( (i + shift + len) % len ))
    rotated+=${alphabet:new_index:1}
  done
  echo "$rotated"
}

# Parse optional shift argument (default 13)
if [[ $# -ge 1 && "$1" =~ ^-?[0-9]+$ ]]; then
  shift_amount=$1
  shift $((1))
else
  shift_amount=13
fi
# Normalize shift to range 0‑25
shift_amount=$(( shift_amount % 26 ))

# Determine input text: either remaining argument or stdin
if [[ $# -ge 1 ]]; then
  input_text="$*"
else
  input_text=$(cat)
fi

# Build source alphabets
upper_src="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lower_src="abcdefghijklmnopqrstuvwxyz"

# Build rotated target alphabets
upper_dst=$(rotate_alphabet "$upper_src" $shift_amount)
lower_dst=$(rotate_alphabet "$lower_src" $shift_amount)

# Perform translation using tr
# Mock rationale: tr will leave non‑alphabetic characters unchanged
echo "$input_text" | tr "$upper_src$lower_src" "$upper_dst$lower_dst"
