#!/bin/bash

# Nightly Digital Dust Bunny Hunt
# Hunts down forgotten files (digital dust bunnies) older than a specified age.

DEFAULT_DIR="."
DEFAULT_AGE=90

TARGET_DIR="$DEFAULT_DIR"
AGE_THRESHOLD="$DEFAULT_AGE"

# Parse command-line arguments
while getopts "d:a:" opt; do
  case "$opt" in
    d)
      TARGET_DIR="$OPTARG"
      ;;
    a)
      AGE_THRESHOLD="$OPTARG"
      ;;
    \?)
      echo "Usage: $0 [-d <directory>] [-a <age_in_days>]" >&2
      exit 1
      ;;
  esac
done

# Validate directory exists
if [ ! -d "$TARGET_DIR" ]; then
  echo "Error: Directory '$TARGET_DIR' not found." >&2
  exit 1
fi

# Validate age threshold is a positive integer
if ! [[ "$AGE_THRESHOLD" =~ ^[0-9]+$ ]] || [ "$AGE_THRESHOLD" -le 0 ]; then
  echo "Error: Age threshold must be a positive integer." >&2
  exit 1
fi

echo "\n--- Initiating Digital Dust Bunny Hunt ---"
echo "Scanning directory: '$TARGET_DIR'"
echo "Looking for files older than: '$AGE_THRESHOLD' days (last modified)"
echo "----------------------------------------\n"

# Find files older than the specified age
# -type f: only regular files
# -mtime +N: files last modified N*24 hours ago. +N means more than N days.
DUST_BUNNIES=$(find "$TARGET_DIR" -type f -mtime +"$AGE_THRESHOLD" 2>/dev/null)

if [ -z "$DUST_BUNNIES" ]; then
  echo "✨ No digital dust bunnies found! Your temporal storage is sparkling clean. ✨"
else
  echo "Found the following digital dust bunnies (files older than $AGE_THRESHOLD days):\n"
  echo "$DUST_BUNNIES"
  echo "\n--- End of Hunt ---"
  echo "Consider reviewing these files for archiving or deletion to keep your digital space tidy."
fi

exit 0
