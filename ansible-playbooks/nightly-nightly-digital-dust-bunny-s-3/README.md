# Nightly Digital Dust Bunny Sweeper

## Overview
In the vast digital landscapes of our servers, forgotten files and directories accumulate like tiny, digital dust bunnies, silently consuming precious disk space and cluttering the pristine pathways of our systems. The `nightly-digital-dust-bunny-sweep` is an Ansible playbook designed to combat this digital detritus.

This playbook intelligently scans specified paths on your remote servers for files and directories older than a configured threshold. Once identified, these 'dust bunnies' can be optionally archived into a designated 'Digital Attic' (a local archive directory) and then removed from their original location, leaving your servers sparkling clean.

## Features
*   **Configurable Scan Paths**: Define which directories to sweep for old files.
*   **Age Threshold**: Set how old a file or directory must be to be considered a 'dust bunny'.
*   **Optional Archiving**: Choose to archive identified items into a compressed tarball before deletion.
*   **Detailed Reporting**: Generates a report listing all identified and processed dust bunnies.
*   **Idempotent**: Running the playbook multiple times will yield the same result if no new 'dust bunnies' appear.

## Usage

### Prerequisites
*   Ansible installed on your control machine.
*   SSH access to your target servers (if not running locally).

### 1. Inventory Setup
Create an `inventory.ini` file (or use an existing one) that lists your target servers. For local execution, you can use `localhost`.

```ini
[servers]
localhost ansible_connection=local
# my_web_server
# my_db_server
```

### 2. Configure Variables
Edit the `vars/main.yml` file to customize the playbook's behavior:

*   `scan_paths`: A list of directories to scan for old files/directories.
*   `age_threshold_days`: The number of days an item must be older than to be considered a dust bunny.
*   `archive_enabled`: Set to `true` to archive items before removal, `false` to only remove them.
*   `archive_path`: The local directory where archived tarballs and reports will be stored.

```yaml
# vars/main.yml
---
scan_paths:
  - "/var/log/old_app_logs"
  - "/tmp/stale_downloads"
age_threshold_days: 30
archive_enabled: true
archive_path: "/opt/digital_attic_archives"
```

### 3. Run the Playbook
Execute the playbook using the `ansible-playbook` command:

```bash
ansible-playbook -i inventory.ini dust_bunny_sweeper.yml
```

After execution, check the `archive_path` on your control machine (or the delegated host) for the generated report and any archived 'dust bunnies'.

## Testing

To ensure the Digital Dust Bunny Sweeper works as expected, a dedicated test playbook is provided. This test creates mock files and directories with specific modification times, runs the main playbook, and then asserts that the correct actions (archiving, removal, reporting) have been taken.

To run the tests:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_dust_bunny_sweeper.yml
```

The test playbook will clean up all created mock files and directories after completion.
