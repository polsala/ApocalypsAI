# Nightly Digital Dust Bunny Sweeper

## Overview
The `nightly-digital-dust-bunny-sweeper` is an Ansible playbook designed to help you keep your remote servers tidy by identifying and optionally removing "digital dust bunnies" – old, temporary, or excessively large files that might be cluttering your file systems. Think of it as a diligent, automated cleaning crew for your digital infrastructure.

## Features
-   **Configurable Scan Paths**: Specify which directories to scan for dust bunnies.
-   **Age-based Cleanup**: Target files older than a defined number of days.
-   **Size-based Cleanup**: Identify files larger than a specified size.
-   **Dry Run Mode**: Preview what files *would* be removed without actually deleting them.
-   **Exclusion List**: Define patterns or paths to ignore during scans.
-   **Detailed Reporting**: Get a summary of found and (if enabled) removed files.

## Prerequisites
-   **Ansible**: Installed on your control machine.
-   **SSH Access**: To your target servers from the control machine.
-   **Python**: Installed on target servers (Ansible's default connection method requires it).

## Usage

1.  **Define your inventory**:
    Create an `inventory.ini` file (or use an existing one) listing your target servers.

    ```ini
    [webservers]
    web1.example.com
    web2.example.com

    [databases]
    db1.example.com
    ```

2.  **Configure cleanup parameters**:
    Edit `src/vars/config.yml` to define your desired scan paths, age thresholds, size limits, and whether to perform a dry run.

    ```yaml
    ---
    dust_bunny_sweeper_paths:
      - /tmp
      - /var/log
      - /opt/old_backups
    dust_bunny_sweeper_age_days: 90 # Files older than 90 days
    dust_bunny_sweeper_min_size_mb: 100 # Files larger than 100 MB
    dust_bunny_sweeper_dry_run: true # Set to 'false' to actually delete files
    dust_bunny_sweeper_exclude_patterns:
      - "*.log.gz" # Example: don't touch compressed logs
      - "/var/log/important_app.log" # Example: don't touch specific important logs
    ```

3.  **Run the playbook (Dry Run first!)**:
    It is **highly recommended** to run with `dust_bunny_sweeper_dry_run: true` first to review the findings before enabling actual deletion.

    ```bash
    ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml
    ```

    After reviewing the dry run output, if you're confident, change `dust_bunny_sweeper_dry_run` to `false` in `src/vars/config.yml` and run again to perform the cleanup.

## Example Output (Dry Run)

```
PLAY [Sweep Digital Dust Bunnies] **********************************************

TASK [Gathering Facts] *********************************************************
ok: [web1.example.com]
ok: [db1.example.com]

TASK [Find potential dust bunnies] *********************************************
ok: [web1.example.com]
ok: [db1.example.com]

TASK [Report findings (Dry Run)] ***********************************************
ok: [web1.example.com] => {
    "msg": "Dry Run: Found 3 potential dust bunnies on web1.example.com:\n- /tmp/old_temp_file.txt (120 days old, 50MB)\n- /opt/old_backups/archive_2022.zip (300 days old, 1.2GB)\n- /var/log/app_debug.log.1 (100 days old, 150MB)"
}
ok: [db1.example.com] => {
    "msg": "Dry Run: Found 1 potential dust bunny on db1.example.com:\n- /tmp/large_db_dump.sql (5 days old, 2.5GB)"
}

PLAY RECAP *********************************************************************
web1.example.com           : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
db1.example.com            : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

## Testing
The `tests/test_dust_bunny_sweeper.yml` playbook provides a local, deterministic test suite. It creates mock files, runs the sweeper in both dry-run and actual cleanup modes, and verifies the outcomes.

To run tests:
```bash
ansible-playbook tests/test_dust_bunny_sweeper.yml
```
