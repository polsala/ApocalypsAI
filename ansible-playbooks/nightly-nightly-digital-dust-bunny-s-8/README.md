# Nightly Digital Dust Bunny Sweeper

This Ansible playbook helps you keep your remote servers tidy by identifying and optionally removing "digital dust bunnies" \u2013 old, forgotten files that accumulate in specified directories. It provides a whimsical report of what it finds before any cleanup action is taken.

## Features

*   **Configurable Paths**: Specify which directories to scan for old files.
*   **Age Threshold**: Define how old a file must be to be considered a "dust bunny."
*   **Whimsical Reporting**: Generates a report listing all identified dust bunnies.
*   **Optional Cleanup**: Safely remove identified files after review.

## Usage

### Prerequisites

*   Ansible installed on your control machine.
*   SSH access to your target servers (or `ansible_connection=local` for localhost).

### 1. Inventory

Create an `inventory.ini` file listing your target servers. For example:

```ini
[webservers]
web1.example.com
web2.example.com

[databases]
db1.example.com

[local]
localhost ansible_connection=local
```

### 2. Configuration

Edit `src/vars/main.yml` to define the directories to scan and the age threshold.

```yaml
# src/vars/main.yml
---
scan_paths:
  - /tmp/apocalypsai_dust_bunnies_scan
  - /var/log/apocalypsai_old_logs
  # Example with wildcard (Ansible's find module supports globbing)
  # - /home/*/downloads

dust_bunny_age_days: 7 # Files older than 7 days are considered dust bunnies
```

### 3. Run the Playbook

#### Report Only Mode (Recommended First)

This mode will scan for dust bunnies and generate a report, but will **not** delete any files. The report will be printed to your console.

```bash
ansible-playbook -i inventory.ini src/dust_bunny_sweeper.yml
```

#### Cleanup Mode

To actually remove the identified dust bunnies, run the playbook with the `cleanup_mode` variable set to `true`. **Use with caution!** It is highly recommended to run in report-only mode first to review the findings.

```bash
ansible-playbook -i inventory.ini src/dust_bunny_sweeper.yml -e "cleanup_mode=true"
```

### Example Output (Report Only)

```
PLAY [Scan for Digital Dust Bunnies] *******************************************

TASK [Gathering Facts] *********************************************************
ok: [web1.example.com]

TASK [Find potential dust bunnies] *********************************************
ok: [web1.example.com]

TASK [Display Dust Bunny Report (console output)] ******************************
ok: [web1.example.com] => {
    "msg": "\n--- Digital Dust Bunny Report for web1.example.com ---\n\nFound 2 dust bunnies older than 7 days:\n\n- /tmp/apocalypsai_dust_bunnies_scan/old_log.txt (Last modified: 2024-01-15)\n- /var/log/apocalypsai_old_logs/backup.zip (Last modified: 2024-02-01)\n\nConsider sweeping these away!\n---------------------------------------------------\n"
}

... (other tasks and hosts) ...
```

## Automated Tests

The `tests/` directory contains a playbook to verify the functionality.

To run the tests:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_dust_bunny_sweeper.yml
```

This will:
1.  Create dummy old and new files in a temporary directory on `localhost`.
2.  Run the main `dust_bunny_sweeper.yml` playbook in report mode.
3.  Assert that the report correctly identifies the old files.
4.  Run the main `dust_bunny_sweeper.yml` playbook in cleanup mode.
5.  Assert that the old files are removed and new files remain.
6.  Clean up the temporary test files.
