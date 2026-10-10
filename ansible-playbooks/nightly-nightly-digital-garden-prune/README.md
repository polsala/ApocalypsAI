# Nightly Digital Garden Pruner

## Summary
This Ansible playbook helps maintain a tidy 'digital garden' (your server or specific directories) by identifying and optionally pruning stale files and empty directories. It generates a report detailing what it found and what actions it would take (or has taken).

## Features
- Scans specified paths for files older than a configured age.
- Scans specified paths for truly empty directories.
- Supports dry-run mode to report findings without making changes.
- Generates a clear, concise pruning report.

## Usage

### Prerequisites
- Ansible installed on your control machine.
- SSH access (or `ansible_connection=local`) to the target servers.

### 1. Configure Inventory
Create an `inventory.ini` file (or use an existing one) that lists your 'garden servers'.

```ini
[garden_servers]
localhost ansible_connection=local
# Add other servers here, e.g.:
# webserver.example.com
# dbserver.example.com
```

### 2. Configure Pruning Rules
Edit `src/vars/pruner_config.yml` to define the paths to scan, age thresholds for files, file patterns, and whether to perform a dry run or actual pruning.

```yaml
---
pruner_paths:
  - path: "/var/log"
    max_age_days: 30
    file_patterns: ["*.log", "*.gz"]
    age_stamp: mtime # Use 'mtime' (modification time) or 'atime' (access time)
  - path: "/tmp"
    max_age_days: 7
    file_patterns: ["*"]
    age_stamp: mtime
  - path: "/home/{{ ansible_user }}/digital_garden/temp_notes"
    max_age_days: 60
    file_patterns: ["*.txt", "*.md"]
    age_stamp: mtime

pruner_empty_dirs_paths:
  - "/home/{{ ansible_user }}/digital_garden/empty_folders"
  - "/var/tmp"

pruner_dry_run: true # Set to false to actually remove files/dirs
pruner_report_path: "/tmp/digital_garden_pruning_report.txt"
```

### 3. Run the Playbook
To run the playbook in dry-run mode (recommended for initial runs):

```bash
ansible-playbook -i inventory.ini src/prune_garden.yml -e "pruner_dry_run=true"
```

To perform actual pruning (be careful!):

```bash
ansible-playbook -i inventory.ini src/prune_garden.yml -e "pruner_dry_run=false"
```

The report will be displayed in the console and saved to the path specified by `pruner_report_path`.

## Automated Tests

To run the tests for this utility, navigate to the `nightly-digital-garden-pruner` directory and execute:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_prune_garden.yml
```

This will:
1. Create a temporary test directory structure with files and directories of varying ages and emptiness.
2. Run the `prune_garden.yml` playbook in dry-run mode and assert the contents of the generated report.
3. Run the `prune_garden.yml` playbook in actual pruning mode and assert that the expected files and directories have been removed.
4. Clean up the temporary test environment.
