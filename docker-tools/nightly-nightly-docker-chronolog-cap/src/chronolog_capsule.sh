#!/bin/bash

set -euo pipefail

# --- Configuration ---
DEFAULT_CONFIG_PATHS=("/etc" "/var/log" "/app/config") # Common paths to capture

# --- Functions ---
log_info() { echo "[INFO] $(date +'%Y-%m-%d %H:%M:%S') - $@"; }
log_error() { echo "[ERROR] $(date +'%Y-%m-%d %H:%M:%S') - $@" >&2; exit 1; }

# --- Main Logic ---

# Check for minimum arguments
if [[ $# -lt 2 ]]; then
    log_error "Usage: $0 <container_name_or_id> <output_directory> [path_to_capture1] [path_to_capture2]..."
fi

CONTAINER_NAME="$1"
OUTPUT_DIR="$2"
shift 2

# Remaining arguments are custom paths to capture
CUSTOM_PATHS=()
for arg in "$@"; do
    CUSTOM_PATHS+=("$arg")
done

ALL_PATHS_TO_CAPTURE=("${DEFAULT_CONFIG_PATHS[@]}" "${CUSTOM_PATHS[@]}")

log_info "Starting Chronolog Capsule for container: '$CONTAINER_NAME'"
log_info "Output directory: '$OUTPUT_DIR'"
log_info "Paths to capture: ${ALL_PATHS_TO_CAPTURE[*]}"

# Create a timestamp for the archive
TIMESTAMP=$(date +'%Y%m%d_%H%M%S')
ARCHIVE_NAME="${CONTAINER_NAME}_chronolog_capsule_${TIMESTAMP}.tar.gz"

# Create a temporary directory for staging files
TEMP_CAPSULE_DIR="/tmp/chronolog_capsule_staging_${TIMESTAMP}"
mkdir -p "$TEMP_CAPSULE_DIR" || log_error "Failed to create temporary directory: $TEMP_CAPSULE_DIR"

log_info "Staging files in: $TEMP_CAPSULE_DIR"

# 1. Capture Docker logs
log_info "Capturing logs from '$CONTAINER_NAME'..."
if ! docker logs "$CONTAINER_NAME" > "$TEMP_CAPSULE_DIR/logs.txt"; then
    log_error "Failed to capture logs from container '$CONTAINER_NAME'. Is the container running and accessible?"
fi
log_info "Logs captured to $TEMP_CAPSULE_DIR/logs.txt"

# 2. Copy specified paths from the container
for path in "${ALL_PATHS_TO_CAPTURE[@]}"; do
    log_info "Attempting to copy '$path' from '$CONTAINER_NAME'..."
    # docker cp requires a colon for container:path, and copies to a local path
    # We want to preserve the directory structure relative to the container root
    # So, if copying /etc/foo, it should end up in $TEMP_CAPSULE_DIR/etc/foo
    
    # Create the target directory structure in TEMP_CAPSULE_DIR
    TARGET_PATH_IN_TEMP="${TEMP_CAPSULE_DIR}${path}"
    mkdir -p "$(dirname "$TARGET_PATH_IN_TEMP")" # Ensure parent dir exists for docker cp

    # docker cp copies the *contents* of the source path if it's a directory, or the file itself
    # If source is /etc, and dest is /tmp/capsule/etc, it copies contents of /etc into /tmp/capsule/etc
    # If source is /etc/file, and dest is /tmp/capsule/etc/file, it copies file into /tmp/capsule/etc/file
    
    # To handle both files and directories gracefully, we copy to the parent directory of the target path
    # and let docker cp create the final component.
    # Example: docker cp container:/etc /tmp/capsule/ -> creates /tmp/capsule/etc/...
    # Example: docker cp container:/etc/file.conf /tmp/capsule/etc/ -> creates /tmp/capsule/etc/file.conf
    
    # Determine the destination for docker cp to correctly preserve structure
    # If path is /etc, we want it to copy to $TEMP_CAPSULE_DIR/
    # If path is /etc/nginx.conf, we want it to copy to $TEMP_CAPSULE_DIR/etc/
    
    # Get the base name of the path (e.g., 'etc' from '/etc', 'nginx.conf' from '/etc/nginx.conf')
    PATH_BASENAME=$(basename "$path")
    
    # If the path is a root directory (e.g., /etc), docker cp needs the destination to be the parent of where /etc should go
    # If the path is a file (e.g., /etc/nginx.conf), docker cp needs the destination to be the directory where nginx.conf should go
    
    # A simpler approach: copy to a temporary sub-directory and then move its contents
    # This avoids issues with docker cp's behavior with trailing slashes and directory vs file copies.
    TEMP_COPY_DEST="${TEMP_CAPSULE_DIR}/_temp_copy_$(basename "$path")"
    mkdir -p "$TEMP_COPY_DEST"

    if docker cp "$CONTAINER_NAME:$path" "$TEMP_COPY_DEST/"; then
        # Move contents from TEMP_COPY_DEST to the correct location in TEMP_CAPSULE_DIR
        # This handles both files and directories copied by docker cp
        mv "$TEMP_COPY_DEST"/* "$TEMP_CAPSULE_DIR/" || true # `|| true` to ignore if dir is empty
        rmdir "$TEMP_COPY_DEST" || true # Clean up temp copy dir
        log_info "Successfully copied '$path'."
    else
        log_info "Warning: Failed to copy '$path' from container '$CONTAINER_NAME'. It might not exist or permissions are an issue. Skipping."
        rm -rf "$TEMP_COPY_DEST" || true # Clean up failed temp copy dir
    fi
done

# 3. Create the tarball
log_info "Creating archive '$ARCHIVE_NAME' from '$TEMP_CAPSULE_DIR'..."
# Use -C to change directory before archiving, so the archive contains 'logs.txt', 'etc/', etc., directly
if ! tar -czf "${OUTPUT_DIR}/${ARCHIVE_NAME}" -C "$TEMP_CAPSULE_DIR" .; then
    log_error "Failed to create tarball: ${OUTPUT_DIR}/${ARCHIVE_NAME}"
fi
log_info "Archive created: ${OUTPUT_DIR}/${ARCHIVE_NAME}"

# 4. Clean up temporary directory
log_info "Cleaning up temporary directory: $TEMP_CAPSULE_DIR"
rm -rf "$TEMP_CAPSULE_DIR"

log_info "Chronolog Capsule operation complete."
