# Nightly Server Zen Cleaner

This Ansible playbook, `nightly-server-zen-cleaner`, is designed to bring digital serenity to your servers by performing a mindful cleanup. It targets common areas where digital 'dust bunnies' accumulate, such as temporary directories, old package caches, and system logs.

## Features

*   **APT Package Cleanup:** Updates package cache, removes unused packages (`autoremove`), and cleans the local repository of retrieved package files (`clean`).
*   **Journal Log Vacuum:** Trims systemd journal logs to a specified size or age.
*   **Temporary File Removal:** Deletes old files from `/tmp` and `/var/tmp` directories based on a configurable age.

## Usage

1.  **Inventory:** Ensure you have an Ansible inventory file (`inventory.ini`) listing the servers you wish to clean. An example `inventory.ini` is provided in `src/`.

    ```ini
    [servers]
    your_server_ip_or_hostname ansible_user=your_ssh_user
    another_server ansible_user=another_ssh_user
    ```

    For local testing, you can use:

    ```ini
    [servers]
    localhost ansible_connection=local
    ```

2.  **Configuration:** Review and adjust the variables in `vars/main.yml` to suit your needs:

    ```yaml
    # vars/main.yml
    journal_vacuum_time: "7d" # Keep journal logs for 7 days
    tmp_age_days: 3          # Remove files in /tmp older than 3 days
    vartmp_age_days: 7       # Remove files in /var/tmp older than 7 days
    ```

3.  **Run the Playbook:** Execute the playbook using `ansible-playbook`.

    ```bash
    ansible-playbook -i src/inventory.ini src/zen_cleaner.yml --ask-become-pass
    ```

    *   `--ask-become-pass`: Prompts for the `sudo` password on the remote host(s), as cleanup tasks often require root privileges.
    *   `-C` or `--check`: Run in check mode (dry run) to see what changes would be made without actually executing them.

    ```bash
    ansible-playbook -i src/inventory.ini src/zen_cleaner.yml --check --ask-become-pass
    ```

## Testing

To run the automated tests for this playbook, use the following command:

```bash
ansible-playbook -i src/inventory.ini tests/test_zen_cleaner.yml
```

This test playbook will:

1.  Create a temporary directory and mock 'old' and 'new' files within it.
2.  Run the file cleanup logic from `zen_cleaner.yml` against this mock directory.
3.  Assert that the 'old' file is deleted and the 'new' file remains.
4.  Verify that `apt` and `journalctl` tasks are correctly configured and would be invoked (using `check_mode` where applicable).
5.  Clean up the temporary test directory.
