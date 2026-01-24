#!/bin/bash

# --- Configuration ---

# Local directory containing the configuration files to sync.
# IMPORTANT: Ensure this directory exists and contains your config files.
# Example: SOURCE_DIR="~/my_apocalypse_configs/"
SOURCE_DIR="/tmp/source_configs/"

# SSH username for remote hosts.
# Example: REMOTE_USER="survivor"
REMOTE_USER="test_user"

# Array of remote hostnames or IP addresses.
# Example: REMOTE_HOSTS=("server1.wasteland" "server2.wasteland" "192.168.1.100")
REMOTE_HOSTS=("host1" "host2" "host3")

# Destination directory on remote hosts.
# Example: DEST_DIR="/etc/survivor_configs/"
DEST_DIR="/tmp/dest_configs/"

# --- Script Logic ---

# Check if source directory exists
if [ ! -d "${SOURCE_DIR}" ]; then
    echo "Error: Source directory '${SOURCE_DIR}' not found. Please create it and add your configuration files."
    exit 1
fi

echo "Starting configuration synchronization..."

# Loop through each remote host
for host in "${REMOTE_HOSTS[@]}"; do
    echo "Attempting to sync to ${REMOTE_USER}@${host}:${DEST_DIR}"
    
    # Use rsync to synchronize. -a (archive), -v (verbose), -z (compress), --delete (remove extraneous files from dest dirs)
    # We are mocking rsync for testing purposes, so this command won't actually run during tests.
    rsync -avz --delete "${SOURCE_DIR}" "${REMOTE_USER}@${host}:${DEST_DIR}"
    
    # Check the exit status of rsync
    if [ $? -eq 0 ]; then
        echo "Successfully synced to ${host}"
    else
        echo "ERROR: Failed to sync to ${host}. Check SSH connection and permissions."
    fi
done

echo "Configuration synchronization complete."

exit 0
