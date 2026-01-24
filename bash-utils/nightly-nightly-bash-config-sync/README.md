# nightly-bash-config-sync

This utility provides a simple bash script to synchronize configuration files from a local source directory to multiple remote hosts using `rsync`. It's designed for quick and dirty configuration management in a post-apocalyptic scenario where robust infrastructure might be scarce.

## Features

*   Synchronizes specified configuration files.
*   Supports multiple remote hosts.
*   Uses `rsync` for efficient file transfer.
*   Basic error handling and reporting.

## Usage

1.  **Prerequisites**: Ensure `rsync` is installed on both the source and target machines.
2.  **Configuration**: Edit the `src/sync_configs.sh` script to define:
    *   `SOURCE_DIR`: The local directory containing the configuration files to sync.
    *   `REMOTE_USER`: The username to use for SSH connections to remote hosts.
    *   `REMOTE_HOSTS`: An array of hostnames or IP addresses of the remote machines.
    *   `DEST_DIR`: The destination directory on the remote hosts where files will be synced.
3.  **Execution**: Run the script from your terminal:
    ```bash
    ./src/sync_configs.sh
    ```

## Example `src/sync_configs.sh` Setup

```bash
#!/bin/bash

# --- Configuration ---

# Local directory containing the configuration files to sync.
SOURCE_DIR="~/my_apocalypse_configs/"

# SSH username for remote hosts.
REMOTE_USER="survivor"

# Array of remote hostnames or IP addresses.
REMOTE_HOSTS=("server1.wasteland" "server2.wasteland" "192.168.1.100")

# Destination directory on remote hosts.
DEST_DIR="/etc/survivor_configs/"

# --- Script Logic ---

echo "Starting configuration synchronization..."

for host in "${REMOTE_HOSTS[@]}"; do
    echo "Syncing to ${REMOTE_USER}@${host}:${DEST_DIR}"
    rsync -avz --delete "${SOURCE_DIR}" "${REMOTE_USER}@${host}:${DEST_DIR}"
    if [ $? -eq 0 ]; then
        echo "Successfully synced to ${host}"
    else
        echo "ERROR: Failed to sync to ${host}"
    fi
done

echo "Configuration synchronization complete."
```

## Testing

This utility includes a basic test suite that mocks `rsync` and checks the script's logic for iterating through hosts and constructing `rsync` commands.

To run tests:

```bash
./tests/test_sync_configs.sh
```
