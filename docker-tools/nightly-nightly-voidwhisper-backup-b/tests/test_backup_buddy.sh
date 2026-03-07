#!/bin/sh

set -e

TEST_DIR="test_data"
BACKUP_OUTPUT="test_backups"

mkdir -p "$TEST_DIR" "$BACKUP_OUTPUT"
echo "sample data" > "$TEST_DIR/sample.txt"

docker build -t voidwhisper-backup-buddy ./src

# Test unencrypted backup
docker run --rm \
  -v "$(pwd)/$TEST_DIR":/data \
  -v "$(pwd)/$BACKUP_OUTPUT":/backups \
  voidwhisper-backup-buddy /data

# Check result
ls "$BACKUP_OUTPUT"/*.tar.gz || { echo "Unencrypted backup failed"; exit 1; }
echo "✓ Unencrypted backup passed"

# Clean up
rm -rf "$BACKUP_OUTPUT"/*

# Test encrypted backup
export PASSPHRASE="testpass"
docker run --rm \
  -v "$(pwd)/$TEST_DIR":/data \
  -v "$(pwd)/$BACKUP_OUTPUT":/backups \
  -e PASSPHRASE="$PASSPHRASE" \
  voidwhisper-backup-buddy /data

# Check result
ls "$BACKUP_OUTPUT"/*.enc || { echo "Encrypted backup failed"; exit 1; }
echo "✓ Encrypted backup passed"

# Cleanup
rm -rf "$TEST_DIR" "$BACKUP_OUTPUT"

echo "All tests passed."
