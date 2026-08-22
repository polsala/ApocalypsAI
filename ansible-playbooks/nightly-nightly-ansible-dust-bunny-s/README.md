# Nightly Ansible Digital Dust Bunny Sweeper

This Ansible playbook helps you keep your managed systems tidy by identifying and optionally cleaning up "digital dust bunnies." These include old backup files, temporary files, and empty files that can accumulate over time, consuming disk space and cluttering directories.

## Features

*   **Identifies:** Locates files matching common backup/temp patterns (`.bak`, `~`, `.tmp`, `.old`, `core.*`) and empty files.
*   **Reports:** Provides a clear summary of all identified dust bunnies.
*   **Cleans Up (Optional):** Can be configured to remove the identified files.
*   **Dry Run Mode:** Always runs in dry-run mode by default, allowing you to review findings before any changes are made.

## Usage

1.  **Inventory:** Ensure you have an `inventory.ini` file listing your target hosts.

    ```ini
    [servers]
    server1.example.com
    server2.example.com
    ```

2.  **Configuration:** Review and customize `vars/main.yml` to define:
    *   `dust_bunny_target_paths`: Directories to scan.
    *   `dust_bunny_file_patterns`: Glob patterns for files to consider.
    *   `dust_bunny_age_threshold_days`: Minimum age (in days) for a file to be considered a "dust bunny" (only applies to pattern-matched files, not empty files).
    *   `dust_bunny_dry_run`: Set to `false` to enable actual deletion (defaults to `true`).

3.  **Run in Dry-Run Mode (Recommended First):**
    This will only report what *would* be cleaned up.

    ```bash
    ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml
    ```

4.  **Run for Cleanup:**
    First, set `dust_bunny_dry_run: false` in `vars/main.yml`.
    Then execute:

    ```bash
    ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml
    ```

    You can also override `dry_run` from the command line:
    ```bash
    ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml -e "dust_bunny_dry_run=false"
    ```

## Example `vars/main.yml`

```yaml
---
dust_bunny_target_paths:
  - /tmp
  - /var/log
  - /etc/nginx/conf.d
  - /home/{{ ansible_user }}/backups # Example for user-specific paths

dust_bunny_file_patterns:
  - "*.bak"
  - "*~"
  - "*.tmp"
  - "*.old"
  - "core.*" # Core dump files

dust_bunny_age_threshold_days: 30 # Files older than 30 days matching patterns

dust_bunny_dry_run: true # Set to false to enable deletion
```

## Testing

To run the tests, you'll need `ansible` installed. The tests create temporary mock files on `localhost`, run the playbook in various modes, and assert the outcomes.

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_dust_bunny_sweeper.yml
```
