# Nightly Server Serenity Ritual (nightly-server-serenity)

## Summary

This Ansible playbook performs a series of gentle, non-disruptive checks and minor cleanups on your servers to ensure their 'serenity' and optimal 'vibe' for the next day. Think of it as a digital spa day for your machines, promoting a calm and efficient operational environment.

## Features

*   **Forgotten Temporary Files**: Identifies and reports (or optionally cleans) old temporary files in common locations (`/tmp`, `/var/tmp`).
*   **Cosmic Clock Sync**: Verifies NTP synchronization to ensure servers are aligned with the universal time stream.
*   **Pending Reboot Reminder**: Gently reminds if a server needs a reboot for kernel or critical updates.
*   **Disk Space Harmony**: Reports directories with high disk usage that might be accumulating 'digital clutter'.
*   **Serenity Report**: Generates a summary report of all checks, complete with a whimsical message.

## Usage

1.  **Prepare your inventory**: Create an `inventory.ini` file listing the servers you wish to bless.

    ```ini
    [servers]
    server1.example.com
    server2.example.com
    ```

2.  **Configure variables (optional)**: You can override default variables by creating a `vars/main.yml` or passing them via the command line.

    *   `serenity_report_path`: Path where the serenity report will be saved (default: `/var/log/serenity_report.txt`).
    *   `tmp_file_age_days`: Age in days for temporary files to be considered 'old' (default: `7`).
    *   `clean_old_tmp_files`: Set to `true` to actually remove old temporary files (default: `false`).

3.  **Run the playbook**:

    ```bash
    ansible-playbook -i src/inventory.ini src/playbook.yml
    ```

    To run with specific variables:

    ```bash
    ansible-playbook -i src/inventory.ini src/playbook.yml -e "serenity_report_path=/tmp/my_serenity.txt clean_old_tmp_files=true"
    ```

## Example Serenity Report

```
--- Server Serenity Report for server1.example.com ---
Date: 2023-10-27 08:00:00 UTC

[ Cosmic Clock Sync ]
Status: Synchronized with NTP server.

[ Forgotten Temporary Files (older than 7 days) ]
Status: No old temporary files found.

[ Pending Reboot Reminder ]
Status: No reboot required.

[ Disk Space Harmony ]
/var/log: 1.2G
/opt: 500M

--- Serenity Level: High ---
May your server hum with the gentle rhythm of efficiency and peace.
```

## Testing

To run the included tests, which use Ansible's `set_fact` to mock remote host outputs for deterministic, offline validation:

```bash
ansible-playbook -i tests/test_inventory.ini tests/test_serenity_ritual.yml
```

This will verify the playbook's logic and report generation without needing actual remote servers or making any changes.
