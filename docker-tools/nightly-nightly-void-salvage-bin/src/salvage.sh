#!/bin/bash

INPUT_FILE=$1

if [ -z "$INPUT_FILE" ]; then
  echo "Usage: salvage.sh <file>"
  exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
  echo "Error: File not found."
  exit 1
fi

# Obfuscate file contents
tr 'A-Za-z' 'N-ZA-Mn-za-m' < "$INPUT_FILE" > "$INPUT_FILE.obfuscated"

# Create archive
ARCHIVE_NAME="$(basename "$INPUT_FILE").salvaged.tar.gz"
tar -czf "$ARCHIVE_NAME" "$INPUT_FILE.obfuscated"

# Output checksum
sha256sum "$ARCHIVE_NAME" > "$ARCHIVE_NAME.sha256"

# Cleanup
rm "$INPUT_FILE.obfuscated"

echo "Salvaged: $ARCHIVE_NAME"
