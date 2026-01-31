# Nightly Digital Dust Bunny Sweeper

This Ansible playbook helps you maintain a pristine digital environment by identifying and archiving old, forgotten files (affectionately known as 'digital dust bunnies') from your servers. It sweeps them into a designated 'digital attic' directory, preventing clutter and reclaiming valuable disk space.

## Features

*   **Scan Multiple Directories**: Configure multiple source paths to scan for old files.
*   **Age-Based Archiving**: Define how old a file must be to be considered a 'dust bunny'.
*   **Designated Archive**: Moves identified files to a specified archive directory.
*   **Optional Compression**: Can compress the archived files into a tar.gz for further space saving.
*   **Sweep Report**: Generates a detailed report of all swept files.

## Prerequisites

*   Ansible (version 2.9 or newer recommended)
*   SSH access to your target servers (if not running locally)

## Usage

1.  **Configure Inventory**: Update `inventory.ini` with your target hosts.
    ```ini
    [webservers]
    web1.example.com
    web2.example.com

    [databases]
    db1.example.com

    [local]
    localhost ansible_connection=local
    ```

2.  **Define Variables**: Edit `vars/main.yml` to customize the sweep parameters:
    *   `source_dirs`: A list of directories to scan on the target hosts.
    *   `archive_dir`: The path on the target hosts where files will be moved.
    *   `age_days`: The minimum age (in days) for a file to be considered a dust bunny.
    *   `compress_archive`: Set to `true` to compress the archive after sweeping, `false` otherwise.

    ```yaml
    ---
    source_dirs:
      - "/var/log/old_app_logs"
      - "/tmp/stale_downloads"
    archive_dir: "/var/digital_attic"
    age_days: 30
    compress_archive: true
    ```

3.  **Run the Playbook**: Execute the playbook using `ansible-playbook`.

    ```bash
    ansible-playbook -i inventory.ini dust_bunny_sweeper.yml
    ```

    To perform a dry run without making any changes (highly recommended for initial testing):

    ```bash
    ansible-playbook -i inventory.ini dust_bunny_sweeper.yml --check --diff
    ```

4.  **Review Report**: After a successful sweep, a report named `sweep_report_YYYYMMDDTHHMMSS.txt` will be generated in your `archive_dir`.

## Example Output (Report)

```
Digital Dust Bunny Sweep Report - 20231027T103000

Archive Location: /var/digital_attic

Swept Files (2 total):
- /var/log/old_app_logs/app.log.2023-09-01 (Last modified: 2023-09-01 00:00:00)
- /tmp/stale_downloads/report.pdf (Last modified: 2023-09-15 14:30:00)

---
May your servers remain clutter-free and your bits ever nimble.
```

## Testing

To run the automated tests for this utility, navigate to the `tests/` directory and execute the test playbook:

```bash
ansible-playbook -i ../inventory.ini test_dust_bunny_sweeper.yml
```

These tests use `check_mode` and mock file system interactions to ensure the playbook logic and report generation work as expected without actual system modifications.
