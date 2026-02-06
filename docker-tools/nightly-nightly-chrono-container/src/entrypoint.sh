#!/bin/bash
set -euo pipefail

SNAPSHOTS_DIR="/snapshots"
WORKSPACE_DIR="/workspace"

# Ensure snapshots directory exists
mkdir -p "$SNAPSHOTS_DIR"

case "$1" in
    snapshot)
        if [ -z "$2" ]; then
            echo "Usage: $0 snapshot <name>"
            exit 1
        fi
        SNAPSHOT_NAME="$2"
        echo "Creating snapshot '$SNAPSHOT_NAME' in $SNAPSHOTS_DIR..."
        # Create a temporary directory for snapshotting to avoid issues with active files
        # Mock rationale: This uses standard tar commands which are deterministic.
        # The actual files being snapshotted are controlled by the test environment.
        tar -czf "${SNAPSHOTS_DIR}/${SNAPSHOT_NAME}.tar.gz" -C "${WORKSPACE_DIR}" --exclude='./.snapshots' .
        echo "Snapshot '$SNAPSHOT_NAME' created at ${SNAPSHOTS_DIR}/${SNAPSHOT_NAME}.tar.gz"
        ;;
    restore)
        if [ -z "$2" ]; then
            echo "Usage: $0 restore <name>"
            exit 1
        fi
        SNAPSHOT_NAME="$2"
        SNAPSHOT_PATH="${SNAPSHOTS_DIR}/${SNAPSHOT_NAME}.tar.gz"
        if [ ! -f "$SNAPSHOT_PATH" ]; then
            echo "Error: Snapshot '$SNAPSHOT_NAME' not found at $SNAPSHOT_PATH"
            exit 1
        fi
        echo "Restoring snapshot '$SNAPSHOT_NAME' from $SNAPSHOT_PATH..."
        # Clear current workspace, but preserve the snapshots directory if it were nested (unlikely with separate mounts)
        find "${WORKSPACE_DIR}" -mindepth 1 -maxdepth 1 ! -name "$(basename "$SNAPSHOTS_DIR")" -exec rm -rf {} + || true
        # Mock rationale: This uses standard tar commands which are deterministic.
        # The actual files being restored are controlled by the test environment.
        tar -xzf "$SNAPSHOT_PATH" -C "${WORKSPACE_DIR}"
        echo "Snapshot '$SNAPSHOT_NAME' restored to ${WORKSPACE_DIR}"
        ;;
    list-snapshots)
        echo "Available snapshots:"
        # Mock rationale: This uses standard ls commands which are deterministic.
        # The files listed are controlled by the test environment.
        ls -1 "${SNAPSHOTS_DIR}"/*.tar.gz 2>/dev/null | xargs -n 1 basename | sed 's/\.tar\.gz$//' || echo "No snapshots found."
        ;;
    cleanup)
        echo "Cleaning up all snapshots in $SNAPSHOTS_DIR..."
        # Mock rationale: This uses standard rm commands which are deterministic.
        # The files removed are controlled by the test environment.
        rm -f "${SNAPSHOTS_DIR}"/*.tar.gz
        echo "All snapshots removed."
        ;;
    *)
        # If no specific command, run the provided command or default to bash
        exec "$@"
        ;;
esac
