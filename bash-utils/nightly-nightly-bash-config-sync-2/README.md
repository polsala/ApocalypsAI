# nightly-bash-config-sync

A whimsical yet practical bash script designed to synchronize configuration files across multiple remote hosts using `rsync`. This utility is perfect for maintaining consistent settings on your fleet of servers or even across your personal machines.

## Philosophy

"Anarchy with discipline" — this script provides a simple, robust way to manage distributed configurations without complex dependencies. It leverages the power of `rsync` for efficient file transfers and basic bash scripting for control.

## Usage

1.  **Prerequisites**: Ensure `rsync` is installed on all target machines and that you have SSH access (preferably with key-based authentication) to them.

2.  **Configuration**: Edit the `src/config_sync.sh` script and modify the `REMOTE_HOSTS` array to include the SSH connection strings for your target machines (e.g., `user@hostname`). Also, define `SOURCE_DIR` for the local directory containing your configuration files and `DEST_DIR` for the remote destination.

3.  **Execution**: Run the script from your local machine:
    ```bash
    ./src/config_sync.sh
    ```

    The script will iterate through each host in `REMOTE_HOSTS` and perform an `rsync` operation to synchronize the `SOURCE_DIR` to the `DEST_DIR` on each remote host.

## Features

*   **Simple Configuration**: Easy to set up by modifying variables within the script.
*   **Efficient Synchronization**: Utilizes `rsync`'s delta-transfer algorithm to only transfer changed files.
*   **SSH Integration**: Leverages SSH for secure remote access and file transfer.
*   **Error Handling**: Basic checks for `rsync` command success.

## Testing

This utility includes a basic test suite that mocks the `rsync` command to verify the script's logic without requiring actual remote hosts.

To run the tests:

```bash
./tests/test_config_sync.sh
```
