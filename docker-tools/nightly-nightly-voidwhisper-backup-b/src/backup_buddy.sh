#!/bin/sh

set -e

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <directory_to_backup>"
  exit 1
fi

SOURCE_DIR="$1"
BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
ARCHIVE_NAME="backup_$TIMESTAMP.tar.gz"
ENCRYPTED_NAME="${ARCHIVE_NAME}.enc"

if [ ! -d "$SOURCE_DIR" ]; then
  echo "Error: Directory '$SOURCE_DIR' does not exist."
  exit 1
fi

# Create archive
tar -czf "$BACKUP_DIR/$ARCHIVE_NAME" -C "$(dirname "$SOURCE_DIR")" "$(basename "$SOURCE_DIR")"

# Encrypt if PASSPHRASE is set
if [ -n "$PASSPHRASE" ]; then
  openssl enc -aes-256-cbc -salt -in "$BACKUP_DIR/$ARCHIVE_NAME" -out "$BACKUP_DIR/$ENCRYPTED_NAME" -k "$PASSPHRASE"
  rm "$BACKUP_DIR/$ARCHIVE_NAME"
  echo "Encrypted backup created: $ENCRYPTED_NAME"
else
  echo "Backup created: $ARCHIVE_NAME"
fi
