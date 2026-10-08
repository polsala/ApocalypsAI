# Nightly Digital Dust Bunny Sweeper

## Summary

This Ansible playbook helps you keep your remote servers tidy by identifying and optionally cleaning up "digital dust bunnies" – old, forgotten files and directories that accumulate over time. It's designed to be run periodically to maintain server hygiene and free up disk space.

## Features

*   **Configurable Scan Paths**: Specify which directories to scan for old files.
*   **Age Threshold**: Define how old a file or directory must be to be considered a "dust bunny".
*   **Dry Run Mode**: Safely preview what would be cleaned up without making any changes.
*   **Detailed Reporting**: Generates a report of identified and (optionally) cleaned items.

## Usage

1.  **Prerequisites**:
    *   Ansible installed on your control machine.
    *   SSH access to your target servers with appropriate permissions (e.g., `sudo` for cleaning system directories).

2.  **Inventory**: Create or update your `src/inventory.ini` file with the target servers.

    ```ini
    [servers]
    server1.example.com
    server2.example.com
    ```

3.  **Configuration**: Edit `src/vars/main.yml` to define your `scan_paths`, `age_threshold_days`, and `dry_run` preference.

    ```yaml
    # src/vars/main.yml
    scan_paths:
      - /tmp
      - /var/log/old_app_logs
      - /opt/stale_backups
    age_threshold_days: 90 # Files older than 90 days are considered dust bunnies
    dry_run: true        # Set to 'false' to actually delete files
    report_path: "/tmp/dust_bunny_report_{{ ansible_hostname }}.txt" # Path on control machine
    ```

4.  **Run the Playbook**:

    To perform a dry run (recommended first):
    ```bash
    ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml -e "dry_run=true"
    ```

    To actually clean up (after reviewing dry run report):
    ```bash
    ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml -e "dry_run=false" --ask-become-pass
    ```
    (Use `--ask-become-pass` if `sudo` is required and not configured for passwordless access.)

## Configuration Details

*   `scan_paths`: A list of absolute paths to directories where the playbook will search for old files and directories. Be cautious when adding paths, especially system-critical ones.
*   `age_threshold_days`: An integer representing the number of days. Any file or directory last accessed or modified `age_threshold_days` ago or earlier will be considered for cleanup.
*   `dry_run`: A boolean (`true` or `false`). If `true`, the playbook will only report findings and generate a report, without deleting anything. If `false`, it will proceed with deletion.
*   `report_path`: The path on the *control machine* where the generated report will be saved. The `{{ ansible_hostname }}` variable ensures a unique report per host.

## Output

The playbook will output a summary of its actions and generate a detailed report file (e.g., `/tmp/dust_bunny_report_server1.example.com.txt`) on the control machine, listing all identified and (if `dry_run` is `false`) cleaned items.

## Testing

To run the tests, use the provided `tests/test_dust_bunny_sweeper.yml` playbook with a local inventory:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_dust_bunny_sweeper.yml
```
