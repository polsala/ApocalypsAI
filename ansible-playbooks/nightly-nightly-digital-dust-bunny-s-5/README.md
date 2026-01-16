# Nightly Digital Dust Bunny Sweeper

## Summary
This Ansible playbook helps you keep your digital infrastructure tidy by identifying and optionally cleaning up "digital dust bunnies" – old, unused files and and directories that accumulate over time on your remote servers. It generates a report detailing these forgotten files, allowing you to review and decide on their fate.

## Features
- Scans specified paths for files and directories older than a configurable age.
- Generates a human-readable report of identified "dust bunnies."
- Supports a dry-run mode to preview changes without actual deletion.
- Can perform actual cleanup (deletion) when `dry_run` is disabled.

## Usage

### Prerequisites
- Ansible installed on your control machine.
- SSH access to your target servers.

### 1. Inventory
Create an `inventory.ini` file listing your target servers.

```ini
[webservers]
web1.example.com
web2.example.com

[databases]
db1.example.com

[all:vars]
ansible_user=your_ssh_user
ansible_ssh_private_key_file=~/.ssh/id_rsa
```

### 2. Configuration
Edit `vars/main.yml` to customize scan paths, age thresholds, and dry-run settings.

```yaml
---
# Configuration for the Digital Dust Bunny Sweeper
scan_paths:
  - /tmp
  - /var/log
  # - /home # Be cautious with /home in production; consider specific user directories.
old_file_age_days: 30 # Files older than this (by access time) will be considered "dust bunnies"
dry_run: true # Set to false to actually delete files. ALWAYS TEST WITH dry_run: true FIRST!
report_path: "/tmp/dust_bunny_report_{{ ansible_hostname }}.txt" # Path on the control machine for the report
```

### 3. Run the Playbook

#### Dry Run (Recommended First Step)
To generate a report without deleting any files:
```bash
ansible-playbook -i inventory.ini dust_bunny_sweeper.yml
```
The report will be saved to the `report_path` specified in `vars/main.yml` on your control machine.

#### Actual Cleanup
**WARNING:** Only run this after reviewing the dry-run report and confirming you want to delete the identified files.
1.  Change `dry_run: false` in `vars/main.yml`.
2.  Run the playbook:
    ```bash
    ansible-playbook -i inventory.ini dust_bunny_sweeper.yml
    ```

## Automated Tests

To run the self-contained tests for this utility:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_dust_bunny_sweeper.yml
```

This test playbook will:
1.  Create a temporary directory on `localhost`.
2.  Create mock "old" and "new" files within it.
3.  Execute the `dust_bunny_sweeper.yml` playbook against this temporary directory in dry-run mode.
4.  Assert that the generated report correctly identifies the "old" file and ignores the "new" file.
5.  Clean up the temporary directory.

### Mock Rationale
The tests use `localhost` connection and create temporary files with specific modification/access times to simulate a server's file system state. This allows for deterministic and offline testing of the playbook's logic without requiring actual remote infrastructure or modifying real system files. The `touch` command is used to precisely control file timestamps, which is crucial for `find` module's `age` parameter.
