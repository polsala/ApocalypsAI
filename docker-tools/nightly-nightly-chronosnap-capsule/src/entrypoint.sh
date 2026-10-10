#!/bin/bash
set -euo pipefail

TARGET_DIR="${TARGET_DIR:-/data}"
SNAPSHOT_ROOT_DIR="${SNAPSHOT_ROOT_DIR:-/snapshots}"

mkdir -p "$TARGET_DIR" "$SNAPSHOT_ROOT_DIR"

# Helper function to get a timestamp
get_timestamp() {
    date +"%Y%m%d%H%M%S"
}

# Snapshot function
snapshot() {
    local timestamp=$(get_timestamp)
    local snapshot_path="$SNAPSHOT_ROOT_DIR/$timestamp.tar.gz"
    echo "Creating snapshot $timestamp of $TARGET_DIR..."
    
    # Ensure the target directory exists before tarring
    if [ ! -d "$TARGET_DIR" ]; then
        echo "Error: Target directory $TARGET_DIR does not exist." >&2
        exit 1
    fi
    
    # Use -C to change directory before adding to archive, so the archive contains just the contents of TARGET_DIR
    # This ensures that when extracted, it doesn't create an extra parent directory.
    tar -czf "$snapshot_path" -C "$(dirname "$TARGET_DIR")" "$(basename "$TARGET_DIR")"
    echo "Snapshot created: $snapshot_path"
}

# Restore function
restore() {
    local timestamp="$1"
    if [ -z "$timestamp" ]; then
        echo "Usage: restore <timestamp>" >&2
        echo "Available snapshots:" >&2
        list_snapshots >&2
        exit 1
    fi

    local snapshot_file="$SNAPSHOT_ROOT_DIR/$timestamp.tar.gz"
    if [ ! -f "$snapshot_file" ]; then
        echo "Error: Snapshot '$timestamp' not found at '$snapshot_file'." >&2
        list_snapshots >&2
        exit 1
    fi

    echo "Restoring $TARGET_DIR from snapshot $timestamp..."
    
    # Clear current target directory contents, ignoring errors if directory is empty or non-existent
    # Use find to delete contents, but keep the directory itself
    find "$TARGET_DIR" -mindepth 1 -delete || true
    mkdir -p "$TARGET_DIR" # Ensure target directory exists

    # Extract the snapshot. -C extracts to the specified directory.
    # The tarball contains the basename of TARGET_DIR, so extracting to its parent will place it correctly.
    tar -xzf "$snapshot_file" -C "$(dirname "$TARGET_DIR")"
    echo "Restoration complete."
}

# List snapshots function
list_snapshots() {
    echo "--- Available Chronosnap Capsules ---"
    find "$SNAPSHOT_ROOT_DIR" -name "*.tar.gz" -printf "%f\n" | sed 's/\.tar\.gz$//' | sort -r
    echo "-------------------------------------"
}

# Main command parsing
case "$1" in
    snapshot)
        snapshot
        ;;
    restore)
        shift
        restore "$@"
        ;;
    list)
        list_snapshots
        ;;
    *)
        echo "Usage: $0 {snapshot|restore <timestamp>|list}" >&2
        exit 1
        ;;
esac
