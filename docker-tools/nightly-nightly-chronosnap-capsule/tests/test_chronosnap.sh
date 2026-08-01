#!/bin/bash
set -euo pipefail

CONTAINER_NAME="test_chronosnap_capsule"
IMAGE_NAME="chronosnap-capsule"
HOST_DATA_DIR="./temp_data"
HOST_SNAPSHOT_DIR="./temp_snapshots"

# Mock rationale: These tests are deterministic and offline as they operate entirely within a local Docker environment.
# They simulate file system changes and container interactions without external dependencies, ensuring consistent results.

# --- Cleanup function to ensure a clean state even if tests fail ---
cleanup() {
  echo "--- Running cleanup ---"
  docker stop "$CONTAINER_NAME" > /dev/null 2>&1 || true
  docker rm "$CONTAINER_NAME" > /dev/null 2>&1 || true
  rm -rf "$HOST_DATA_DIR"
  rm -rf "$HOST_SNAPSHOT_DIR"
}

trap cleanup EXIT

echo "--- Building Docker image ---"
docker build -t "$IMAGE_NAME" .

echo "--- Setting up test environment ---"
mkdir -p "$HOST_DATA_DIR"
mkdir -p "$HOST_SNAPSHOT_DIR"

# Start the container in detached mode, keeping it alive
docker run -d --name "$CONTAINER_NAME" \
  -v "$(pwd)/$HOST_DATA_DIR":/data \
  -v "$(pwd)/$HOST_SNAPSHOT_DIR":/snapshots \
  "$IMAGE_NAME" tail -f /dev/null

# Give the container a moment to start
sleep 2

# --- Test Case 1: Initial Snapshot and Restore ---

echo "--- Test Case 1: Initial Snapshot ---"

# Create initial files in the target directory
docker exec "$CONTAINER_NAME" bash -c "echo 'Initial content for file1' > /data/file1.txt"
docker exec "$CONTAINER_NAME" bash -c "mkdir -p /data/subdir && echo 'Subdir content' > /data/subdir/file_in_subdir.txt"

# Take a snapshot
SNAPSHOT_OUTPUT=$(docker exec "$CONTAINER_NAME" /usr/local/bin/entrypoint.sh snapshot)
FIRST_SNAPSHOT_TIMESTAMP=$(echo "$SNAPSHOT_OUTPUT" | grep 'Snapshot created' | sed -E 's/.*\/([0-9]+)\.tar\.gz/\1/')

if [ -z "$FIRST_SNAPSHOT_TIMESTAMP" ]; then
  echo "Error: Could not get first snapshot timestamp." >&2
  exit 1
fi

echo "First snapshot timestamp: $FIRST_SNAPSHOT_TIMESTAMP"

# Verify snapshot file exists on host
if [ ! -f "$HOST_SNAPSHOT_DIR/$FIRST_SNAPSHOT_TIMESTAMP.tar.gz" ]; then
  echo "Error: Snapshot file $HOST_SNAPSHOT_DIR/$FIRST_SNAPSHOT_TIMESTAMP.tar.gz not found on host." >&2
  exit 1
fi

echo "--- Test Case 1: Modify and Restore ---"

# Modify existing file and add a new one
docker exec "$CONTAINER_NAME" bash -c "echo 'Modified content for file1' > /data/file1.txt"
docker exec "$CONTAINER_NAME" bash -c "echo 'New file content' > /data/file2.txt"
docker exec "$CONTAINER_NAME" bash -c "rm -f /data/subdir/file_in_subdir.txt"

# Verify changes before restore
if [ "$(cat "$HOST_DATA_DIR/file1.txt")" != "Modified content for file1" ]; then
  echo "Error: file1.txt not modified as expected before restore." >&2
  exit 1
fi
if [ ! -f "$HOST_DATA_DIR/file2.txt" ]; then
  echo "Error: file2.txt not created as expected before restore." >&2
  exit 1
fi
if [ -f "$HOST_DATA_DIR/subdir/file_in_subdir.txt" ]; then
  echo "Error: file_in_subdir.txt not removed as expected before restore." >&2
  exit 1
fi

# Restore to the first snapshot
docker exec "$CONTAINER_NAME" /usr/local/bin/entrypoint.sh restore "$FIRST_SNAPSHOT_TIMESTAMP"

# Verify restoration
if [ "$(cat "$HOST_DATA_DIR/file1.txt")" != "Initial content for file1" ]; then
  echo "Error: file1.txt not restored correctly." >&2
  exit 1
fi
if [ -f "$HOST_DATA_DIR/file2.txt" ]; then
  echo "Error: file2.txt should not exist after restore." >&2
  exit 1
fi
if [ ! -f "$HOST_DATA_DIR/subdir/file_in_subdir.txt" ]; then
  echo "Error: file_in_subdir.txt not restored (missing)." >&2
  exit 1
fi
if [ "$(cat "$HOST_DATA_DIR/subdir/file_in_subdir.txt")" != "Subdir content" ]; then
  echo "Error: file_in_subdir.txt content not restored correctly." >&2
  exit 1
fi

echo "--- Test Case 2: Listing Snapshots ---"

# Take a second snapshot
SNAPSHOT_OUTPUT=$(docker exec "$CONTAINER_NAME" /usr/local/bin/entrypoint.sh snapshot)
SECOND_SNAPSHOT_TIMESTAMP=$(echo "$SNAPSHOT_OUTPUT" | grep 'Snapshot created' | sed -E 's/.*\/([0-9]+)\.tar\.gz/\1/')

if [ -z "$SECOND_SNAPSHOT_TIMESTAMP" ]; then
  echo "Error: Could not get second snapshot timestamp." >&2
  exit 1
fi

# List snapshots and verify both are present
LIST_OUTPUT=$(docker exec "$CONTAINER_NAME" /usr/local/bin/entrypoint.sh list)
if ! echo "$LIST_OUTPUT" | grep -q "$FIRST_SNAPSHOT_TIMESTAMP"; then
  echo "Error: First snapshot timestamp not found in list output." >&2
  exit 1
fi
if ! echo "$LIST_OUTPUT" | grep -q "$SECOND_SNAPSHOT_TIMESTAMP"; then
  echo "Error: Second snapshot timestamp not found in list output." >&2
  exit 1
fi

echo "All tests passed successfully!"

# Cleanup is handled by the trap EXIT
