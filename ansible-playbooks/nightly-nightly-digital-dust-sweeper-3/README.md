# Nightly Digital Dust Sweeper

## Summary

This Ansible playbook acts as your diligent digital janitor, sweeping away the accumulated "dust bunnies" of temporary files, old logs, and orphaned packages from your remote servers. It ensures your systems remain lean, efficient, and ready for whatever the apocalypse throws their way.

## Features

*   **Temporary File Cleanup**: Deletes files older than a configurable number of days from `/tmp`.
*   **Configurable Path Cleanup**: Cleans up old files in user-defined directories (e.g., application-specific log folders).
*   **Package Cache Management**: Cleans `apt` (Debian/Ubuntu) or `yum` (RHEL/CentOS) caches and removes orphaned packages.
*   **Idempotent**: Can be run multiple times without causing unintended side effects.
*   **Whimsical**: Keeps your digital environment sparkling clean, just like a good dust bunny sweeper should!

## Prerequisites

*   **Ansible**: Version 2.10 or newer is recommended.
*   **Target Servers**: Linux-based servers accessible via SSH where you have `sudo` privileges.

## Usage

1.  **Clone the repository** (or copy this utility's folder):

    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/ansible-playbooks/nightly-digital-dust-sweeper
    ```

2.  **Configure your inventory**: Edit `src/inventory.ini` to list your target servers.

    ```ini
    # src/inventory.ini
    [servers]
    # Add your remote servers here:
    # server1.example.com
    # server2.example.com
    # You can also run it on localhost for testing:
    localhost ansible_connection=local
    ```

3.  **Customize variables**: Adjust cleanup thresholds in `vars/main.yml`.

    ```yaml
    # vars/main.yml
    cleanup_tmp_days: 7  # Files in /tmp older than 7 days will be deleted
    cleanup_log_days: 30 # Files in configured cleanup_paths older than 30 days will be deleted
    cleanup_paths:
      - /var/log/my_app_logs # Add any other paths you want to clean here
      - /opt/old_data
    ```

4.  **Run the playbook**: Execute the playbook from the utility's root directory.

    ```bash
    ansible-playbook -i src/inventory.ini src/dust_sweeper.yml --ask-become-pass
    ```

    *   `--ask-become-pass`: Prompts for the `sudo` password on target hosts.
    *   You can also use SSH keys for passwordless `sudo` if configured.

5.  **Run in Check Mode (Dry Run)**: To see what changes would be made without actually applying them:

    ```bash
    ansible-playbook -i src/inventory.ini src/dust_sweeper.yml --check --diff --ask-become-pass
    ```

## Testing

To run the automated tests for this utility:

1.  Ensure Ansible is installed.
2.  Navigate to the utility's root directory.
3.  Execute the test playbook:

    ```bash
    ansible-playbook -i tests/inventory_test.ini tests/test_dust_sweeper.yml --ask-become-pass
    ```

    This will create temporary files, run the cleanup playbook in check mode and for real, and then assert that the cleanup was successful and only targeted old files. It requires `sudo` access on `localhost` to create/delete files in `/tmp` for testing purposes.
